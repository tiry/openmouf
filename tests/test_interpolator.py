"""Unit tests for interpolator module."""

import math
import unittest
from unittest.mock import Mock

from mouf.driver.interpolator import (
    Interpolator,
    LinearInterpolator,
    SmoothInterpolator,
    DEFAULT_INTERPOLATOR_CLASS,
)


class TestInterpolator(unittest.TestCase):
    """Test cases for Interpolator classes."""
    
    def test_linear_interpolator_step_size(self):
        """Test LinearInterpolator stores step_size."""
        interp = LinearInterpolator(step_size=5.0)
        self.assertEqual(interp.step_size, 5.0)
    
    def test_smooth_interpolator_step_size(self):
        """Test SmoothInterpolator stores step_size."""
        interp = SmoothInterpolator(step_size=3.0)
        self.assertEqual(interp.step_size, 3.0)
    
    def test_default_interpolator_is_smooth(self):
        """Test default interpolator is SmoothInterpolator."""
        self.assertEqual(DEFAULT_INTERPOLATOR_CLASS, SmoothInterpolator)
    
    def test_linear_drive_small_distance(self):
        """Test LinearInterpolator handles small distance (< step_size)."""
        interp = LinearInterpolator(step_size=2.0)
        mock_servo = Mock()
        mock_servo.current_angle = 90
        
        interp.drive(mock_servo, target_angle=91, start_angle=90, speed_per_deg=0.01)
        
        # Should move directly to target
        mock_servo.move.assert_called_once_with(91)
    
    def test_linear_drive_calls_move_multiple_times(self):
        """Test LinearInterpolator calls move multiple times for larger distance."""
        interp = LinearInterpolator(step_size=10.0)
        mock_servo = Mock()
        mock_servo.current_angle = 0
        
        # Distance is 90, step_size is 10, so should call move ~9 times
        interp.drive(mock_servo, target_angle=90, start_angle=0, speed_per_deg=0.001)
        
        # Should call move at least 8 times (for steps) + 1 final call
        self.assertGreaterEqual(mock_servo.move.call_count, 8)
    
    def test_smooth_drive_small_distance(self):
        """Test SmoothInterpolator handles small distance (< step_size)."""
        interp = SmoothInterpolator(step_size=2.0)
        mock_servo = Mock()
        mock_servo.current_angle = 90
        
        interp.drive(mock_servo, target_angle=91, start_angle=90, speed_per_deg=0.01)
        
        # Should move directly to target
        mock_servo.move.assert_called_once_with(91)
    
    def test_smooth_drive_uses_cosine_easing(self):
        """Test SmoothInterpolator produces different results than linear."""
        smooth_interp = SmoothInterpolator(step_size=10.0)
        linear_interp = LinearInterpolator(step_size=10.0)
        
        mock_servo = Mock()
        mock_servo.current_angle = 0
        
        # Run both interpolators
        smooth_interp.drive(mock_servo, target_angle=90, start_angle=0, speed_per_deg=0.001)
        smooth_positions = [call[0][0] for call in mock_servo.move.call_args_list[:-1]]
        
        mock_servo.reset_mock()
        linear_interp.drive(mock_servo, target_angle=90, start_angle=0, speed_per_deg=0.001)
        linear_positions = [call[0][0] for call in mock_servo.move.call_args_list[:-1]]
        
        # Smooth should produce different positions than linear
        self.assertNotEqual(smooth_positions, linear_positions)
        
        # Linear should have equal increments
        linear_increments = [linear_positions[i+1] - linear_positions[i] for i in range(len(linear_positions)-1)]
        self.assertTrue(all(abs(inc - linear_increments[0]) < 0.01 for inc in linear_increments))
    
    def test_interpolator_respects_start_angle(self):
        """Test interpolator uses provided start_angle."""
        interp = LinearInterpolator(step_size=10.0)
        mock_servo = Mock()
        mock_servo.current_angle = 999  # Should not be used
        
        interp.drive(mock_servo, target_angle=90, start_angle=45, speed_per_deg=0.001)
        
        # First call should be at start_angle + step_size
        first_call = mock_servo.move.call_args_list[0][0][0]
        self.assertEqual(first_call, 55)  # 45 + 10
    
    def test_interpolator_negative_distance(self):
        """Test interpolator handles negative distance (moving backward)."""
        interp = LinearInterpolator(step_size=10.0)
        mock_servo = Mock()
        mock_servo.current_angle = 90
        
        interp.drive(mock_servo, target_angle=0, start_angle=90, speed_per_deg=0.001)
        
        # First call should be at start_angle - step_size
        first_call = mock_servo.move.call_args_list[0][0][0]
        self.assertEqual(first_call, 80)  # 90 - 10


if __name__ == '__main__':
    unittest.main()