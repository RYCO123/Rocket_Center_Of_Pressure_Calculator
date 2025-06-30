# Welcome to the Rocket COP Calculator

![CI/CD Status](https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/ci.yml/badge.svg)

This project provides a Python class to calculate a rocket's Center of Pressure (COP) using the subsonic Barrowman method. It is designed to be a simple, reusable tool for model rocket analysis.

This project is automatically tested and deployed using GitHub Actions.

## Quick Start

To get started, install the necessary packages and use the `CalculateCOP` class.

```python
from cop_calculator.calculator import CalculateCOP

# Define your rocket's parameters
params = {
    'nose_type': 'cone',
    'Ln': 12.5, 'd': 5.54, 'CR': 10.0, 'CT': 0.0,
    'S': 5.25, 'LF': 6.5, 'R': 2.77, 'XR': 9.0,
    'XB': 27.0, 'N': 3, 'dF': 5.54, 'dR': 5.54,
    'Lt': 0.0, 'Xp': 0.0
}

# Calculate the COP
rocket = CalculateCOP(**params)
cop_location = rocket.net_COP()

print(f"The Center of Pressure is {cop_location:.2f} units from the nose tip.")
