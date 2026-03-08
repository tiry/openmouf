"""Interpolation classes for smooth servo movement."""

import math
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from mouf.driver.Servo import ServoDriver


class Interpolator(ABC):
    """Base class for interpolators with drive method."""
    
    def __init__(self, step_size: float = 2.0) -> None:
        """
        Initialize interpolator.
        
        Args:
            step_size: Step size in degrees for movement
        """
        self.step_size = step_size
    
    @abstractmethod
    def drive(
        self,
        servo: "ServoDriver",
        target_angle: float,
        start_angle: Optional[float],
        speed_per_deg: float
    ) -> None:
        """
        Execute movement using this interpolator.
        
        Args:
            servo: The servo to move
            target_angle: Target angle in degrees
            start_angle: Starting angle, or None to use current
            speed_per_deg: Speed in seconds per degree
        """
        pass


class LinearInterpolator(Interpolator):
    """Simple linear interpolation."""
    
    def drive(
        self,
        servo: "ServoDriver",
        target_angle: float,
        start_angle: Optional[float],
        speed_per_deg: float
    ) -> None:
        """Linear movement implementation."""
        local_pos: float = start_angle if start_angle is not None else servo.current_angle
        distance: float = target_angle - local_pos
        
        if abs(distance) < self.step_size:
            servo.move(target_angle)
            return

        direction: int = 1 if distance > 0 else -1
        total_steps: int = int(abs(distance) / self.step_size)
        step_delay: float = speed_per_deg * self.step_size

        for _ in range(total_steps):
            local_pos += (direction * self.step_size)
            servo.move(local_pos, wait=False)
            time.sleep(step_delay)

        servo.move(target_angle, wait=True)


class SmoothInterpolator(Interpolator):
    """Smooth interpolation using cosine ease-in-out."""
    
    def drive(
        self,
        servo: "ServoDriver",
        target_angle: float,
        start_angle: Optional[float],
        speed_per_deg: float
    ) -> None:
        """Smooth movement using cosine interpolation."""
        local_pos: float = start_angle if start_angle is not None else servo.current_angle
        distance: float = target_angle - local_pos
        
        if abs(distance) < self.step_size:
            servo.move(target_angle)
            return

        total_steps: int = int(abs(distance) / self.step_size)
        step_delay: float = speed_per_deg * self.step_size

        for step in range(total_steps):
            # Normalized time (0 to 1)
            t = (step + 1) / total_steps
            
            # Cosine ease-in-out: (1 - cos(t * pi)) / 2
            eased_t = (1 - math.cos(t * math.pi)) / 2
            
            # Calculate position based on eased time
            local_pos = start_angle + (distance * eased_t)
            
            servo.move(local_pos, wait=False)
            time.sleep(step_delay)

        servo.move(target_angle, wait=True)


# Default interpolator class
DEFAULT_INTERPOLATOR_CLASS = SmoothInterpolator