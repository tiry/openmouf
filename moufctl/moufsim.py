"""3D Simulation visualization for Mouf robot segments."""

from typing import Callable, Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class FlattenedSphere:
    """A flattened ellipsoid (sphere scaled on Y axis)."""
    
    def __init__(self, radius: float = 1.0, flatten_factor: float = 0.4) -> None:
        """
        Initialize a flattened sphere.
        
        Args:
            radius: Base radius (applies to X and Y axes)
            flatten_factor: Z axis scale (1/4 means Z = radius * 0.4)
        """
        self.radius = radius
        self.flatten_factor = flatten_factor
        
        # Generate sphere mesh - flattened in Z direction
        # Standard sphere parametric equations:
        # x = r * sin(v) * cos(u)
        # y = r * sin(v) * sin(u)  
        # z = r * cos(v)
        u = np.linspace(0, 2 * np.pi, 12)
        v = np.linspace(0, np.pi, 12)
        self.x = radius * np.outer(np.sin(v), np.cos(u))
        self.y = radius * np.outer(np.sin(v), np.sin(u))
        self.z = radius * flatten_factor * np.outer(np.cos(v), np.ones_like(u))
    


class MoufSim3D:
    def __init__(
        self,
        spacing: float = 1.0,
        radius: float = 1.0,
        flatten: float = 0.4,
        show_hull: bool = True  # New boolean flag
    ) -> None:
        self.spacing = spacing
        self.radius = radius
        self.flatten = flatten
        self.show_hull = show_hull # Store the flag
        
        self.spheres = [FlattenedSphere(radius, flatten) for _ in range(4)]
        
        # Setup figure
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_zlim(-1, 1)
        self.ax.set_aspect('equal')

        self.plots = []
        
        # Default rotation logic
        self.roll_func = lambda t: 0.0
        self.pitch_func = lambda t: 0.0
        self.yaw_func = lambda t: 0.0
        self._times = np.linspace(0, 1, 101)

    def _draw_spheres(self, roll: float, pitch: float, yaw: float) -> None:
        """Draw spheres and optionally a convex hull wrapper."""
        for plot in self.plots:
            plot.remove()
        self.plots = []

        def get_r_matrix(r, p, y):
            cr, sr = np.cos(r), np.sin(r)
            cp, sp = np.cos(p), np.sin(p)
            cy, sy = np.cos(y), np.sin(y)
            Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
            Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
            Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
            return Rz @ Ry @ Rx

        local_rots = [
            get_r_matrix(0, 0, 0),      
            get_r_matrix(roll, 0, 0),   
            get_r_matrix(0, pitch, 0),  
            get_r_matrix(0, 0, yaw),    
        ]

        current_pivot = np.array([-2.0 * self.spacing, 0, 0]) 
        current_R = np.eye(3)
        
        # List to collect all points for the hull
        all_points = []

        for i in range(4):
            current_R = current_R @ local_rots[i]
            
            # Pivot offset: Left edge of sphere at (0,0,0)
            mesh_x = self.spheres[i].x + (self.spacing / 2)
            mesh_y = self.spheres[i].y
            mesh_z = self.spheres[i].z
            
            coords = np.vstack([mesh_x.flatten(), mesh_y.flatten(), mesh_z.flatten()])
            rotated_coords = (current_R @ coords).reshape(3, *mesh_x.shape)
            
            x_final = rotated_coords[0] + current_pivot[0]
            y_final = rotated_coords[1] + current_pivot[1]
            z_final = rotated_coords[2] + current_pivot[2]

            # Add these points to our hull cloud
            if self.show_hull:
                sphere_pts = np.vstack([x_final.flatten(), y_final.flatten(), z_final.flatten()]).T
                all_points.append(sphere_pts)

            # Draw the actual spheres (semi-transparent)
            if not self.show_hull: 
                plot = self.ax.plot_surface(x_final, y_final, z_final, 
                                      alpha=0.3, color=plt.cm.cool(i / 3),
                                      antialiased=False)
                self.plots.append(plot)

            # Move pivot for next segment
            joint_vector = current_R @ np.array([self.spacing, 0, 0])
            current_pivot = current_pivot + joint_vector

        # --- HULL LOGIC ---
        if self.show_hull and len(all_points) > 0:
            points_cloud = np.vstack(all_points)
            hull = ConvexHull(points_cloud)
            
            # Create triangles for the hull surface
            for simplex in hull.simplices:
                pts = points_cloud[simplex]
                # Using Poly3DCollection for better performance in animations
                poly = Poly3DCollection([pts], alpha=0.3, facecolor='grey', edgecolor='darkgrey')
                self.ax.add_collection3d(poly)
                self.plots.append(poly)


    def _rotate_around_point(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        roll: float,
        pitch: float,
        yaw: float,
        center: float
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Rotate mesh around a specific X-axis center point."""
        # Translate to origin
        x_centered = x + center
        
        # Rotation matrices
        cos_r, sin_r = np.cos(roll), np.sin(roll)
        cos_p, sin_p = np.cos(pitch), np.sin(pitch)
        cos_y, sin_y = np.cos(yaw), np.sin(yaw)
        
        # Roll (X rotation)
        Rx = np.array([
            [1.0, 0.0, 0.0],
            [0.0, cos_r, -sin_r],
            [0.0, sin_r, cos_r]
        ])
        
        # Pitch (Y rotation)
        Ry = np.array([
            [cos_p, 0.0, sin_p],
            [0.0, 1.0, 0.0],
            [-sin_p, 0.0, cos_p]
        ])
        
        # Yaw (Z rotation)
        Rz = np.array([
            [cos_y, -sin_y, 0.0],
            [sin_y, cos_y, 0.0],
            [0.0, 0.0, 1.0]
        ])
        
        # Combined rotation
        R = Rz @ Ry @ Rx
        
        # Apply to all points
        coords = np.vstack([x_centered.flatten(), y.flatten(), z.flatten()])
        rotated = (R @ coords).reshape(3, *x.shape)
        
        return rotated[0], rotated[1], rotated[2]

    def set_rotation_functions(
        self,
        roll_func: Optional[Callable[[float], float]] = None,
        pitch_func: Optional[Callable[[float], float]] = None,
        yaw_func: Optional[Callable[[float], float]] = None
    ) -> None:
        """
        Set functions that define how rotations evolve with time.
        
        Each function takes time t (0 to 1) and returns angle in radians.
        
        Args:
            roll_func: Function for roll angle evolution
            pitch_func: Function for pitch angle evolution
            yaw_func: Function for yaw angle evolution
        """
        self.roll_func = roll_func if roll_func is not None else lambda t: 0.0
        self.pitch_func = pitch_func if pitch_func is not None else lambda t: 0.0
        self.yaw_func = yaw_func if yaw_func is not None else lambda t: 0.0
        
        # Pre-compute values for smooth animation
        self._roll_vals = np.array([self.roll_func(t) for t in self._times])
        self._pitch_vals = np.array([self.pitch_func(t) for t in self._times])
        self._yaw_vals = np.array([self.yaw_func(t) for t in self._times])

    def set_rotation_arrays(
        self,
        times: np.ndarray,
        roll: Optional[np.ndarray] = None,
        pitch: Optional[np.ndarray] = None,
        yaw: Optional[np.ndarray] = None
    ) -> None:
        """
        Set rotation arrays for time-based animation.
        
        Args:
            times: Array of time values (0 to 1)
            roll: Array of roll angles in radians
            pitch: Array of pitch angles in radians
            yaw: Array of yaw angles in radians
        """
        self._times = times
        
        # Default to zeros if not provided
        self._roll_vals = roll if roll is not None else np.zeros_like(times)
        self._pitch_vals = pitch if pitch is not None else np.zeros_like(times)
        self._yaw_vals = yaw if yaw is not None else np.zeros_like(times)
        
        # Create interpolation functions using numpy
        self.roll_func = lambda t: float(np.interp(t, times, self._roll_vals))
        self.pitch_func = lambda t: float(np.interp(t, times, self._pitch_vals))
        self.yaw_func = lambda t: float(np.interp(t, times, self._yaw_vals))

    def update(self, frame: int) -> None:
        """Update animation frame."""
        # Get time from 0 to 1 (100 frames = 0 to 1)
        t = frame / 100.0
        
        # Get current rotations
        roll = self.roll_func(t)
        pitch = self.pitch_func(t)
        yaw = self.yaw_func(t)
        
        # Redraw spheres
        self._draw_spheres(roll, pitch, yaw)

    def animate(self, frames: int = 100, interval: int = 50) -> None:
        """
        Run the animation.
        
        Args:
            frames: Number of animation frames
            interval: Delay between frames in ms
        """
        self.ani = FuncAnimation(
            self.fig, 
            self.update,
            frames=frames,
            interval=interval,
            blit=False
        )
        plt.show()


def demo() -> None:
    """Run a demo animation with sinusoidal rotations."""
    sim = MoufSim3D(spacing=0.5, radius=1.0, flatten=0.5, show_hull=True)
    
    # Set rotation functions using lambdas
    roll = lambda t: np.sin(t * 2 * np.pi) * 0.2   # One cycle, ±0.5 rad
    pitch = lambda t: np.sin(t * 2 * np.pi) * 0.8  # One cycle, ±0.3 rad
    yaw = lambda t: np.sin(t * 4 * np.pi) * 1   # Two cycles, ±0.4 rad
    
    sim.set_rotation_functions(roll, pitch, yaw)
    sim.animate()


if __name__ == "__main__":
    demo()