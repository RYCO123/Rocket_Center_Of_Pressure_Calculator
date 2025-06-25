from dataclasses import dataclass
from typing import List, Optional
from .utils import mm_to_m, load_json


@dataclass
class NoseCone:
    """Represents a nose cone component."""
    part: str
    type: str
    length: float  # in meters
    base_diameter: float  # in meters


@dataclass
class BodyTube:
    """Represents a body tube component."""
    part: str
    name: str
    length: float  # in meters
    diameter: float  # in meters


@dataclass
class IrregularBody:
    """Represents an irregular body section with varying diameter."""
    part: str
    name: str
    length: float  # in meters
    front_diameter: float  # in meters
    rear_diameter: float  # in meters
    position_from_nose_tip: float  # in meters


@dataclass
class PayloadFairing:
    """Represents a payload fairing with complex geometry."""
    part: str
    name: str
    length: float  # in meters
    base_diameter: float  # in meters
    shape_type: str  # "conical", "ogive", "parabolic", "custom"
    # For custom shapes, additional parameters can be added
    custom_parameters: Optional[dict] = None


@dataclass
class FinSet:
    """Represents a fin set component."""
    part: str
    count: int
    root_chord: float  # in meters
    tip_chord: float  # in meters
    span: float  # in meters
    sweep: float  # in meters
    thickness: float  # in meters
    position_from_nose_tip: float  # in meters


@dataclass
class Rocket:
    """Represents a complete rocket with all its components."""
    name: str
    reference_diameter: float  # in meters
    components: List


def load_rocket_from_config(path):
    """
    Load rocket configuration from JSON file and create Rocket object.
    
    Args:
        path: Path to the JSON configuration file
        
    Returns:
        Rocket object with all components
    """
    data = load_json(path)
    
    components = []
    
    for component_data in data['components']:
        part_type = component_data['part']
        
        if part_type == 'nosecone':
            component = NoseCone(
                part=component_data['part'],
                type=component_data['type'],
                length=mm_to_m(component_data['length_mm']),
                base_diameter=mm_to_m(component_data['base_diameter_mm'])
            )
        elif part_type == 'body_tube':
            component = BodyTube(
                part=component_data['part'],
                name=component_data['name'],
                length=mm_to_m(component_data['length_mm']),
                diameter=mm_to_m(component_data['diameter_mm'])
            )
        elif part_type == 'irregular_body':
            component = IrregularBody(
                part=component_data['part'],
                name=component_data['name'],
                length=mm_to_m(component_data['length_mm']),
                front_diameter=mm_to_m(component_data['front_diameter_mm']),
                rear_diameter=mm_to_m(component_data['rear_diameter_mm']),
                position_from_nose_tip=mm_to_m(component_data['position_from_nose_tip_mm'])
            )
        elif part_type == 'payload_fairing':
            component = PayloadFairing(
                part=component_data['part'],
                name=component_data['name'],
                length=mm_to_m(component_data['length_mm']),
                base_diameter=mm_to_m(component_data['base_diameter_mm']),
                shape_type=component_data['shape_type'],
                custom_parameters=component_data.get('custom_parameters')
            )
        elif part_type == 'fin_set':
            component = FinSet(
                part=component_data['part'],
                count=component_data['count'],
                root_chord=mm_to_m(component_data['root_chord_mm']),
                tip_chord=mm_to_m(component_data['tip_chord_mm']),
                span=mm_to_m(component_data['span_mm']),
                sweep=mm_to_m(component_data['sweep_mm']),
                thickness=mm_to_m(component_data['thickness_mm']),
                position_from_nose_tip=mm_to_m(component_data['position_from_nose_tip_mm'])
            )
        else:
            raise ValueError(f"Unknown component type: {part_type}")
        
        components.append(component)
    
    rocket = Rocket(
        name=data['name'],
        reference_diameter=mm_to_m(data['reference_diameter_mm']),
        components=components
    )
    
    return rocket 