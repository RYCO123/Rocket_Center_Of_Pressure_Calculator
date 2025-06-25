import json
from pathlib import Path


def mm_to_m(value):
    """Convert millimeters to meters by dividing by 1000."""
    return value / 1000.0


def load_json(path):
    """Load and return data from a JSON file."""
    with open(path, 'r') as file:
        return json.load(file) 