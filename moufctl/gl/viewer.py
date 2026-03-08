"""OpenGL viewer utilities."""

import numpy as np
from OpenGL.GL import *


class Viewer:
    """OpenGL viewer with camera controls and grid."""
    
    def __init__(self) -> None:
        """Initialize the viewer."""
        self.angle_x: float = 20.0
        self.angle_y: float = 45.0
        self.distance: float = -12.0
        self.mouse_down: bool = False
    
    def draw_grid(self) -> None:
        """Draw a ground grid."""
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2)
        for i in range(-10, 11):
            glVertex3f(i, -2, -10)
            glVertex3f(i, -2, 10)
            glVertex3f(-10, -2, i)
            glVertex3f(10, -2, i)
        glEnd()
        glEnable(GL_LIGHTING)
    
    def handle_input(self, events) -> bool:
        """
        Handle pygame input events.
        
        Args:
            events: pygame event list
            
        Returns:
            True if should continue, False to quit
        """
        import pygame
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                if event.button == 4:  # Scroll up
                    self.distance += 0.5
                if event.button == 5:  # Scroll down
                    self.distance -= 0.5
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            if event.type == pygame.MOUSEMOTION and self.mouse_down:
                self.angle_y += event.rel[0] * 0.5
                self.angle_x += event.rel[1] * 0.5
        return True
    
    def setup_camera(self, display: tuple[int, int], distance: float = -12.0) -> None:
        """
        Setup OpenGL camera.
        
        Args:
            display: (width, height) tuple
            distance: Camera distance
        """
        self.distance = distance
        
        from OpenGL.GLU import gluPerspective, gluLookAt
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 10, 1))

        glDisable(GL_CULL_FACE)  # Draw both sides of the triangles
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) # Light both sides
    
    def get_rotation_matrix(self, r_deg: float, p_deg: float, y_deg: float) -> np.ndarray:
        """
        Get combined rotation matrix from roll, pitch, yaw in degrees.
        
        Args:
            r_deg: Roll in degrees
            p_deg: Pitch in degrees
            y_deg: Yaw in degrees
            
        Returns:
            3x3 rotation matrix
        """
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
