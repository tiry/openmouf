"""CLI for controlling servo motors."""

import click

from mouf.driver.Servo import ServoDriver


@click.command()
@click.argument('angle', type=float)
@click.option('--channel', '-c', default=0, help='PWM channel number (0-15)')
@click.option('--offset', '-o', default=0, help='Calibration offset in degrees')
@click.option('--min', 'min_angle', default=0, help='Minimum angle in degrees')
@click.option('--max', 'max_angle', default=180, help='Maximum angle in degrees')
@click.option('--wait/--no-wait', default=False, help='Wait for servo to reach position')
def servo(angle, channel, offset, min_angle, max_angle, wait):
    """Move a servo to the specified angle.
    
    ANGLE: Target angle in degrees.
    """
    servo = ServoDriver(
        channel=channel,
        offset=offset,
        min_angle=min_angle,
        max_angle=max_angle
    )
    
    click.echo(f"Moving servo on channel {channel} to {angle} degrees...")
    servo.move(angle, wait=wait)
    
    actual_angle = servo.get_angle()
    click.echo(f"Servo moved to {actual_angle} degrees")


if __name__ == '__main__':
    servo()