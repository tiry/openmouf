from ServoMTO import Servo, initialize_hardware
import time
import sys

def calibrate(servo_id, offset=0):
    s = Servo(servo_id, offset=offset)
    
    steps = [0, 90, 180]
    
    for angle in steps:
        print(f"\nMoving to {angle} degrees...")
        s.move(angle)
        time.sleep(2)
        
    print("\nCalibration sequence complete.")

if __name__ == '__main__':
    # You can change these two variables to test different servos
    TEST_ID = 0      # Change this to your Servo ID (0, 1, 2...)
    TEST_OFFSET = 0  # Adjust this (e.g., -10 or 15) to center the servo
    
    initialize_hardware()

    # Check if user provided arguments via command line
    if len(sys.argv) > 1:
        TEST_ID = int(sys.argv[1])
    if len(sys.argv) > 2:
        TEST_OFFSET = int(sys.argv[2])

    calibrate(TEST_ID, TEST_OFFSET)

