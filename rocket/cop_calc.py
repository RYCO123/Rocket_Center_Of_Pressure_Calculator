import numpy as np
from .geometry import NoseCone, BodyTube, FinSet, Rocket, PayloadFairing
from .custom_fairing import compute_custom_fairing_cop


def _calculate_nosecone_cop(nosecone: NoseCone, rocket: Rocket):
    """
    Calculate the Center of Pressure for a nose cone using Barrowman equations.
    
    Args:
        nosecone: NoseCone object
        rocket: Rocket object (for reference diameter)
        
    Returns:
        tuple: (x_cp, C_Nα) where x_cp is distance from nose tip in meters
    """
    C_Nα = 2.0
    
    if nosecone.type == "ogive":
        x_cp = 0.466 * nosecone.length
    elif nosecone.type == "cone":
        x_cp = 0.666 * nosecone.length
    else:
        raise ValueError(f"Unknown nosecone type: {nosecone.type}")
    
    return (x_cp, C_Nα)


def _calculate_finset_cop(finset: FinSet, rocket: Rocket):
    """
    Calculate the Center of Pressure for a fin set using Barrowman equations.
    
    Args:
        finset: FinSet object
        rocket: Rocket object (for reference diameter)
        
    Returns:
        tuple: (x_cp, C_Nα) where x_cp is distance from nose tip in meters
    """
    # Calculate normal force coefficient slope for fins
    C_Nα_fins = (1 + rocket.reference_diameter / (2 * finset.span + rocket.reference_diameter)) * \
                (4 * finset.count * (finset.span / rocket.reference_diameter)**2) / \
                (1 + np.sqrt(1 + (2 * (finset.sweep + finset.tip_chord / 2 - finset.root_chord / 2) / 
                                 (finset.root_chord + finset.tip_chord))**2))
    
    # Calculate center of pressure for fins
    x_cp_fins = finset.position_from_nose_tip + \
                (finset.sweep * (finset.root_chord + 2 * finset.tip_chord) + 
                 (1/6) * (finset.root_chord**2 + finset.tip_chord**2 + finset.root_chord * finset.tip_chord)) / \
                (finset.root_chord + finset.tip_chord)
    
    return (x_cp_fins, C_Nα_fins)


def compute_overall_cop(rocket: Rocket):
    """
    Compute the overall Center of Pressure for the entire rocket.
    
    Args:
        rocket: Rocket object with all components
        
    Returns:
        tuple: (x_cp_total, contributions) where:
            - x_cp_total is the overall CoP distance from nose tip in meters
            - contributions is a dict mapping component names to their (x_cp, C_Nα) values
    """
    total_C_Nα = 0
    total_moment = 0
    contributions = {}
    
    for component in rocket.components:
        if isinstance(component, NoseCone):
            x_cp, C_Nα = _calculate_nosecone_cop(component, rocket)
            contributions[component.part] = (x_cp, C_Nα)
        
        elif isinstance(component, FinSet):
            x_cp, C_Nα = _calculate_finset_cop(component, rocket)
            contributions[component.part] = (x_cp, C_Nα)
        
        elif isinstance(component, BodyTube):
            # Body tubes contribute no normal force in this simplified model
            contributions[component.name] = (0, 0)
            continue
        
        elif isinstance(component, PayloadFairing):
            if getattr(component, 'shape_type', None) == 'custom' and component.custom_parameters:
                profile_points = component.custom_parameters.get('profile_points')
                if profile_points:
                    # Ensure profile_points are in meters
                    # (Assume input is in meters, or convert if needed)
                    x_cp, C_Nα = compute_custom_fairing_cop(profile_points)
                    contributions[component.name] = (x_cp, C_Nα)
                    total_C_Nα += C_Nα
                    total_moment += C_Nα * x_cp
                    continue
            # If not custom or missing profile, skip or treat as no contribution
            contributions[component.name] = (0, 0)
            continue
        
        # Add to totals for contributing components
        total_C_Nα += C_Nα
        total_moment += C_Nα * x_cp
    
    # Calculate overall CoP
    if total_C_Nα > 0:
        x_cp_total = total_moment / total_C_Nα
    else:
        x_cp_total = 0
    
    return x_cp_total, contributions 