import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rocket.geometry import NoseCone, BodyTube, FinSet, Rocket, load_rocket_from_config
from rocket.utils import mm_to_m


def test_mm_to_m_conversion():
    """Test that mm_to_m correctly converts millimeters to meters."""
    assert mm_to_m(1000) == 1.0
    assert mm_to_m(254) == 0.254
    assert mm_to_m(66.8) == 0.0668


def test_nosecone_creation():
    """Test that NoseCone objects are created correctly."""
    nosecone = NoseCone(
        part="nosecone",
        type="ogive",
        length=0.254,
        base_diameter=0.0668
    )
    
    assert nosecone.part == "nosecone"
    assert nosecone.type == "ogive"
    assert nosecone.length == 0.254
    assert nosecone.base_diameter == 0.0668


def test_body_tube_creation():
    """Test that BodyTube objects are created correctly."""
    body_tube = BodyTube(
        part="body_tube",
        name="Payload Section",
        length=0.3048,
        diameter=0.0668
    )
    
    assert body_tube.part == "body_tube"
    assert body_tube.name == "Payload Section"
    assert body_tube.length == 0.3048
    assert body_tube.diameter == 0.0668


def test_fin_set_creation():
    """Test that FinSet objects are created correctly."""
    fin_set = FinSet(
        part="fin_set",
        count=3,
        root_chord=0.152,
        tip_chord=0.076,
        span=0.095,
        sweep=0.051,
        thickness=0.003175,
        position_from_nose_tip=1.0926
    )
    
    assert fin_set.part == "fin_set"
    assert fin_set.count == 3
    assert fin_set.root_chord == 0.152
    assert fin_set.tip_chord == 0.076
    assert fin_set.span == 0.095
    assert fin_set.sweep == 0.051
    assert fin_set.thickness == 0.003175
    assert fin_set.position_from_nose_tip == 1.0926


def test_rocket_creation():
    """Test that Rocket objects are created correctly."""
    components = [
        NoseCone("nosecone", "ogive", 0.254, 0.0668),
        BodyTube("body_tube", "Payload Section", 0.3048, 0.0668)
    ]
    
    rocket = Rocket(
        name="Test Rocket",
        reference_diameter=0.0668,
        components=components
    )
    
    assert rocket.name == "Test Rocket"
    assert rocket.reference_diameter == 0.0668
    assert len(rocket.components) == 2
    assert isinstance(rocket.components[0], NoseCone)
    assert isinstance(rocket.components[1], BodyTube) 