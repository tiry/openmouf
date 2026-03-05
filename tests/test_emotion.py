"""Tests for emotion module."""

import numpy as np
from pathlib import Path

import pytest

from mouf.engine import data_utils
from mouf.engine.emotion import MoufEmotionEngine


class TestMoufEmotionEngine:
    """Tests for MoufEmotionEngine class."""
    
    def test_init_default_values(self) -> None:
        """Test initialization with default values."""
        # Clear cache to use test data
        data_utils._states_cache["data"] = None
        
        # Patch the default path for testing
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            
            # Check initial position is at origin
            assert np.allclose(engine.pos, [0.0, 0.0])
            # Check initial velocity is zero
            assert np.allclose(engine.vel, [0.0, 0.0])
            # Check physics parameters
            assert engine.friction == 0.95
            assert engine.impulse_scale == 0.05
            assert engine.homeostasis == 0.0001
            # Check states loaded
            assert len(engine.states) > 0
        finally:
            data_utils.states_csv_path = original_default
            
    def test_apply_impulse(self) -> None:
        """Test applying impulse to the emotion state."""
        # Use test data
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            initial_vel = engine.vel.copy()
            
            # Apply impulse
            engine.apply_impulse(1.0, 0.5)
            
            # Velocity should have increased
            assert not np.allclose(engine.vel, initial_vel)
        finally:
            data_utils.states_csv_path = original_default
            
    def test_update_returns_position(self) -> None:
        """Test that update returns the current position."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            result = engine.update()
            
            assert isinstance(result, np.ndarray)
            assert result.shape == (2,)
        finally:
            data_utils.states_csv_path = original_default
            
    def test_update_applies_friction(self) -> None:
        """Test that friction is applied during update."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            engine.vel = np.array([1.0, 1.0])
            
            initial_vel_magnitude = np.linalg.norm(engine.vel)
            engine.update()
            final_vel_magnitude = np.linalg.norm(engine.vel)
            
            # Velocity should decrease due to friction
            assert final_vel_magnitude < initial_vel_magnitude
        finally:
            data_utils.states_csv_path = original_default
            
    def test_update_applies_homeostasis(self) -> None:
        """Test that homeostasis pulls position toward origin."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            engine.pos = np.array([0.5, 0.5])
            engine.vel = np.array([0.0, 0.0])  # No velocity
            
            initial_dist = np.linalg.norm(engine.pos)
            engine.update()
            final_dist = np.linalg.norm(engine.pos)
            
            # Position should have moved closer to origin
            assert final_dist < initial_dist
        finally:
            data_utils.states_csv_path = original_default
            
    def test_boundary_clamping(self) -> None:
        """Test that position is clamped to unit circle."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            engine.pos = np.array([1.5, 0.0])  # Outside unit circle
            engine.vel = np.array([0.0, 0.0])
            
            engine.update()
            
            # Position should be clamped to unit circle
            assert np.linalg.norm(engine.pos) <= 1.0
        finally:
            data_utils.states_csv_path = original_default
            
    def test_get_active_states_returns_list(self) -> None:
        """Test that get_active_states returns a list."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            engine.pos = np.array([0.0, 0.0])  # Neutral position
            
            active = engine.get_active_states()
            
            assert isinstance(active, list)
        finally:
            data_utils.states_csv_path = original_default
            
    def test_get_active_states_sorted_by_intensity(self) -> None:
        """Test that active states are sorted by intensity."""
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        original_default = data_utils.states_csv_path
        data_utils.states_csv_path = test_csv
        
        try:
            engine = MoufEmotionEngine()
            # Position at a state center should give highest intensity
            engine.pos = np.array([0.5, 0.5])  # Center of "Happy" state
            
            active = engine.get_active_states()
            
            if active:
                # First item should have highest intensity
                intensities = [s[1] for s in active]
                assert intensities == sorted(intensities, reverse=True)
        finally:
            data_utils.states_csv_path = original_default
