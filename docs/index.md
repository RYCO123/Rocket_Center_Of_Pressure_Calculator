# Rocket COP Calculator

This project provides a Python class to calculate a rocket's Center of Pressure (COP) using the subsonic Barrowman method. It is designed to be a simple, reusable tool for model rocket analysis.

## Quick Start

Run the example script to see it in action:

```bash
python example.py
```

Or use the `CalculateCOP` class directly:

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

See the [API Reference](api.md) for parameter details.

## Theory & References

The Center of Pressure is calculated using the Barrowman equations, considering nose, transition, and fin contributions. For stability, the COP should be behind the rocket's center of gravity (CG) by at least one body diameter ("one caliber stability").

For a diagram and detailed explanation of each variable, see the [Barrowman Equations page](https://www.rocketmime.com/rockets/Barrowman.html).

![CI/CD Status](https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/ci.yml/badge.svg)

This project is automatically tested and deployed using GitHub Actions.
