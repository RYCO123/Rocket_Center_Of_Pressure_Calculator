# Rocket COP Calculator

![CI](https://github.com/RYCO123/Rocket_Center_Of_Pressure_Calculator/actions/workflows/ci.yml/badge.svg)

A Python library for computing the Center of Pressure (COP) of model rockets using the Barrowman equations. This tool provides accurate aerodynamic analysis for rocket stability calculations.

I used this tool to help find the Center of Pressure of my L1 certificaiton "Super Rocket" (a Loc Precision Hi-Tech H45) pictured below. 

![IMG_6991](https://github.com/user-attachments/assets/38d721f7-f67b-4c1c-943a-2e393f6fadae)



## Features

- Implements the Barrowman equations for subsonic model rockets
- Supports both ogive and cone nose shapes, transitions, and fins
- Simple, single-class API (`CalculateCOP`)
- Unit-agnostic: use any consistent length units

## Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd rocket_cop
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from calculator import CalculateCOP

params = {
    'nose_type': 'ogive',
    'Ln': 12.5,
    'd': 5.54,
    'dF': 5.54,
    'dR': 5.54,
    'Lt': 0.0,
    'Xp': 0.0,
    'CR': 10.0,
    'CT': 0.0,
    'S': 5.25,
    'LF': 6.5,
    'R': 2.77,
    'XR': 9.0,
    'XB': 27.0,
    'N': 3,
}

cop = CalculateCOP(**params)
print(f"Center of Pressure: {cop.net_COP():.2f} units from nose tip")
```

### Parameters

The `CalculateCOP` class requires the following parameters (all units must be consistent):

| Parameter | Description |
|-----------|-------------|
| nose_type | Nose cone shape: `'ogive'` or `'cone'` |
| Ln        | Length of nose cone |
| d         | Diameter at base of nose cone |
| dF        | Diameter at front of transition (set equal to `d` if no transition) |
| dR        | Diameter at rear of transition (set equal to `d` if no transition) |
| Lt        | Length of transition (set to 0.0 if no transition) |
| Xp        | Distance from nose tip to front of transition (set to 0.0 if no transition) |
| CR        | Fin root chord |
| CT        | Fin tip chord |
| S         | Fin semispan (height of one fin) |
| LF        | Length of fin mid-chord line |
| R         | Radius of body at aft end |
| XR        | Fin sweep distance (root leading edge to tip leading edge, parallel to body) |
| XB        | Distance from nose tip to fin root chord leading edge |
| N         | Number of fins |

For a diagram and detailed explanation of each variable, see the [Barrowman Equations page](https://www.rocketmime.com/rockets/Barrowman.html).

## Testing

Run the test suite:

```bash
pytest tests/
```

## Theory

The Center of Pressure is calculated using the Barrowman equations, considering nose, transition, and fin contributions. For stability, the COP should be behind the rocket's center of gravity (CG) by at least one body diameter ("one caliber stability").

The equations and variable definitions are based on the classic Barrowman method. For more details and a helpful diagram, see [RocketMime's Barrowman Equations page](https://www.rocketmime.com/rockets/Barrowman.html).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.

## References

- Barrowman Equations and variable definitions:  
  [https://www.rocketmime.com/rockets/Barrowman.html](https://www.rocketmime.com/rockets/Barrowman.html)  
  This page includes a helpful diagram and detailed explanation of each parameter used in the Barrowman equations. 
