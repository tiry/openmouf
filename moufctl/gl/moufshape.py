"""Mouf shape rendering with forward kinematics."""

import numpy as np
from OpenGL.GL import *


class MoufShape:
    """Renders the Mouf robot shape with forward kinematics."""
    
    def __init__(
        self,
        spacing: float,
        radius: float,
        sphere_renderer,
        hull_renderer
    ) -> None:
        self.spacing = spacing
        self.radius = radius
        self.sphere_renderer = sphere_renderer
        self.hull_renderer = hull_renderer
    
    def render(
        self,
        roll: float,
        pitch: float,
        yaw: float,
        show_spheres: bool,
        show_hull: bool,
        colors: list
    ) -> None:
        """
        Render the Mouf shape with given rotations.
        
        Args:
            roll: Roll angle in degrees
            pitch: Pitch angle in degrees
            yaw: Yaw angle in degrees
            show_spheres: Whether to render spheres
            show_hull: Whether to render hull
            colors: List of colors for each segment
        """
        # Forward kinematics
        current_pivot = np.array([-1.5 * self.spacing, 0, 0])
        current_R = np.eye(3)
        all_points = []

        # Get base points for hull
        base_x, base_y, base_z = self.sphere_renderer.get_base_points()

        glPushMatrix()
        glTranslatef(*current_pivot)

        for i in range(4):
            if i == 1:
                glRotatef(roll, 1, 0, 0)
                current_R = current_R @ self._get_rotation_matrix(roll, 0, 0)
            if i == 2:
                glRotatef(pitch, 0, 0, 1)
                current_R = current_R @ self._get_rotation_matrix(0, 0, pitch)
            if i == 3:
                glRotatef(yaw, 0, 1, 0)
                current_R = current_R @ self._get_rotation_matrix(0, yaw, 0)

            # Collect points for hull
            if show_hull:
                transformed_pts = self.hull_renderer.collect_segment_points(
                    base_x, base_y, base_z, current_pivot, current_R
                )
                all_points.append(transformed_pts)

            # Render spheres
            if show_spheres:
                self.sphere_renderer.draw_segment(colors[i])

            # Move pivot
            move_vec = current_R @ np.array([self.spacing, 0, 0])
            current_pivot += move_vec
            glTranslatef(self.spacing, 0, 0)

        glPopMatrix()

        # Render hull
        if show_hull and len(all_points) > 0:
            self.hull_renderer.draw_hull(np.vstack(all_points))
    
    def _get_rotation_matrix(
        self,
        r_deg: float,
        p_deg: float,
        y_deg: float
    ) -> np.ndarray:
        """Get rotation matrix from angles in degrees."""
        r, p, y = np.radians(r_deg), np.radians(p_deg), np.radians(y_deg)
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(r), -np.sin(r)],
            [0, np.sin(r), np.cos(r)]
        ])
        Ry = np.array([
            [np.cos(p), 0, np.sin(p)],
            [0, 1, 0],
            [-np.sin(p), 0, np.cos(p)]
        ])
        Rz = np.array([
            [np.cos(y), -np.sin(y), 0],
            [np.sin(y), np.cos(y), 0],
            [0, 0, 1]
        ])
        
        return Rz @ Ry @ Rx
