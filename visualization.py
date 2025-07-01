import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm

def visualize_rocket(
    nose_type='ogive', Ln=10.0, d=2.0,
    Lt=0.0, dF=2.0, dR=2.0, Xp=10.0,
    N=4, CR=5.0, CT=2.5, S=3.0, XB=15.0, XR=2.5,
    cp_location=18.0):
    """
    Generates and plots a 3D visualization of a rocket, including the nose,
    body, transition, and fins, along with a marker for the Center of Pressure (CP).
    """

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    R = dR / 2.0
    body_end = XB + CR
    
    # Generate the 2D profile of the rocket body
    x_points = []
    y_points = []

    # Nose Cone
    if nose_type.lower() == 'ogive':
        rho = (Ln**2 + (d/2)**2) / (d) # Ogive radius calculation
        nose_x = np.linspace(0, Ln, 50)
        nose_y = np.sqrt(rho**2 - (Ln - nose_x)**2) + (d/2) - rho
    else:  # Conical Nose
        nose_x = np.linspace(0, Ln, 50)
        nose_y = (d / 2) * (nose_x / Ln)

    x_points.extend(nose_x)
    y_points.extend(nose_y)

    # Main Body Tube (pre-transition)
    if Xp > Ln:
        x_points.extend([Ln, Xp])
        y_points.extend([d/2, d/2])
        
    # Transition Section
    if Lt > 0:
        x_points.extend([Xp, Xp + Lt])
        y_points.extend([dF/2, dR/2])

    # Aft Body
    aft_start = Xp + Lt if Lt > 0 else Xp
    x_points.extend([aft_start, body_end])
    y_points.extend([R, R])
    
    # Revolve the 2D profile to create the 3D body
    angles = np.linspace(0, 2 * np.pi, 36)
    X_body = np.outer(x_points, np.ones_like(angles))
    Y_body = np.outer(y_points, np.cos(angles))
    Z_body = np.outer(y_points, np.sin(angles))

    ax.plot_surface(X_body, Y_body, Z_body, color='lightgray', alpha=0.6, edgecolor='k', linewidth=0.5)

    # Define vertices for a single fin at the top of the rocket
    fin_vertices = np.array([
        [XB, R, 0],              # Root leading edge
        [XB + CR, R, 0],         # Root trailing edge
        [XB + XR + CT, R + S, 0],# Tip trailing edge
        [XB + XR, R + S, 0]      # Tip leading edge
    ])

    # Create and plot N fins by rotating the base fin
    for i in range(N):
        angle = i * (2 * np.pi / N)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        
        # Rotation matrix around the x-axis
        rotation_matrix = np.array([
            [1, 0,      0],
            [0, cos_a, -sin_a],
            [0, sin_a,  cos_a]
        ])

        rotated_vertices = np.dot(fin_vertices, rotation_matrix.T)
        
        fin = Poly3DCollection([rotated_vertices], facecolor='darkred', edgecolor='k', alpha=0.8)
        ax.add_collection3d(fin)

    # Plot the Center of Pressure
    ax.scatter([cp_location], [0], [0], color='blue', s=150, label='Center of Pressure (CP)', depthshade=False)

    # Set plot aesthetics
    ax.set_xlabel('X (axial distance from nose tip)')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Rocket Visualization')
    ax.legend()

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.set_axis_off()

    # Set equal aspect ratio for proper scaling
    ax.set_box_aspect([(max(x_points) - min(x_points)), (max(y_points) - min(y_points)), (max(y_points) - min(y_points))])
    
    ax.view_init(elev=20, azim=-60)

    plt.show()
    
    return fig


