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
    def __init__(self, channel, initial_angle=0):
        self.channel = channel
        self.current_angle = initial_angle
        self._stop_event = threading.Event()
        self.move(initial_angle)

    def move(self, angle):
        angle = max(0, min(180, angle))
        pulse = int(angle * (2000 / 180) + 500)
        with _BUS_LOCK:
            if _GLOBAL_PWM_DRIVER:
                _GLOBAL_PWM_DRIVER.setServoPulse(self.channel, pulse)
        self.current_angle = angle

    def _threaded_loop(self, target_angle, start_angle, speed_per_deg):
        """Internal blocking move used by threads."""
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
                return # Exit early if stopped
            local_pos += (direction * STEP_SIZE)
            self.move(local_pos)
            time.sleep(step_delay)

        self.move(target_angle)

    def move_to_timed(self, target_angle, start_angle=None, speed_per_deg=DEFAULT_SPEED):
        """Single move in a background thread."""
        self._stop_event.clear()
        t = threading.Thread(
            target=self._threaded_loop, 
            args=(target_angle, start_angle, speed_per_deg),
            daemon=True 
        )
        t.start()
        return t

    def move_sequence(self, angles, speed_per_deg=DEFAULT_SPEED, loops=1):
        """
        Takes a list of angles [0, 180, 90] and executes them in order.
        'loops' allows for easy oscillation.
        """
        def run_sequence():
            self._stop_event.clear()
            for _ in range(loops):
                for target in angles:
                    if self._stop_event.is_set():
                        return
                    # We call the internal loop directly because we are already in a thread
                    self._threaded_loop(target, self.current_angle, speed_per_deg)
        
        t = threading.Thread(target=run_sequence, daemon=True)
        t.start()
        return t

if __name__ == '__main__':
    initialize_hardware()
    
    s1 = Servo(0)
    s2 = Servo(1)

    print("Starting complex movement sequence...")
    
    # Servo 0 will oscillate between 0 and 180 three times
    t1 = s1.move_sequence([180, 0], speed_per_deg=0.005, loops=3)
    
    # Servo 1 will do a 'triangle' move once
    t2 = s2.move_sequence([45, 135, 90], speed_per_deg=0.01, loops=1)

    t1.join()
    t2.join()
    print("All sequences finished.")
