import pytest
from calculator import CalculateCOP

test_rockets = [
    (
        {
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
        },
        24.65, # this is for a LOC Precision Minie-Magg rocket kit. COP is found on their website
    ),
    (
        {

            'nose_type': 'ogive',  
            'Ln': 9,  
            'd': 2.6,     
            'dF': 2.6,         
            'dR': 2.6,      
            'Lt': 0.0, 
            'Xp': 0.0,     
            'N': 3,        
            'CR': 4.527,       
            'CT': 2.55,      
            'S': 3.93,    
            'LF': 4.21,  
            'XR': 0.511,    
            'R': 1.3, 
            'XB': 44.488,
        },
        41.71, # this is for a LOC Precision HI-TECH H45 (Super Rocket found in the READ ME), COP is found on their website
    ),
    (
        {
            'nose_type': 'ogive',
            'Ln': 11.25, 
            'd': 3.0, 
            'dF': 3.0,   
            'dR': 4.0,      
            'Lt': 2.5,        
            'Xp': 11.259,   
            'N': 3,     
            'CR': 10.5,
            'CT': 2.559,       
            'S': 4.25,         
            'LF': 7.0,    
            'XR': 7.87,      
            'R': 1.5,    
            'XB': 106.299, 
        },

        91.3386, # this is for the loc expediter. Used the COP calculated in Open Rocket for verification. This rocket has a transition section
    ),
]

@pytest.mark.parametrize("params, known_cop", test_rockets)
def test_cop_within_tolerance(params, known_cop):
    calc = CalculateCOP(**params)
    computed_cop = calc.net_COP()  # or whichever method returns the COP value
    tol = 0.05  # 5% tolerance
    lower_bound = known_cop * (1 - tol)
    upper_bound = known_cop * (1 + tol)
    assert lower_bound <= computed_cop <= upper_bound, (
        f"COP {computed_cop} not within ±5% of known {known_cop}"
    )
