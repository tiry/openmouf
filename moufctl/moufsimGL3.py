import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial import ConvexHull

class MoufSimOpenGL:
    def __init__(self, spacing=0.8, radius=1, flatten=0.5, show_spheres=False, show_hull=True):
        self.spacing = spacing
        self.radius = radius
        self.flatten = flatten
        self.show_spheres = show_spheres
        self.show_hull = show_hull
        
        # Camera & UI
        self.angle_x, self.angle_y = 20.0, 45.0
        self.distance = -12.0
        self.mouse_down = False
        
        pygame.init()
        self.display = (1200, 800)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        
        # OpenGL Setup
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND) # For transparent skin
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 10, 1))

        # settings for hull
        glDisable(GL_CULL_FACE)  # Draw both sides of the triangles
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) # Light both sides


        # Pre-generate low-res sphere points for Hull calculation
        # (10x10 is very fast for scipy)
        u = np.linspace(0, 2 * np.pi, 16)
        v = np.linspace(0, np.pi, 16)
        self.base_x = self.radius * np.outer(np.cos(u), np.sin(v))
        self.base_y = self.radius * np.outer(np.sin(u), np.sin(v)) * self.flatten
        self.base_z = self.radius * np.outer(np.ones_like(u), np.cos(v))
        
        # Offset the base points so pivot is at (0,0,0) like in the draw call
        self.base_x += self.radius

    def get_rotation_matrix(self, r_deg, p_deg, y_deg):
        r, p, y = np.radians(r_deg), np.radians(p_deg), np.radians(y_deg)
        Rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
        Ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
        Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
        return Rz @ Ry @ Rx

    def run(self):
        clock = pygame.time.Clock()
        t = 0
        colors = [(0.2, 0.6, 1.0), (0.2, 0.9, 0.6), (0.9, 0.8, 0.2), (1.0, 0.4, 0.4)]

        while True:
            if not self.handle_input(): break
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0, 0, self.distance)
            glRotatef(self.angle_x, 1, 0, 0)
            glRotatef(self.angle_y, 0, 1, 0)
            self.draw_grid()

            # Animation
            t += 0.03
            roll  = np.degrees(np.sin(t) * 0.5)
            pitch = np.degrees(np.cos(t * 0.7) * 0.6)
            yaw   = np.degrees(np.sin(t * 1.2) * 0.4)

            # --- FORWARD KINEMATICS & POINT COLLECTION ---
            current_pivot = np.array([-1.5 * self.spacing, 0, 0])
            current_R = np.eye(3)
            all_points = []

            # We'll use OpenGL for rendering and NumPy for Hull calculation
            glPushMatrix()
            glTranslatef(*current_pivot)

            for i in range(4):
                if i == 1: glRotatef(roll, 1, 0, 0); current_R = current_R @ self.get_rotation_matrix(roll, 0, 0)
                if i == 2: glRotatef(pitch, 0, 1, 0); current_R = current_R @ self.get_rotation_matrix(0, pitch, 0)
                if i == 3: glRotatef(yaw, 0, 0, 1); current_R = current_R @ self.get_rotation_matrix(0, 0, yaw)

                # Collect Points for Hull
                if self.show_hull:
                    pts = np.vstack([self.base_x.flatten(), self.base_y.flatten(), self.base_z.flatten()])
                    transformed_pts = (current_R @ pts).T + current_pivot
                    all_points.append(transformed_pts)

                # Render Spheres (Optional)
                if self.show_spheres:
                    self.draw_segment_gl(colors[i])

                # Move current pivot for math and OpenGL
                move_vec = current_R @ np.array([self.spacing, 0, 0])
                current_pivot += move_vec
                glTranslatef(self.spacing, 0, 0)

            glPopMatrix()

            # --- RENDER HULL ---
            if self.show_hull and len(all_points) > 0:
                # Add microscopic jitter to prevent degenerate coplanar triangles
                #jitter = np.random.normal(0, 0.0001, (len(all_points),len(all_points[0]),3, ))
                #print(f"all_points={all_points}")
                #print(f"jitter={jitter}")
                #all_points += jitter
                self.draw_hull(np.vstack(all_points))
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def draw_segment_gl(self, color):
        glColor4f(color[0], color[1], color[2], 0.4)
        glPushMatrix()
        glTranslatef(self.radius, 0, 0)
        glScalef(1.0, self.flatten, 1.0)
        quad = gluNewQuadric()
        gluSphere(quad, self.radius, 16, 16)
        glPopMatrix()

    def draw_hull(self, points):
        try:
            hull = ConvexHull(points)
            
            # We use GL_TRIANGLES for the skin
            glEnable(GL_LIGHTING)
            glBegin(GL_TRIANGLES)
            glColor4f(0.7, 0.7, 0.7, 1) # Slightly more opaque for visibility
            
            for simplex in hull.simplices:
                # 1. Calculate the Face Normal (for stable lighting)
                # This prevents the 'flickering' look by giving OpenGL a 
                # consistent direction for light to bounce off.
                p1, p2, p3 = points[simplex]
                v1 = p2 - p1
                v2 = p3 - p1
                normal = np.cross(v1, v2)
                norm = np.linalg.norm(normal)
                if norm > 0:
                    glNormal3f(*(normal / norm))
                
                # 2. Draw the vertices
                for vertex in simplex:
                    glVertex3f(*points[vertex])
            glEnd()
            
            # 3. Draw a slightly darker wireframe to define the shape
            glDisable(GL_LIGHTING)
            glLineWidth(1.0)
            glBegin(GL_LINES)
            glColor4f(0.4, 0.4, 0.4, 0.2)
            for simplex in hull.simplices:
                for i in range(3):
                    glVertex3f(*points[simplex[i]])
                    glVertex3f(*points[simplex[(i+1)%3]])
            glEnd()
            glEnable(GL_LIGHTING)
            
        except Exception:
            # ConvexHull can fail if points are co-planar (rare in 3D)
            pass

    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES); glColor3f(0.2, 0.2, 0.2)
        for i in range(-10, 11):
            glVertex3f(i, -2, -10); glVertex3f(i, -2, 10)
            glVertex3f(-10, -2, i); glVertex3f(10, -2, i)
        glEnd(); glEnable(GL_LIGHTING)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.mouse_down = True
                if event.button == 4: self.distance += 0.5
                if event.button == 5: self.distance -= 0.5
            if event.type == pygame.MOUSEBUTTONUP: self.mouse_down = False
            if event.type == pygame.MOUSEMOTION and self.mouse_down:
                self.angle_y += event.rel[0] * 0.5
                self.angle_x += event.rel[1] * 0.5
        return True

if __name__ == "__main__":
    # You can toggle show_spheres=True to see the "skeleton" inside the skin
    MoufSimOpenGL(show_spheres=False, show_hull=True).run()