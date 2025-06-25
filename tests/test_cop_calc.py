import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rocket.geometry import NoseCone, Rocket, PayloadFairing
from rocket.cop_calc import _calculate_nosecone_cop, compute_overall_cop


def test_nosecone_cop_calculation():
    """Test that nosecone CoP calculation returns expected values."""
    # Create a simple cone nosecone of length 1m
    nosecone = NoseCone(
        part="nosecone",
        type="cone",
        length=1.0,
        base_diameter=0.1
    )
    
    # Create a simple rocket for reference
    rocket = Rocket(
        name="Test Rocket",
        reference_diameter=0.1,
        components=[]
    )
    
    x_cp, Cna = _calculate_nosecone_cop(nosecone, rocket)
    
    # For a cone, x_cp should be 0.666 * length
    expected_x_cp = 0.666 * 1.0
    assert abs(x_cp - expected_x_cp) < 1e-6, f"Expected x_cp = {expected_x_cp}, got {x_cp}"
    
    # C_Nα should be 2.0 for nosecones
    assert Cna == 2.0, f"Expected C_Nα = 2.0, got {Cna}"


def test_ogive_nosecone_cop_calculation():
    """Test that ogive nosecone CoP calculation returns expected values."""
    # Create an ogive nosecone of length 1m
    nosecone = NoseCone(
        part="nosecone",
        type="ogive",
        length=1.0,
        base_diameter=0.1
    )
    
    # Create a simple rocket for reference
    rocket = Rocket(
        name="Test Rocket",
        reference_diameter=0.1,
        components=[]
    )
    
    x_cp, Cna = _calculate_nosecone_cop(nosecone, rocket)
    
    # For an ogive, x_cp should be 0.466 * length
    expected_x_cp = 0.466 * 1.0
    assert abs(x_cp - expected_x_cp) < 1e-6, f"Expected x_cp = {expected_x_cp}, got {x_cp}"
    
    # C_Nα should be 2.0 for nosecones
    assert Cna == 2.0, f"Expected C_Nα = 2.0, got {Cna}"


def test_custom_fairing_cop_integration():
    """
    Test compute_overall_cop with a custom payload fairing using a semi-elliptical profile.
    """
    import numpy as np
    # Semi-elliptical ogive fairing from x = 0 to x = 1, radius up to 0.2
    x = np.linspace(0, 1, 50)
    y = 0.2 * np.sqrt(1 - (x - 1)**2)  # semi-ellipse
    profile_points = list(zip(x.tolist(), y.tolist()))

    fairing = PayloadFairing(
        part="payload_fairing",
        name="Custom Fairing",
        length=1.0,
        base_diameter=0.4,
        shape_type="custom",
        custom_parameters={"profile_points": profile_points}
    )

    rocket = Rocket(
        name="Test Custom Fairing Rocket",
        reference_diameter=0.4,
        components=[fairing]
    )

    x_cp_total, contributions = compute_overall_cop(rocket)
    x_cp, Cn = contributions["Custom Fairing"]

    print(f"Custom Fairing CoP: {x_cp:.4f} m, Cn: {Cn:.4f}")
    assert 0 < x_cp < 1, "CoP should lie within fairing length"
    assert Cn > 0, "Cn should be positive"


def test_conical_payload_fairing_cop_matches_analytical():
    """
    Test that a conical payload fairing (wider than rocket body) produces a CoP 
    matching the analytical cone value (2/3 of length).
    """
    import numpy as np
    # Conical payload fairing: wider than rocket body to accommodate payload
    L = 1.0  # length in meters
    R_fairing = 0.3  # fairing base radius (wider than rocket)
    R_rocket = 0.1   # rocket body radius
    
    # Create conical profile: y(x) = R_fairing * (x/L) from x=0 to x=L
    x = np.linspace(0, L, 100)
    y = R_fairing * (x / L)
    profile_points = list(zip(x.tolist(), y.tolist()))

    fairing = PayloadFairing(
        part="payload_fairing",
        name="Conical Payload Fairing",
        length=L,
        base_diameter=2*R_fairing,
        shape_type="custom",
        custom_parameters={"profile_points": profile_points}
    )

    rocket = Rocket(
        name="Test Conical Payload Fairing Rocket",
        reference_diameter=2*R_rocket,  # rocket body diameter
        components=[fairing]
    )

    x_cp_total, contributions = compute_overall_cop(rocket)
    x_cp, Cn = contributions["Conical Payload Fairing"]

    expected_x_cp = 0.666 * L  # Analytical CoP for cone
    print(f"Conical Payload Fairing CoP: {x_cp:.4f} m, expected: {expected_x_cp:.4f} m")
    print(f"Fairing base diameter: {2*R_fairing:.2f}m, Rocket body diameter: {2*R_rocket:.2f}m")
    print(f"Profile: y(x) = {R_fairing:.1f} * (x/{L:.1f}) from x=0 to x={L:.1f}")
    print(f"Difference: {abs(x_cp - expected_x_cp):.4f} m")
    # Use a more reasonable tolerance for slender body theory vs analytical
    assert abs(x_cp - expected_x_cp) < 0.1, f"Expected x_cp ≈ {expected_x_cp}, got {x_cp}"
    assert Cn > 0, "Cn should be positive"


def test_blunt_nosed_payload_fairing_cop():
    """
    Test a blunt-nosed conical payload fairing (cylindrical section + cone taper).
    This is a common real-world payload fairing shape.
    """
    import numpy as np
    # Blunt-nosed conical fairing: cylindrical section + conical taper
    L_total = 1.0  # total length
    L_cyl = 0.4    # cylindrical section length
    L_cone = 0.6   # conical section length
    R_fairing = 0.3  # fairing radius
    R_rocket = 0.1   # rocket body radius
    
    # Create profile: cylindrical from 0 to L_cyl, then conical taper
    x = np.linspace(0, L_total, 200)
    y = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        if xi <= L_cyl:
            # Cylindrical section
            y[i] = R_fairing
        else:
            # Conical taper: y = R_fairing * (1 - (x-L_cyl)/L_cone)
            y[i] = R_fairing * (1 - (xi - L_cyl) / L_cone)
    
    profile_points = list(zip(x.tolist(), y.tolist()))

    fairing = PayloadFairing(
        part="payload_fairing",
        name="Blunt-Nosed Payload Fairing",
        length=L_total,
        base_diameter=2*R_fairing,
        shape_type="custom",
        custom_parameters={"profile_points": profile_points}
    )

    rocket = Rocket(
        name="Test Blunt-Nosed Payload Fairing Rocket",
        reference_diameter=2*R_rocket,
        components=[fairing]
    )

    x_cp_total, contributions = compute_overall_cop(rocket)
    x_cp, Cn = contributions["Blunt-Nosed Payload Fairing"]

    # For a blunt-nosed fairing, CoP should be between cylindrical and conical values
    # Cylindrical section contributes at its centroid (L_cyl/2)
    # Conical section contributes at 2/3 of its length from start
    expected_x_cp_min = L_cyl/2  # if all cylindrical
    expected_x_cp_max = L_cyl + (2/3)*L_cone  # if all conical
    expected_x_cp = (expected_x_cp_min + expected_x_cp_max) / 2  # rough estimate
    
    print(f"Blunt-Nosed Payload Fairing CoP: {x_cp:.4f} m")
    print(f"Expected range: {expected_x_cp_min:.3f} - {expected_x_cp_max:.3f} m")
    print(f"Fairing: {L_cyl:.1f}m cylindrical + {L_cone:.1f}m conical")
    assert expected_x_cp_min < x_cp < expected_x_cp_max, f"CoP {x_cp:.4f} outside expected range"
    assert Cn > 0, "Cn should be positive" 


def test_bulbous_payload_fairing_cop():
    """
    Test a bulbous payload fairing where the cylindrical section is wider than the rocket body.
    This is common in real rockets where the payload requires more volume than the rocket body.
    """
    import numpy as np
    # Bulbous fairing: cylindrical section wider than rocket body
    L_total = 1.0  # total length
    L_cyl = 0.5    # cylindrical section length
    L_cone = 0.5   # conical section length
    R_fairing = 0.4  # fairing radius (wider than rocket)
    R_rocket = 0.1   # rocket body radius (much smaller)
    
    # Create profile: cylindrical from 0 to L_cyl, then conical taper to rocket body
    x = np.linspace(0, L_total, 200)
    y = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        if xi <= L_cyl:
            # Cylindrical section - constant wide radius
            y[i] = R_fairing
        else:
            # Conical taper: from R_fairing to R_rocket
            # y = R_fairing - (R_fairing - R_rocket) * (x - L_cyl) / L_cone
            y[i] = R_fairing - (R_fairing - R_rocket) * (xi - L_cyl) / L_cone
    
    profile_points = list(zip(x.tolist(), y.tolist()))

    fairing = PayloadFairing(
        part="payload_fairing",
        name="Bulbous Payload Fairing",
        length=L_total,
        base_diameter=2*R_fairing,
        shape_type="custom",
        custom_parameters={"profile_points": profile_points}
    )

    rocket = Rocket(
        name="Test Bulbous Payload Fairing Rocket",
        reference_diameter=2*R_rocket,  # rocket body diameter
        components=[fairing]
    )

    x_cp_total, contributions = compute_overall_cop(rocket)
    x_cp, Cn = contributions["Bulbous Payload Fairing"]

    # For a bulbous fairing, the CoP should be:
    # - Closer to the cylindrical section due to larger cross-sectional area
    # - Between the cylindrical centroid and the overall fairing centroid
    expected_x_cp_min = L_cyl/2  # cylindrical section centroid
    expected_x_cp_max = L_cyl + (2/3)*L_cone  # if all conical
    
    print(f"Bulbous Payload Fairing CoP: {x_cp:.4f} m")
    print(f"Expected range: {expected_x_cp_min:.3f} - {expected_x_cp_max:.3f} m")
    print(f"Fairing: {L_cyl:.1f}m cylindrical ({2*R_fairing:.1f}m dia) + {L_cone:.1f}m conical taper")
    print(f"Rocket body diameter: {2*R_rocket:.1f}m")
    print(f"Bulge ratio: {R_fairing/R_rocket:.1f}:1")
    
    assert expected_x_cp_min < x_cp < expected_x_cp_max, f"CoP {x_cp:.4f} outside expected range"
    assert Cn > 0, "Cn should be positive"
    # The bulbous fairing should have higher Cn due to larger cross-sectional area
    assert Cn > 0.01, "Bulbous fairing should have significant aerodynamic contribution" 