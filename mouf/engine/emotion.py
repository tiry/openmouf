"""Emotion engine for the Mouf robot."""

import numpy as np
from numpy.typing import NDArray

from mouf.engine.data_utils import load_states
from shapely.geometry import Point
from shapely.geometry import Polygon


# Type aliases
FloatArray = NDArray[np.float64]
StateDict = dict[str, Polygon]
ActiveState = tuple[str, float]
ActiveStatesList = list[ActiveState]


class MoufEmotionEngine:
    """
    Emotional state engine for the Mouf robot.
    
    Uses a 2D valence-arousal space where the robot's emotional state
    is represented as a point that moves based on impulses and physics.
    """
    
    def __init__(self) -> None:
        """Initialize the emotion engine with default physics parameters."""
        # Physics parameters
        self.pos: FloatArray = np.array([0.0, 0.0])
        self.vel: FloatArray = np.array([0.0, 0.0])
        self.friction: float = 0.95
        self.impulse_scale: float = 0.05
        self.homeostasis: float = 0.0001
        
        # State definitions from CSV
        self.states: StateDict = load_states()

    def apply_impulse(self, dv: float, da: float) -> None:
        """
        Apply an impulse to the emotion state.
        
        Args:
            dv: Change in valence
            da: Change in arousal
        """
        self.vel += np.array([dv, da]) * self.impulse_scale

    def update(self) -> FloatArray:
        """
        Update the emotional state (the 'Tick' function).
        
        Applies physics simulation including:
        - Homeostatic drift toward neutral (0, 0)
        - Velocity and friction
        - Boundary clamping to the unit circle
        
        Returns:
            Current position in valence-arousal space
        """
        self.vel -= self.pos * self.homeostasis
        self.pos += self.vel
        self.vel *= self.friction

        # Boundary clamping to unit circle
        dist = np.linalg.norm(self.pos)
        if dist > 1.0:
            self.pos /= dist
            self.vel *= -0.5 
            
        return self.pos

    def get_active_states(self) -> ActiveStatesList:
        """
        Get the currently active emotional states.
        
        Returns:
            List of (name, intensity) tuples sorted by dominance.
            Intensity is 1.0 at state center, 0.0 at edge.
        """
        p = Point(self.pos)
        active: ActiveStatesList = []
        for name, geom in self.states.items():
            if geom.contains(p):
                # Calculate intensity: 1.0 at center, 0.0 at edge
                dist = p.distance(geom.centroid)
                # We use the 'representative' radius for normalized intensity
                intensity = max(0, 1 - (dist / 0.35)) 
                active.append((name, intensity))
        
        return sorted(active, key=lambda x: x[1], reverse=True)
