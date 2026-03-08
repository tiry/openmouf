"""Mouf body with 3 servos: roll, pitch, yaw."""

from typing import Optional

from mouf.driver.Servo import ServoDriver
from mouf.driver.ServoMG90S import Servo as ServoMG90S


class MoufBody:
    """Mouf robot body with 3 servos for roll, pitch, and yaw."""
    
    def __init__(
        self,
        roll_channel: int = 0,
        pitch_channel: int = 1,
        yaw_channel: int = 2,
        simulated: bool = True,
        servo_class: Optional[type] = None
    ) -> None:
        """
        Initialize Mouf body with 3 servos.
        
        Args:
            roll_channel: PWM channel for roll servo
            pitch_channel: PWM channel for pitch servo
            yaw_channel: PWM channel for yaw servo
            simulated: If True, use ServoDriver (no hardware).
                      If False, use ServoMG90S (real hardware).
                      Ignored if servo_class is provided.
            servo_class: Custom servo class to use. If provided, overrides simulated.
        """
        self.simulated = simulated
        
        # Choose servo class: custom class > simulated flag
        if servo_class is not None:
            self.servo_class = servo_class
        else:
            self.servo_class = ServoDriver if simulated else ServoMG90S
        
        # Initialize the 3 servos
        self.roll_servo = self.servo_class(roll_channel, initial_angle=90)
        self.pitch_servo = self.servo_class(pitch_channel, initial_angle=90)
        self.yaw_servo = self.servo_class(yaw_channel, initial_angle=90)
    
    def set_roll(self, angle: float, wait: bool = False) -> None:
        """Set roll servo angle."""
        self.roll_servo.move(angle, wait=wait)
    
    def set_pitch(self, angle: float, wait: bool = False) -> None:
        """Set pitch servo angle."""
        self.pitch_servo.move(angle, wait=wait)
    
    def set_yaw(self, angle: float, wait: bool = False) -> None:
        """Set yaw servo angle."""
        self.yaw_servo.move(angle, wait=wait)
    
    def set_all(self, roll: float, pitch: float, yaw: float, wait: bool = False) -> None:
        """Set all servo angles."""
        self.set_roll(roll, wait=wait)
        self.set_pitch(pitch, wait=wait)
        self.set_yaw(yaw, wait=wait)
    
    def get_roll(self) -> float:
        """Get current roll angle."""
        return self.roll_servo.get_angle()
    
    def get_pitch(self) -> float:
        """Get current pitch angle."""
        return self.pitch_servo.get_angle()
    
    def get_yaw(self) -> float:
        """Get current yaw angle."""
        return self.yaw_servo.get_angle()
    
    def get_all(self) -> tuple[float, float, float]:
        """Get all servo angles as (roll, pitch, yaw)."""
        return (self.get_roll(), self.get_pitch(), self.get_yaw())


if __name__ == "__main__":
    # Demo with simulated servos
    body = MoufBody(simulated=True)
    
    print(f"Initial angles: {body.get_all()}")
    
    body.set_all(roll=45, pitch=90, yaw=135)
    print(f"After set_all: {body.get_all()}")
    
    body.set_roll(60)
    body.set_pitch(120)
    body.set_yaw(180)
    print(f"After individual sets: {body.get_all()}")
