#!/usr/bin/env python3
"""PCA9685 16-Channel PWM Servo Driver."""

import math
from typing import Optional

import smbus2 as smbus


class PCA9685:
    """PCA9685 16-channel PWM servo driver."""

    # Register addresses
    __SUBADR1: int = 0x02
    __SUBADR2: int = 0x03
    __SUBADR3: int = 0x04
    __MODE1: int = 0x00
    __PRESCALE: int = 0xFE
    __LED0_ON_L: int = 0x06
    __LED0_ON_H: int = 0x07
    __LED0_OFF_L: int = 0x08
    __LED0_OFF_H: int = 0x09
    __ALLLED_ON_L: int = 0xFA
    __ALLLED_ON_H: int = 0xFB
    __ALLLED_OFF_L: int = 0xFC
    __ALLLED_OFF_H: int = 0xFD

    def __init__(self, address: int = 0x40, debug: bool = False) -> None:
        """
        Initialize the PCA9685 driver.
        
        Args:
            address: I2C address of the PCA9685 (default 0x40)
            debug: Enable debug output
        """
        self.bus: smbus.SMBus = smbus.SMBus(1)
        self.address: int = address
        self.debug: bool = debug
        if self.debug:
            print("Reseting PCA9685")
        self.write(self.__MODE1, 0x00)

    def write(self, reg: int, value: int) -> None:
        """
        Write an 8-bit value to the specified register.
        
        Args:
            reg: Register address
            value: Value to write
        """
        self.bus.write_byte_data(self.address, reg, value)
        if self.debug:
            print(f"I2C: Write 0x{value:02X} to register 0x{reg:02X}")

    def read(self, reg: int) -> int:
        """
        Read an unsigned byte from the I2C device.
        
        Args:
            reg: Register address
            
        Returns:
            The byte value read from the register
        """
        result: int = self.bus.read_byte_data(self.address, reg)
        if self.debug:
            print(f"I2C: Device 0x{self.address:02X} returned 0x{result & 0xFF:02X} from reg 0x{reg:02X}")
        return result

    def setPWMFreq(self, freq: float) -> None:
        """
        Set the PWM frequency.
        
        Args:
            freq: Frequency in Hz
        """
        prescaleval: float = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        
        if self.debug:
            print(f"Setting PWM frequency to {freq:d} Hz")
            print(f"Estimated pre-scale: {prescaleval:d}")
        
        prescale: int = math.floor(prescaleval + 0.5)
        if self.debug:
            print(f"Final pre-scale: {prescale:d}")

        oldmode: int = self.read(self.__MODE1)
        newmode: int = (oldmode & 0x7F) | 0x10  # sleep
        self.write(self.__MODE1, newmode)  # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        # sleep 5 microseconds
        import time
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel: int, on: int, off: int) -> None:
        """
        Set a single PWM channel.
        
        Args:
            channel: Channel number (0-15)
            on: On time (0-4095)
            off: Off time (0-4095)
        """
        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)
        
        if self.debug:
            print(f"channel: {channel:d}  LED_ON: {on:d} LED_OFF: {off:d}")

    def setServoPulse(self, channel: int, pulse: float) -> None:
        """
        Set the servo pulse width.
        
        The PWM frequency must be 50Hz.
        
        Args:
            channel: Channel number (0-15)
            pulse: Pulse width in microseconds
        """
        # PWM frequency is 50Hz, the period is 20000us
        pulse_scaled: float = pulse * 4096.0 / 20000.0
        self.setPWM(channel, 0, int(pulse_scaled))
