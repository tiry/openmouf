"""Data loading utilities for emotional states and stimuli from CSV files."""

import csv
from pathlib import Path
from typing import Any

from shapely.geometry import Point
from shapely.geometry import Polygon


# Type aliases
StatesDict = dict[str, Polygon]
StimulusList = list[tuple[str, list[float]]]
OptionalPath = Path | None

current_dir = Path(__file__).parent
states_csv_path: Path = current_dir.parent / "data" / "states.csv"
stimulus_csv_path: Path = current_dir.parent / "data" / "stimulus.csv"


# Internal module caches
_states_cache: dict[str, Any] = {
    "data": None,
    "source_file": None
}

_stimulus_cache: dict[str, Any] = {
    "data": None,
    "source_file": None
}


def load_states(file_path: OptionalPath = None, refresh: bool = False) -> StatesDict:
    """
    Reads emotional states from a CSV file and returns a dictionary of Shapely Polygons.
    
    The CSV should have columns: name, v, a, radius.
    Each state is represented as a buffered point (disc) for containment checks.
    
    Args:
        file_path: Optional path to the states CSV file. 
                   Defaults to mouf/data/states.csv.
        refresh: If True, forces reload from file even if cached.
    
    Returns:
        Dictionary mapping state names to Shapely Polygon objects.
    """
    global _states_cache
    
    # Use default path if not provided
    if file_path is None:
        file_path = states_csv_path
    
    # Return cache if available and refresh is not requested
    if _states_cache["data"] is not None and not refresh and _states_cache["source_file"] == file_path:
        return _states_cache["data"]

    new_states: StatesDict = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name'].strip()
                v = float(row['v'])
                a = float(row['a'])
                r = float(row['radius'])
                
                # We store the buffered polygon (the disc) for containment checks
                new_states[name] = Point(v, a).buffer(r)
        
        # Update cache
        _states_cache["data"] = new_states
        _states_cache["source_file"] = file_path
        print(f"Successfully loaded {len(new_states)} states from {file_path}")
        
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Returning empty state dictionary.")
        return {}
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return {}

    return _states_cache["data"]


def load_stimulus(file_path: OptionalPath = None, refresh: bool = False) -> StimulusList:
    """
    Reads stimulus definitions from a CSV file and returns a list of (name, [v, a]) tuples.
    
    The CSV should have columns: name, v, a.
    Each stimulus has a name and a 2D vector [valence, arousal].
    
    Args:
        file_path: Optional path to the stimulus CSV file.
                   Defaults to mouf/data/stimulus.csv.
        refresh: If True, forces reload from file even if cached.
    
    Returns:
        List of tuples containing (stimulus_name, [valence, arousal]).
    """
    global _stimulus_cache
    
    # Use default path if not provided
    if file_path is None:
        file_path = stimulus_csv_path
    
    # Return cache if available and refresh is not requested
    if _stimulus_cache["data"] is not None and not refresh and _stimulus_cache["source_file"] == file_path:
        return _stimulus_cache["data"]

    stimulus_list: StimulusList = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name'].strip()
                v = float(row['v'])
                a = float(row['a'])
                stimulus_list.append((name, [v, a]))
        
        # Update cache
        _stimulus_cache["data"] = stimulus_list
        _stimulus_cache["source_file"] = file_path
        print(f"Successfully loaded {len(stimulus_list)} stimulus definitions from {file_path}")
        
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Returning empty stimulus list.")
        return []
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return []

    return _stimulus_cache["data"]
