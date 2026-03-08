"""Unit tests for Servo driver."""

import time
import unittest

from mouf.driver.Servo import ServoDriver, SERVO_SPEED_PER_DEG, MECHANICAL_LAG


class TestServoDriver(unittest.TestCase):
    """Test cases for ServoDriver class."""
    
    def test_initial_angle(self):
        """Test servo initializes with correct angle."""
        servo = ServoDriver(0, initial_angle=45)
        self.assertEqual(servo.get_angle(), 45)
    
    def test_initial_angle_with_offset(self):
        """Test servo applies offset during initialization."""
        servo = ServoDriver(0, initial_angle=0, offset=10)
        # Logical angle is 0, but physical should be 10
        self.assertEqual(servo.get_angle(), 0)
    
    def test_move_updates_angle(self):
        """Test move() updates current_angle."""
        servo = ServoDriver(0, initial_angle=0)
        servo.move(90)
        self.assertEqual(servo.get_angle(), 90)
    
    def test_move_with_offset(self):
        """Test move() applies calibration offset."""
        servo = ServoDriver(0, initial_angle=0, offset=-10)
        # Move to logical 90, physical should be 80
        servo.move(90)
        # Logical angle is 90
        self.assertEqual(servo.get_angle(), 90)
    
    def test_move_clamps_to_safe_bounds(self):
        """Test move() clamps angle to 0-180 range (default max)."""
        servo = ServoDriver(0, initial_angle=0)
        # Move beyond 180 - should clamp to max (180)
        servo.move(200)
        self.assertEqual(servo.get_angle(), 180)
    
    def test_move_negative_clamped(self):
        """Test negative angles are clamped to 0 (default min)."""
        servo = ServoDriver(0, initial_angle=0)
        servo.move(-30)
        self.assertEqual(servo.get_angle(), 0)
    
    def test_move_waits_when_requested(self):
        """Test move() with wait=True blocks for travel time."""
        servo = ServoDriver(0, initial_angle=0)
        
        start = time.time()
        servo.move(90, wait=True)
        elapsed = time.time() - start
        
        # Should wait for (90 * speed) + mechanical_lag
        expected_wait = (90 * SERVO_SPEED_PER_DEG) + MECHANICAL_LAG
        self.assertGreater(elapsed, expected_wait * 0.9)  # Allow 10% tolerance
        self.assertLess(elapsed, expected_wait * 1.5)
    
    def test_move_no_wait_by_default(self):
        """Test move() doesn't wait by default."""
        servo = ServoDriver(0, initial_angle=0)
        
        start = time.time()
        servo.move(90)  # wait=False by default
        elapsed = time.time() - start
        
        # Should return immediately
        self.assertLess(elapsed, 0.1)
    
    def test_get_channel(self):
        """Test channel is stored correctly."""
        servo = ServoDriver(5, initial_angle=0)
        self.assertEqual(servo.channel, 5)
    
    def test_offset_stored(self):
        """Test offset is stored correctly."""
        servo = ServoDriver(0, initial_angle=0, offset=-15)
        self.assertEqual(servo.offset, -15)
    
    def test_move_sequence_starts_thread(self):
        """Test move_sequence returns a thread."""
        servo = ServoDriver(0, initial_angle=0)
        
        sequence = [0, 45, 90, 45]
        thread = servo.move_sequence(sequence, loops=1)
        
        # Should return a thread
        self.assertIsNotNone(thread)
        self.assertTrue(thread.daemon)
        
        # Wait for sequence to complete
        thread.join(timeout=5)
    
    def test_move_sequence_accepts_tuples(self):
        """Test move_sequence accepts (angle, pause) tuples."""
        servo = ServoDriver(0, initial_angle=0)
        
        sequence = [(0, 0.01), (90, 0.01)]
        thread = servo.move_sequence(sequence, loops=1)
        
        thread.join(timeout=5)
        # If we get here without timeout, test passes
    
    def test_multiple_servos_independent(self):
        """Test multiple servos maintain independent state."""
        servo1 = ServoDriver(0, initial_angle=0)
        servo2 = ServoDriver(1, initial_angle=90)
        
        self.assertEqual(servo1.get_angle(), 0)
        self.assertEqual(servo2.get_angle(), 90)
        
        servo1.move(45)
        servo2.move(135)
        
        self.assertEqual(servo1.get_angle(), 45)
        self.assertEqual(servo2.get_angle(), 135)
    
    def test_min_angle_stored(self):
        """Test min_angle is stored correctly."""
        servo = ServoDriver(0, initial_angle=0, min_angle=10)
        self.assertEqual(servo.min_angle, 10)
    
    def test_max_angle_stored(self):
        """Test max_angle is stored correctly."""
        servo = ServoDriver(0, initial_angle=0, max_angle=90)
        self.assertEqual(servo.max_angle, 90)
    
    def test_move_clamped_to_min(self):
        """Test move() clamps angle to min_angle."""
        servo = ServoDriver(0, initial_angle=0, min_angle=10, max_angle=90)
        servo.move(5)  # Below min
        self.assertEqual(servo.get_angle(), 10)
    
    def test_move_clamped_to_max(self):
        """Test move() clamps angle to max_angle."""
        servo = ServoDriver(0, initial_angle=0, min_angle=10, max_angle=90)
        servo.move(100)  # Above max
        self.assertEqual(servo.get_angle(), 90)
    
    def test_move_within_bounds(self):
        """Test move() works within bounds."""
        servo = ServoDriver(0, initial_angle=0, min_angle=10, max_angle=90)
        servo.move(50)
        self.assertEqual(servo.get_angle(), 50)
    
    def test_custom_min_max_defaults(self):
        """Test default min/max values."""
        servo = ServoDriver(0, initial_angle=0)
        self.assertEqual(servo.min_angle, 0)
        self.assertEqual(servo.max_angle, 180)


if __name__ == '__main__':
    unittest.main()
