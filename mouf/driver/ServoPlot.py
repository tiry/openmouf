import time
from typing import Optional

from mouf.driver.Servo import ServoDriver


class Servo(ServoDriver):
    
    def __init__(self, channel: int, initial_angle: float = 0, offset: float = 0) -> None:
        # Initialize data before super().__init__ because parent calls send_PWM
        self.data: list = []
        super().__init__(channel, initial_angle, offset)

    def send_PWM(self, channel, pulse):
        self.data.append((time.time_ns(), pulse, self.current_angle))

    def get_data(self) -> list:
        return self.data

if __name__ == '__main__':
    pass