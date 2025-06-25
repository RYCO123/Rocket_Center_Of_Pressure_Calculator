# Rocket CoP Calculator

A Python library for computing the Center of Pressure (CoP) of model rockets using the Barrowman equations. This tool provides accurate aerodynamic analysis for rocket stability calculations.

## Features

- **Modular Design**: Clean separation of geometry, calculations, and utilities
- **Data-Driven**: Rocket configurations loaded from JSON files
- **Barrowman Equations**: Implements standard aerodynamic theory for rocket stability
- **Multiple Components**: Supports nosecones, body tubes, and fin sets
- **Extensible**: Easy to add new component types and calculation methods

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rocket_cop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the example script to calculate CoP for the LOC Precision Hi-Tech H45 rocket:

```bash
python examples/compute_hi_tech.py
```

### Programmatic Usage

```python
from rocket.geometry import load_rocket_from_config
from rocket.cop_calc import compute_overall_cop

# Load rocket configuration
rocket = load_rocket_from_config('rocket/config/hi_tech.json')

# Calculate Center of Pressure
cop_m, contributions = compute_overall_cop(rocket)

print(f"Overall CoP: {cop_m:.4f} m from nose tip")
```

## Project Structure

```
rocket_cop/
├── rocket/                 # Main package
│   ├── config/            # Rocket configuration files
│   ├── geometry.py        # Component data classes and loading
│   ├── cop_calc.py        # Barrowman equations implementation
│   └── utils.py           # Utility functions
├── examples/              # Example scripts
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

Rocket configurations are stored in JSON format. Each component includes:

- **Nosecones**: Type (ogive/cone), length, base diameter
- **Body Tubes**: Name, length, diameter  
- **Fin Sets**: Count, root/tip chord, span, sweep, thickness, position

Example configuration:
```json
{
  "name": "My Rocket",
  "reference_diameter_mm": 66.8,
  "components": [
    {
      "part": "nosecone",
      "type": "ogive",
      "length_mm": 254.0,
      "base_diameter_mm": 66.8
    }
  ]
}
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Theory

The Center of Pressure calculation uses the Barrowman equations, which provide:

- **Nosecone CoP**: Based on shape type (ogive vs cone)
- **Fin CoP**: Complex calculation considering fin geometry and interference
- **Body Tubes**: Neglected in simplified model (no normal force contribution)

The overall CoP is calculated as a weighted average of individual component contributions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source. Please see the LICENSE file for details. 