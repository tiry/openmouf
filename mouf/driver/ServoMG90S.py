"""Multi-threaded optimized Servo driver."""

import threading
import time
from typing import Optional
from mouf.driver.Servo import ServoDriver

# --- SETTINGS ---
I2C_ADDRESS: int = 0x40
PWM_FREQ: int = 50

# Module-level globals
_BUS_LOCK: threading.RLock = threading.RLock()
_GLOBAL_PWM_DRIVER: Optional["PCA9685"] = None

def initialize_hardware() -> None:
    """Initialize the global PWM driver hardware."""
    global _GLOBAL_PWM_DRIVER
    with _BUS_LOCK:
        if _GLOBAL_PWM_DRIVER is None:
            from mouf.driver.PCA9685 import PCA9685
            _GLOBAL_PWM_DRIVER = PCA9685(I2C_ADDRESS, debug=False)
            _GLOBAL_PWM_DRIVER.setPWMFreq(PWM_FREQ)


class Servo(ServoDriver):
    
    def send_PWM(self, channel, pulse):
        with _BUS_LOCK:
            if _GLOBAL_PWM_DRIVER is not None:
                _GLOBAL_PWM_DRIVER.setServoPulse(channel, pulse)


if __name__ == '__main__':
    initialize_hardware()
    
    # CALIBRATION EXAMPLE:
    # If Servo 0 is perfect, offset = 0
    # If Servo 1 sits at 90 when you want 0, offset = -90
    s1: Servo = Servo(0, initial_angle=0, offset=0)
    s2: Servo = Servo(1, initial_angle=0, offset=-90)

    print("Both servos should now be at their respective '0' positions...")
    time.sleep(2)

    # Now when you move them to 90, they will both move to the same physical spot
    s1.move(90)
    s2.move(90)
