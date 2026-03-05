"""Tests for data_utils module."""

import tempfile
from pathlib import Path

import pytest
from shapely.geometry import Point

from mouf.engine import data_utils


class TestLoadStates:
    """Tests for load_states function."""
    
    def test_load_states_from_default_path(self) -> None:
        """Test loading states from default CSV path."""
        # Clear cache to ensure fresh load
        data_utils._states_cache["data"] = None
        
        states = data_utils.load_states()
        
        assert isinstance(states, dict)
        assert len(states) > 0
        # Check that states have the expected names from the CSV
        assert "Zoomies" in states
        assert "Alert" in states
        
    def test_load_states_from_custom_path(self) -> None:
        """Test loading states from custom CSV path."""
        # Clear cache
        data_utils._states_cache["data"] = None
        
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        states = data_utils.load_states(file_path=test_csv)
        
        assert isinstance(states, dict)
        assert len(states) == 4
        assert "Happy" in states
        assert "Sad" in states
        
    def test_load_states_caching(self) -> None:
        """Test that states are cached."""
        # Clear cache first
        data_utils._states_cache["data"] = None
        
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        
        # First load
        states1 = data_utils.load_states(file_path=test_csv)
        
        # Second load should return cached
        states2 = data_utils.load_states(file_path=test_csv)
        
        assert states1 is states2
        
    def test_load_states_refresh(self) -> None:
        """Test force refresh of states."""
        data_utils._states_cache["data"] = None
        
        test_csv = Path(__file__).parent / "data" / "test_states.csv"
        
        states1 = data_utils.load_states(file_path=test_csv)
        states2 = data_utils.load_states(file_path=test_csv, refresh=True)
        
        # With refresh, it should be the same data but reloaded
        assert states1.keys() == states2.keys()
        
    def test_load_states_nonexistent_file(self) -> None:
        """Test loading from nonexistent file returns empty dict."""
        data_utils._states_cache["data"] = None
        
        result = data_utils.load_states(file_path=Path("/nonexistent/file.csv"))
        
        assert result == {}


class TestLoadStimulus:
    """Tests for load_stimulus function."""
    
    def test_load_stimulus_from_default_path(self) -> None:
        """Test loading stimulus from default CSV path."""
        # Clear cache
        data_utils._stimulus_cache["data"] = None
        
        stimulus = data_utils.load_stimulus()
        
        assert isinstance(stimulus, list)
        assert len(stimulus) > 0
        # Check expected stimulus from the CSV
        names = [s[0] for s in stimulus]
        assert "Treat" in names
        assert "Vacuum" in names
        
    def test_load_stimulus_from_custom_path(self) -> None:
        """Test loading stimulus from custom CSV path."""
        # Clear cache
        data_utils._stimulus_cache["data"] = None
        
        test_csv = Path(__file__).parent / "data" / "test_stimulus.csv"
        stimulus = data_utils.load_stimulus(file_path=test_csv)
        
        assert isinstance(stimulus, list)
        assert len(stimulus) == 3
        
        # Check structure
        names = [s[0] for s in stimulus]
        assert "Food" in names
        assert "Scary" in names
        
    def test_load_stimulus_caching(self) -> None:
        """Test that stimulus are cached."""
        data_utils._stimulus_cache["data"] = None
        
        test_csv = Path(__file__).parent / "data" / "test_stimulus.csv"
        
        # First load
        stimulus1 = data_utils.load_stimulus(file_path=test_csv)
        
        # Second load should return cached
        stimulus2 = data_utils.load_stimulus(file_path=test_csv)
        
        assert stimulus1 is stimulus2
        
    def test_load_stimulus_nonexistent_file(self) -> None:
        """Test loading from nonexistent file returns empty list."""
        data_utils._stimulus_cache["data"] = None
        
        result = data_utils.load_stimulus(file_path=Path("/nonexistent/file.csv"))
        
        assert result == []
