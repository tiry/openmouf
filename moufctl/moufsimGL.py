import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class MoufSimOpenGL:
    def __init__(self, spacing=0.8, radius=1, flatten=0.5):
        self.spacing = spacing
        self.radius = radius
        self.flatten = flatten
        
        # Camera State
        self.angle_x = 20.0
        self.angle_y = 45.0
        self.distance = -12.0
        self.mouse_down = False
        
        pygame.init()
        self.display = (1200, 800)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Mouf 3D - GPU Accelerated")

        # Initial Projection
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Hardware acceleration settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Light Setup
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 10, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))

    def draw_segment(self, color):
        """Draws a sphere centered on its pivot point, flattened vertically."""
        glColor3f(*color)
        glPushMatrix()
        
        # 1. Move the sphere so its left edge is at the joint origin
        # (This remains on X-axis)
        glTranslatef(self.radius, 0, 0)
        
        # 2. Apply the flattening to the UP axis (Y)
        glScalef(1.0, self.flatten, 1.0)
        
        # 3. Create and draw the quadric
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius, 32, 32)
        
        glPopMatrix()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.mouse_down = True
                if event.button == 4: self.distance += 0.5 # Scroll Up
                if event.button == 5: self.distance -= 0.5 # Scroll Down
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.mouse_down = False
            if event.type == pygame.MOUSEMOTION and self.mouse_down:
                dx, dy = event.rel
                self.angle_y += dx * 0.5
                self.angle_x += dy * 0.5
        return True

    def run(self):
        clock = pygame.time.Clock()
        t = 0
        colors = [(0.2, 0.6, 1.0), (0.2, 0.9, 0.6), (0.9, 0.8, 0.2), (1.0, 0.4, 0.4)]

        while True:
            if not self.handle_input(): break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            
            # Global Camera Transform
            glTranslatef(0, 0, self.distance)
            glRotatef(self.angle_x, 1, 0, 0)
            glRotatef(self.angle_y, 0, 1, 0)

            # Draw Ground Grid
            self.draw_grid()

            # Animation State (Radians -> Degrees for OpenGL)
            t += 0.03
            roll  = np.degrees(np.sin(t) * 0.5)
            pitch = 0*np.degrees(np.cos(t * 0.7) * 0.6)
            yaw   = 0*np.degrees(np.sin(t * 1.2) * 0.4)

            # --- CHAINED FORWARD KINEMATICS ---
            glPushMatrix()
            # Start at the far left
            glTranslatef(-1.5 * self.spacing, 0, 0)

            for i in range(4):
                # 1. Apply Rotation to this joint (affects this and all following)
                if i == 1: glRotatef(roll, 1, 0, 0)
                if i == 2: glRotatef(pitch, 0, 1, 0)
                if i == 3: glRotatef(yaw, 0, 0, 1)

                # 2. Draw the segment at current transformed origin
                self.draw_segment(colors[i])

                # 3. Translate to the end of this segment for the next joint
                glTranslatef(self.spacing, 0, 0)

            glPopMatrix()
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2)
        for i in range(-10, 11):
            glVertex3f(i, -2, -10); glVertex3f(i, -2, 10)
            glVertex3f(-10, -2, i); glVertex3f(10, -2, i)
        glEnd()
        glEnable(GL_LIGHTING)

if __name__ == "__main__":
    MoufSimOpenGL().run()