import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import simpson

def compute_custom_fairing_cop(profile_points):
    """
    Compute the aerodynamic center of pressure (CoP) and normal force coefficient
    slope (Cn) for a custom fairing shape using slender body theory.
    
    Args:
        profile_points: List of (x, y) tuples describing the fairing profile.
                        x is axial position, y is radius at that position.
    Returns:
        x_cp: Center of pressure (float)
        Cn: Normal force coefficient slope (float, unscaled)
    """
    # Sort points to ensure x is increasing
    profile_points = sorted(profile_points)
    x_vals, y_vals = zip(*profile_points)
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)

    # Interpolate y(x) to get smooth function
    y_interp = interp1d(x_vals, y_vals, kind='cubic', fill_value="extrapolate")

    # Resample finely for better numerical stability
    x_fine = np.linspace(x_vals[0], x_vals[-1], 500)
    y_fine = y_interp(x_fine)

    # Compute cross-sectional area: S(x) = pi * y^2
    S = np.pi * y_fine**2

    # Compute dS/dx using numerical derivative
    dS_dx = np.gradient(S, x_fine)

    # Slender body theory: CoP is the area-weighted x-location
    numerator = simpson((dS_dx**2) * x_fine, x=x_fine)
    denominator = simpson(dS_dx**2, x=x_fine)
    x_cp = numerator / denominator if denominator != 0 else np.mean(x_fine)

    # Optional: Return Cn (unscaled here, for relative contribution)
    Cn = denominator  # The integral of (dS/dx)^2, proportional to force slope

    return x_cp, Cn 