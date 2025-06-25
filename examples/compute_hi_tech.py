import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rocket.geometry import load_rocket_from_config
from rocket.cop_calc import compute_overall_cop

def main():
    """
    Loads rocket data, computes the Center of Pressure, and prints the results.
    """
    config_path = project_root / 'rocket' / 'config' / 'hi_tech.json'
    
    print(f"Loading rocket configuration from: {config_path}")
    rocket = load_rocket_from_config(config_path)
    
    cop_m, contributions = compute_overall_cop(rocket)
    
    print("\n--- Center of Pressure Calculation Results ---")
    print(f"Rocket: {rocket.name}")
    print(f"Overall CoP: {cop_m:.4f} m from the nose tip")
    print(f"Overall CoP: {cop_m * 39.37:.2f} inches from the nose tip")
    
    print("\nComponent Contributions:")
    for part, (x_cp, Cna) in contributions.items():
        if Cna > 0:
            print(f"  - {part:<15}: CoP = {x_cp:.4f} m, Cna = {Cna:.3f}")

if __name__ == "__main__":
    main() 