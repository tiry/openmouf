"""Convex hull generation for robot segments."""

import numpy as np
from scipy.spatial import ConvexHull


class HullRenderer:
    """Generates and renders convex hulls around robot segments."""
    
    def __init__(self) -> None:
        """Initialize the hull renderer."""
        pass
    
    def draw_hull(self, points: np.ndarray) -> None:
        """
        Draw a convex hull around the given points.
        
        Args:
            points: Nx3 array of 3D points
        """
        from OpenGL.GL import glBegin, glColor4f, glDisable, glEnable, glEnd
        from OpenGL.GL import glVertex3f, glNormal3f, glLineWidth, glBegin
        from OpenGL.GL import GL_TRIANGLES, GL_LINES, GL_LIGHTING, GL_LINES
        
        try:
            hull = ConvexHull(points)
            
            # Draw triangles for the skin
            glEnable(GL_LIGHTING)
            glBegin(GL_TRIANGLES)
            glColor4f(0.7, 0.7, 0.7, 1)  # Slightly more opaque
            
            for simplex in hull.simplices:
                # Calculate face normal for stable lighting
                p1, p2, p3 = points[simplex]
                v1 = p2 - p1
                v2 = p3 - p1
                normal = np.cross(v1, v2)
                norm = np.linalg.norm(normal)
                if norm > 0:
                    glNormal3f(*(normal / norm))
                
                # Draw vertices
                for vertex in simplex:
                    glVertex3f(*points[vertex])
            glEnd()
            
            # Draw wireframe for definition
            glDisable(GL_LIGHTING)
            glLineWidth(1.0)
            glBegin(GL_LINES)
            glColor4f(0.4, 0.4, 0.4, 0.2)
            for simplex in hull.simplices:
                for i in range(3):
                    glVertex3f(*points[simplex[i]])
                    glVertex3f(*points[simplex[(i + 1) % 3]])
            glEnd()
            glEnable(GL_LIGHTING)
            
        except Exception:
            # ConvexHull can fail if points are co-planar (rare in 3D)
            pass
    
    def collect_segment_points(
        self,
        base_x: np.ndarray,
        base_y: np.ndarray,
        base_z: np.ndarray,
        current_pivot: np.ndarray,
        current_R: np.ndarray
    ) -> np.ndarray:
        """
        Transform base sphere points to world coordinates.
        
        Args:
            base_x, base_y, base_z: Base mesh coordinates
            current_pivot: Current pivot position
            current_R: Current rotation matrix
            
        Returns:
            Transformed points array
        """
        pts = np.vstack([
            base_x.flatten(), 
            base_y.flatten(), 
            base_z.flatten()
        ])
        transformed_pts = (current_R @ pts).T + current_pivot
        return transformed_pts
