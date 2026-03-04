import time
import threading

# --- SETTINGS ---
I2C_ADDRESS = 0x40
PWM_FREQ    = 50
STEP_SIZE   = 2  
DEFAULT_SPEED = 0.011 / 60 

_BUS_LOCK = threading.RLock()
_GLOBAL_PWM_DRIVER = None

def initialize_hardware():
    global _GLOBAL_PWM_DRIVER
    with _BUS_LOCK:
        if _GLOBAL_PWM_DRIVER is None:
            from PCA9685 import PCA9685
            _GLOBAL_PWM_DRIVER = PCA9685(I2C_ADDRESS, debug=False)
            _GLOBAL_PWM_DRIVER.setPWMFreq(PWM_FREQ)

class Servo:
    def __init__(self, channel, initial_angle=0, offset=0):
        """
        offset: Use this to calibrate. If your servo is at 90 when it should be 0,
                set offset to -90.
        """
        self.channel = channel
        self.offset = offset
        self.current_angle = initial_angle
        self._stop_event = threading.Event()
        
        # Initialize at the corrected position
        self.move(initial_angle)

    def move(self, angle):
        """Moves to an angle adjusted by the offset."""
        # The angle the user wants + the calibration offset
        adjusted_angle = angle + self.offset
        
        # Keep the hardware within safe physical bounds (0-180)
        safe_angle = max(0, min(180, adjusted_angle))
        
        pulse = int(safe_angle * (2000 / 180) + 500)
        
        with _BUS_LOCK:
            if _GLOBAL_PWM_DRIVER:
                _GLOBAL_PWM_DRIVER.setServoPulse(self.channel, pulse)
        
        # We store the 'logical' angle the user requested, not the 'offset' one
        self.current_angle = angle

    def _threaded_loop(self, target_angle, start_angle, speed_per_deg):
        local_pos = start_angle if start_angle is not None else self.current_angle
        distance = target_angle - local_pos
        
        if abs(distance) < STEP_SIZE:
            self.move(target_angle)
            return

        direction = 1 if distance > 0 else -1
        total_steps = int(abs(distance) / STEP_SIZE)
        step_delay = speed_per_deg * STEP_SIZE

        for _ in range(total_steps):
            if self._stop_event.is_set():
                return
            local_pos += (direction * STEP_SIZE)
            self.move(local_pos)
            time.sleep(step_delay)

        self.move(target_angle)

    def move_sequence(self, sequence, speed_per_deg=DEFAULT_SPEED, loops=1):
        def run_sequence():
            self._stop_event.clear()
            for _ in range(loops):
                for item in sequence:
                    if self._stop_event.is_set(): return
                    target, pause = item if isinstance(item, tuple) else (item, 0)
                    self._threaded_loop(target, self.current_angle, speed_per_deg)
                    if pause > 0: time.sleep(pause)
        
        t = threading.Thread(target=run_sequence, daemon=True)
        t.start()
        return t

if __name__ == '__main__':
    initialize_hardware()
    
    # CALIBRATION EXAMPLE:
    # If Servo 0 is perfect, offset = 0
    # If Servo 1 sits at 90 when you want 0, offset = -90
    s1 = Servo(0, initial_angle=0, offset=0)
    s2 = Servo(1, initial_angle=0, offset=-90) 

    print("Both servos should now be at their respective '0' positions...")
    time.sleep(2)

    # Now when you move them to 90, they will both move to the same physical spot
    t1 = s1.move_to_timed(90)
    t2 = s2.move_to_timed(90)
