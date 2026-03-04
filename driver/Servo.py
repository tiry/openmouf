import time

# --- HARDWARE CONSTANTS ---
I2C_ADDRESS        = 0x40
PWM_FREQ           = 50
MIN_PULSE          = 500   
MAX_PULSE          = 2500  
SERVO_RANGE_DEG    = 180

# --- MOVEMENT CONSTANTS ---
# Speed: 11ms for 60 degrees = 0.011 / 60 seconds per degree
TARGET_SPEED_SPD   = 0.011 / 60 
# Physical limit: If speed is faster than this, we move directly
SERVO_PHYSICAL_LIMIT = 0.1 / 60 

# Chunked Stepping: Move in blocks of X degrees to reduce I2C overhead
STEP_SIZE          = 2  # degrees per step

pwm_instance = None

def get_pwm():
    global pwm_instance
    if pwm_instance is not None:
        return pwm_instance
    from PCA9685 import PCA9685 
    pwm_instance = PCA9685(I2C_ADDRESS, debug=False)
    pwm_instance.setPWMFreq(PWM_FREQ)
    return pwm_instance

class Servo:
    def __init__(self, channel, initial_angle=0):
        self.channel = channel
        self.current_angle = initial_angle

    def move(self, angle):
        """Instant move to a specific angle and updates state."""
        angle = max(0, min(SERVO_RANGE_DEG, angle))
        pulse = int(angle * ((MAX_PULSE - MIN_PULSE) / SERVO_RANGE_DEG) + MIN_PULSE)
        get_pwm().setServoPulse(self.channel, pulse)
        self.current_angle = angle

    def move_to_timed(self, target_angle, start_angle=None, speed_per_deg=TARGET_SPEED_SPD):
        """
        Moves to target_angle. Uses start_angle if provided, 
        otherwise uses internal state.
        """
        # 1. Determine starting point
        current = start_angle if start_angle is not None else self.current_angle
        
        # 2. Logic for immediate jump (High speed or 0 distance)
        distance = target_angle - current
        if speed_per_deg <= SERVO_PHYSICAL_LIMIT or abs(distance) < STEP_SIZE:
            self.move(target_angle)
            return

        # 3. Chunked Stepping Logic
        direction = 1 if distance > 0 else -1
        total_steps = int(abs(distance) / STEP_SIZE)
        
        # Calculate delay based on the jump size (e.g., delay for 5 degrees)
        step_delay = speed_per_deg * STEP_SIZE

        for _ in range(total_steps):
            current += (direction * STEP_SIZE)
            self.move(current)
            time.sleep(step_delay)

        # 4. Final adjustment (ensure we hit the exact target)
        if self.current_angle != target_angle:
            self.move(target_angle)

if __name__ == '__main__':
    # Initialize at 0 degrees
    s = Servo(1, initial_angle=0)
    s.move(0) 
    time.sleep(5)

    print(f"Sweeping to 180 using chunked steps of {STEP_SIZE} deg...")
    s.move_to_timed(180) 
    time.sleep(5)

    print("Returning to 90 using an explicit start angle of 180...")
    s.move_to_timed(target_angle=90, start_angle=180, speed_per_deg=0.01)


