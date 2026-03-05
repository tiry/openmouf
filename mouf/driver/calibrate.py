"""Calibration utility for servo motors."""

import sys
import time
from typing import Optional

from mouf.driver.ServoMTO import Servo, initialize_hardware


def calibrate(servo_id: int, offset: float = 0) -> None:
    """
    Run calibration sequence for a servo.
    
    Args:
        servo_id: The servo channel ID (0-15)
        offset: Calibration offset in degrees
    """
    s: Servo = Servo(servo_id, offset=offset)
    
    steps: list[int] = [0, 90, 180]
    
    for angle in steps:
        print(f"\nMoving to {angle} degrees...")
        s.move(angle)
        time.sleep(2)
        
    print("\nCalibration sequence complete.")


if __name__ == '__main__':
    # Default values
    test_id: int = 0
    test_offset: float = 0
    
    initialize_hardware()

    # Check if user provided arguments via command line
    if len(sys.argv) > 1:
        test_id = int(sys.argv[1])
    if len(sys.argv) > 2:
        test_offset = int(sys.argv[2])

    calibrate(test_id, test_offset)
