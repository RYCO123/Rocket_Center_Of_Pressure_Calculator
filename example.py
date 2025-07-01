#!/usr/bin/env python3
"""
Example: Calculate Center of Pressure for LOC Expediter rocket
"""

from calculator import CalculateCOP

def main():
    # LOC Expediter rocket parameters
    params = {
        'nose_type': 'ogive',
        'Ln': 11.25,
        'd': 3.0,
        'dF': 3.0,
        'dR': 4.0,
        'Lt': 2.5,
        'Xp': 25.259,
        'CR': 10.5,
        'CT': 2.559,
        'S': 4.25,
        'LF': 7.0,
        'XR': 7.87,
        'R': 1.5,
        'XB': 106.299,
        'N': 3,
    }

    cop_calc = CalculateCOP(**params)
    cop_location = cop_calc.net_COP()

    print("Rocket COP Calculator Example")
    print("=" * 30)
    print("Rocket: LOC Expediter")
    print(f"Center of Pressure: {cop_location:.2f} inches from nose tip")
    print()
    print("Component contributions:")
    print(f"  Nose cone: {cop_calc.nose_contribution():.2f} inches")
    print(f"  Transition: {cop_calc.transition_contribution():.2f} inches")
    print(f"  Fins: {cop_calc.fin_contribution():.2f} inches")
    
    # Create 3D visualization
    print("\nGenerating 3D visualization...")
    cop_calc.visualize_rocket()

if __name__ == "__main__":
    main() 