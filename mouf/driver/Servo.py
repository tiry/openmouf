"""Multi-threaded optimized Servo driver."""

import threading
import time
from typing import Optional

# --- SETTINGS ---
STEP_SIZE: float = 2.0
# PHYSICAL CONSTANTS
# 0.11s per 60 degrees = 0.001833s per degree
SERVO_SPEED_PER_DEG: float = 0.11 / 60 
# Small buffer for inertia and I2C latency
MECHANICAL_LAG: float = 0.05


class ServoDriver:
    """Thread-safe servo driver with position control."""
    
    def __init__(self, channel: int, initial_angle: float = 0, offset: float = 0) -> None:
        """
        Initialize a servo on a given channel.
        
        Args:
            channel: PWM channel number (0-15)
            initial_angle: Starting angle in degrees
            offset: Calibration offset. If servo is at 90 when it should be 0,
                    set offset to -90.
        """
        self.channel: int = channel
        self.offset: float = offset
        self.current_angle: float = initial_angle
        self._stop_event: threading.Event = threading.Event()
        
        # Initialize at the corrected position
        self.move(initial_angle)

    def send_PWM(self, channel, pulse):
        print(f"Channel {channel} => {pulse}")

    def get_angle(self):
        return  self.current_angle

    def move(self, angle: float, wait: bool = False) -> None:
        """
        Move to an angle, adjusted by the offset.
        
        Args:
            angle: Target logical angle in degrees (0-180)
            wait: If True, blocks execution until the servo physically arrives.
        """
        # Calculate travel distance BEFORE updating current_angle
        distance = abs(angle - self.current_angle)
        
        # Apply calibration offset
        adjusted_angle: float = angle + self.offset
        
        # Keep hardware within safe physical bounds (0-180)
        safe_angle: float = max(0, min(180, adjusted_angle))
        
        # Convert angle to pulse width (500-2500us for 0-180 degrees)
        pulse: int = int(safe_angle * (2000 / 180) + 500)
        
        self.send_PWM(self.channel, pulse)
        
        # Update logical state
        self.current_angle = angle

        # Physical Sync Logic
        if wait and distance > 0:
            # Wait for (deg * speed) + overhead
            travel_time = (distance * SERVO_SPEED_PER_DEG) + MECHANICAL_LAG
            time.sleep(travel_time)

    def _threaded_loop(
        self, 
        target_angle: float, 
        start_angle: Optional[float], 
        speed_per_deg: float
    ) -> None:
        """Internal threaded movement loop."""
        local_pos: float = start_angle if start_angle is not None else self.current_angle
        distance: float = target_angle - local_pos
        
        if abs(distance) < STEP_SIZE:
            self.move(target_angle)
            return

        direction: int = 1 if distance > 0 else -1
        total_steps: int = int(abs(distance) / STEP_SIZE)
        step_delay: float = speed_per_deg * STEP_SIZE

        for _ in range(total_steps):
            if self._stop_event.is_set():
                return
            local_pos += (direction * STEP_SIZE)
            self.move(local_pos, wait=False)
            time.sleep(step_delay)

        self.move(target_angle, wait=True)

    def move_sequence(
        self, 
        sequence: list, 
        speed_per_deg: float = SERVO_SPEED_PER_DEG, 
        loops: int = 1
    ) -> threading.Thread:
        """
        Execute a sequence of movements.
        
        Args:
            sequence: List of target angles or (angle, pause) tuples
            speed_per_deg: Movement speed in seconds per degree
            loops: Number of times to repeat the sequence
            
        Returns:
            The running thread handle
        """
        def run_sequence() -> None:
            self._stop_event.clear()
            for _ in range(loops):
                for item in sequence:
                    if self._stop_event.is_set():
                        return
                    target, pause = (
                        item if isinstance(item, tuple) 
                        else (item, 0)
                    )
                    self._threaded_loop(target, self.current_angle, speed_per_deg)
                    if pause > 0:
                        time.sleep(pause)
        
        t: threading.Thread = threading.Thread(target=run_sequence, daemon=True)
        t.start()
        return t


if __name__ == '__main__':
  
    s1: Servo = ServoDriver(0, initial_angle=0, offset=0)
    s2: Servo = ServoDriver(1, initial_angle=0, offset=-90)

    print("Both servos should now be at their respective '0' positions...")
    time.sleep(2)

    # Now when you move them to 90, they will both move to the same physical spot
    s1.move(90)
    s2.move(90)
