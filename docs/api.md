Generated markdown
The Barrowman equations permit you to determine the stability of your rocket by finding the location of the center of pressure (CP). The value computed is the distance from the tip of the rocket's nose to the CP. In order for your rocket to be stable, the CP must be located behind the center of gravity (CG).

You can find the CG of your rocket by simply finding its balance point after loading the recovery system and motor. The distance from the tip of the rocket's nose to this balance point is the CG location. For a stable flight, the calculated CP distance should be greater than the measured CG distance by at least one rocket body diameter. This is called "one caliber stability".

---

## `CalculateCOP` Class

This class implements the Barrowman equations to calculate the Center of Pressure for a subsonic rocket. It accounts for contributions from the nose cone, body transitions, and fins.

### Initialization

To begin, import the class and create an instance of it by providing your rocket's geometric parameters. All length-based units must be consistent (e.g., all in inches or all in centimeters).

**Example 1: Simple Rocket (No Transitions)**

For a rocket with a single body tube diameter, set the transition parameters to zero and the transition diameters equal to the body diameter.

```python
from cop_calculator.calculator import CalculateCOP

# Rocket with a straight body tube
simple_rocket = CalculateCOP(
    nose_type='ogive',
    Ln=12.5,
    d=5.54,
    CR=10.0,
    CT=4.0,
    S=5.25,
    LF=6.5,  # Calculated from S and XR
    R=2.77,  # d/2
    XR=3.5,
    XB=27.0,
    N=3,
    # No transition section
    dF=5.54, # Same as d
    dR=5.54, # Same as d
    Lt=0.0,
    Xp=0.0
)


Example 2: Rocket with a Transition (e.g., a payload bay reducer)

Generated python
from cop_calculator.calculator import CalculateCOP

# Rocket with a transition from a larger to smaller diameter
transition_rocket = CalculateCOP(
    nose_type='cone',
    Ln=20.0,
    d=7.6,
    CR=15.0,
    CT=7.0,
    S=8.0,
    LF=9.43, # Calculated from S and XR
    R=3.8,   # d/2
    XR=5.0,
    XB=45.0,
    N=4,
    # Transition section details
    dF=10.0, # Diameter at the front of the transition
    dR=7.6,  # Diameter at the rear of the transition (matches body tube d)
    Lt=8.0,  # Length of the transition
    Xp=20.0  # Distance from nose tip to start of transition
)
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Constructor Parameters

The following parameters must be provided when creating a CalculateCOP object.

Parameter	Symbol	Type	Description
nose_type	-	str	The shape of the nose cone. Must be either 'ogive' or 'cone'.
Ln	L<sub>N</sub>	float	The length of the nose cone.
d	d	float	The diameter at the base of the nose cone (typically the main body tube diameter).
dF	d<sub>F</sub>	float	The diameter at the front of a transition section. For a simple rocket, this is the same as d.
dR	d<sub>R</sub>	float	The diameter at the rear of a transition section. For a simple rocket, this is the same as d.
Lt	L<sub>T</sub>	float	The length of the transition section. Set to 0.0 for a simple rocket.
Xp	X<sub>P</sub>	float	The distance from the tip of the nose cone to the front of the transition section.
CR	C<sub>R</sub>	float	The Fin Root Chord: the length of the fin where it attaches to the body.
CT	C<sub>T</sub>	float	The Fin Tip Chord: the length of the fin at its outermost edge.
S	S	float	The Fin Semispan: the height of a single fin, measured from the body outwards.
LF	L<sub>F</sub>	float	The length of the fin mid-chord line. This can be calculated as sqrt(S² + XR²).
R	R	float	The radius of the rocket body tube at the aft end (equal to d / 2).
XR	X<sub>R</sub>	float	The Fin Sweep Distance: the horizontal distance from the fin root leading edge to the fin tip leading edge.
XB	X<sub>B</sub>	float	The distance from the nose tip to the fin root chord's leading edge.
N	N	int	The total number of fins on the rocket.
Methods
net_COP()

This is the primary method to call. It calculates the overall Center of Pressure (X) for the entire rocket by combining all component contributions. The result is the distance from the tip of the nose cone.

Usage:

Generated python
# Assuming 'simple_rocket' is an initialized CalculateCOP object
center_of_pressure = simple_rocket.net_COP()
print(f"The net Center of Pressure is {center_of_pressure:.2f} units from the nose tip.")
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Returns:

(float): The final Center of Pressure location.

Component Calculation Methods

These methods allow for inspecting the individual parts of the COP calculation. They are called internally by net_COP() but can be used for debugging or analysis.

nose_contribution()

Calculates the location of the center of pressure for the nose cone alone.

Returns: (float)

transition_contribution()

Calculates the location of the center of pressure for the transition section. If no valid transition exists (e.g., Lt=0), this method will print a warning and return 0.

Returns: (float)

fin_contribution()

Calculates the location of the center of pressure for the fin set alone.

Returns: (float)

constant_calculations()

Calculates the normal force coefficient derivatives (C<sub>N</sub>) for the nose, transition, and fins. These constants represent how much force each component generates.

Returns: A tuple (cnn, cnt, cnf) containing the three float constants.

Generated code
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
