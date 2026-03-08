"""OpenGL sphere rendering with textures."""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *


class SphereRenderer:
    """Renders flattened spheres with checkerboard textures."""
    
    def __init__(self, radius: float = 1.0, flatten: float = 0.5) -> None:
        """
        Initialize the sphere renderer.
        
        Args:
            radius: Sphere radius
            flatten: Flatten factor for Z-axis (0.5 = half height)
        """
        self.radius = radius
        self.flatten = flatten
        self.tex_id: int = 0
        self._setup_texture()
    
    def _setup_texture(self) -> None:
        """Create checkerboard texture."""
        # 2x2 checkerboard pattern (Black and White)
        check_data = np.array([
            [0, 0, 0, 255, 255, 255],
            [255, 255, 255, 0, 0, 0]
        ], dtype=np.uint8)
        
        self.tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        
        # Texture wrapping and filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        # Upload to GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_UNSIGNED_BYTE, check_data)
    
    def draw_segment(self, color: tuple[float, float, float]) -> None:
        """
        Draw a single flattened sphere segment.
        
        Args:
            color: RGB color tuple
        """
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        
        # GL_MODULATE multiplies the white squares by the color parameter
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glColor3f(*color)
        
        glPushMatrix()
        glTranslatef(self.radius, 0, 0)
        glScalef(1.0, self.flatten, 1.0)
        
        # Rotate sphere so poles aren't visible from the side
        glRotatef(90, 1, 0, 0)
        
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluQuadricNormals(quad, GLU_SMOOTH)
        
        # Scale texture coordinates for more squares
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glScalef(10.0, 5.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        
        gluSphere(quad, self.radius, 32, 32)
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
    
    def get_base_points(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get base sphere points for hull calculation.
        
        Returns:
            Tuple of (x, y, z) mesh arrays
        """
        # Low-res sphere for fast hull calculation
        u = np.linspace(0, 2 * np.pi, 16)
        v = np.linspace(0, np.pi, 16)
        
        base_x = self.radius * np.outer(np.cos(u), np.sin(v))
        base_y = self.radius * np.outer(np.sin(u), np.sin(v)) * self.flatten
        base_z = self.radius * np.outer(np.ones_like(u), np.cos(v))
        
        # Offset so pivot is at (0,0,0)
        base_x += self.radius
        
        return base_x, base_y, base_z
