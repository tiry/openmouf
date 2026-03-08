"""Mouf 3D simulation using OpenGL."""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from moufctl.gl import SphereRenderer, HullRenderer, Viewer, MoufShape


def default_servo_positions(t: float) -> tuple[float, float, float]:
    """
    Default servo position calculation.
    
    Args:
        t: Time value
        
    Returns:
        Tuple of (roll, pitch, yaw) in degrees
    """
    roll = np.degrees(np.sin(t*0.1) * 0.2)
    pitch = abs(np.degrees(np.cos(t * 0.3) * 0.5))
    yaw = np.degrees(np.sin(t * 0.5) * 0.4)
    return roll, pitch, yaw


class MoufSimOpenGL:
    # Class-level registry for servo position functions
    _servo_position_func = default_servo_positions
    
    @classmethod
    def register_servo_positions(cls, func):
        """Register a custom servo position function."""
        cls._servo_position_func = func
        return func
    
    @classmethod
    def get_servo_positions(cls, t: float) -> tuple[float, float, float]:
        """Get servo positions using registered function."""
        return cls._servo_position_func(t)
    def __init__(self, spacing=0.8, radius=1, flatten=0.5, show_spheres=False, show_hull=True):
        self.spacing = spacing
        self.radius = radius
        self.flatten = flatten
        self.show_spheres = show_spheres
        self.show_hull = show_hull
        
        # Initialize components
        self.sphere_renderer = SphereRenderer(radius, flatten)
        self.hull_renderer = HullRenderer()
        self.viewer = Viewer()
        self.mouf_shape = MoufShape(spacing, radius, self.sphere_renderer, self.hull_renderer)
        
        self.colors = [(0.2, 0.6, 1.0), (0.2, 0.9, 0.6), (0.9, 0.8, 0.2), (1.0, 0.4, 0.4)]
        
        pygame.init()
        self.display = (1200, 800)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        
        # OpenGL Setup
        self.viewer.setup_camera(self.display)
        
        # Material settings for hull
        if show_hull and not show_spheres:
            glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    def run(self):
        clock = pygame.time.Clock()
        t = 0

        while True:
            if not self.viewer.handle_input(pygame.event.get()): break
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0, 0, self.viewer.distance)
            glRotatef(self.viewer.angle_x, 1, 0, 0)
            glRotatef(self.viewer.angle_y, 0, 1, 0)
            self.viewer.draw_grid()

            # Animation
            t += 0.03
            roll, pitch, yaw = self.get_servo_positions(t)

            # Render Mouf shape
            self.mouf_shape.render(
                roll, pitch, yaw,
                self.show_spheres,
                self.show_hull,
                self.colors
            )
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Mouf 3D OpenGL Simulation")
    parser.add_argument("--sphere", action="store_true", help="Show spheres")
    parser.add_argument("--hull", action="store_true", help="Show hull")
    args = parser.parse_args()
    
    if not args.sphere and not args.hull:
        parser.print_help()
    else:
        MoufSimOpenGL(show_spheres=args.sphere, show_hull=args.hull).run()
