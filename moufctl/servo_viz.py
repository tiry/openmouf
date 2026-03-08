"""Servo visualization - plot servo movements across time."""

import time

import matplotlib.pyplot as plt

from mouf.driver.body import MoufBody
from mouf.driver.ServoPlot import Servo as ServoPlot


def run_sequence_viz(sequence, loops=1):
    """
    Run a move sequence and visualize servo positions over time.
    
    Args:
        sequence: List of (roll, pitch, yaw) tuples
        loops: Number of times to repeat the sequence
    """
    # Create body with ServoPlot to capture data
    body = MoufBody(
        roll_channel=0,
        pitch_channel=1,
        yaw_channel=2,
        simulated=True,
        servo_class=ServoPlot
    )
    
    # Run the sequence for each servo
    roll_sequence = [(roll, 0.05) for roll, _, _ in sequence]
    pitch_sequence = [(pitch, 0.05) for _, pitch, _ in sequence]
    yaw_sequence = [(yaw, 0.05) for _, _, yaw in sequence]
    
    # Start all three sequences
    roll_thread = body.roll_servo.move_sequence(roll_sequence, loops=loops)
    pitch_thread = body.pitch_servo.move_sequence(pitch_sequence, loops=loops)
    yaw_thread = body.yaw_servo.move_sequence(yaw_sequence, loops=loops)
    
    # Wait for completion
    roll_thread.join()
    pitch_thread.join()
    yaw_thread.join()
    
    # Get data from each servo (timestamp, pulse, angle)
    roll_data = body.roll_servo.get_data()
    pitch_data = body.pitch_servo.get_data()
    yaw_data = body.yaw_servo.get_data()
    
    # Normalize times to start at 0
    all_data = roll_data + pitch_data + yaw_data
    if all_data:
        t0 = min(d[0] for d in all_data)
    else:
        t0 = 0
    
    # Convert to relative time in seconds
    def normalize(data):
        return [(float(t - t0) / 1e9, p, a) for t, p, a in data]
    
    roll_times = normalize(roll_data)
    pitch_times = normalize(pitch_data)
    yaw_times = normalize(yaw_data)
    
    # Plot with dual Y axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot pulse on left Y axis
    color = 'tab:blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('PWM Pulse', color=color)
    ax1.plot([t for t, _, _ in roll_times], [p for _, p, _ in roll_times], 
             label='Roll Pulse', color='blue', marker='.', linestyle='-', markersize=3)
    ax1.plot([t for t, _, _ in pitch_times], [p for _, p, _ in pitch_times], 
             label='Pitch Pulse', color='green', marker='.', linestyle='-', markersize=3)
    ax1.plot([t for t, _, _ in yaw_times], [p for _, p, _ in yaw_times], 
             label='Yaw Pulse', color='red', marker='.', linestyle='-', markersize=3)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Plot angle on right Y axis
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Angle (degrees)', color=color)
    ax2.plot([t for t, _, _ in roll_times], [a for _, _, a in roll_times], 
             label='Roll Angle', color='blue', marker='^', linestyle='--', markersize=3, alpha=0.7)
    ax2.plot([t for t, _, _ in pitch_times], [a for _, _, a in pitch_times], 
             label='Pitch Angle', color='green', marker='^', linestyle='--', markersize=3, alpha=0.7)
    ax2.plot([t for t, _, _ in yaw_times], [a for _, _, a in yaw_times], 
             label='Yaw Angle', color='red', marker='^', linestyle='--', markersize=3, alpha=0.7)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Add legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    ax1.set_title('Servo Movements Over Time')
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def demo():
    """Run a demo visualization."""
    sequence = [
        (45, 90, 135),
        (90, 90, 90),
        (135, 45, 45),
        (90, 90, 90),
    ]
    run_sequence_viz(sequence)


if __name__ == "__main__":
    demo()