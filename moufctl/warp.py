import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_wrapped_spheres(sphere_centers, radius=0.2):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Collect all surface points of all spheres to define the "cloud"
    all_points = []
    u, v = np.mgrid[0:2*np.pi:10j, 0:np.pi:10j]
    
    for center in sphere_centers:
        x = center[0] + radius * np.cos(u) * np.sin(v)
        y = center[1] + radius * np.sin(u) * np.sin(v)
        z = center[2] + radius * np.cos(v)
        
        # Plot individual spheres
        ax.plot_surface(x, y, z, color='r', alpha=0.3, linewidth=0)
        
        # Add these points to our cloud for the hull calculation
        points = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
        all_points.append(points)

    all_points = np.vstack(all_points)

    # 2. Calculate the Convex Hull
    hull = ConvexHull(all_points)

    # 3. Draw the Hull (the wrapper)
    for simplex in hull.simplices:
        # Each simplex is a triangle in 3D
        pts = all_points[simplex]
        triangle = Poly3DCollection([pts])
        triangle.set_alpha(0.2)
        triangle.set_facecolor('cyan')
        triangle.set_edgecolor('blue')
        ax.add_collection3d(triangle)

    # UI Cleanup
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_aspect('equal')
    plt.show()

# Example: 5 spheres in random locations
centers = np.random.uniform(-1, 1, (5, 3))
plot_wrapped_spheres(centers)