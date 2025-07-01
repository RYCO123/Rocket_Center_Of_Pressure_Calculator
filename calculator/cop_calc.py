import numpy as np
import matplotlib.pyplot as plt

class CalculateCOP:
    """
    Calculate the Center of Pressure (COP) using the Barrowman method.

    This method is only accurate for subsonic aerodynamic analysis of slender bodies.

    This method allows for any system of units as long as the units are consistent throughout.
    """

    def __init__(self,
                 nose_type: str,
                 Ln: float,
                 d: float,
                 dF: float,
                 dR: float,
                 Lt: float,
                 Xp: float,
                 CR: float,
                 CT: float,
                 S: float,
                 LF: float,
                 R: float,
                 XR: float,
                 XB: float,
                 N: int
                 ):
        """
        Initialize the rocket's geometric data.

        Args:
            nose_type (str): Type of nose cone ('ogive' or 'cone').
            Ln (float): Length of the nose cone.
            d (float): Diameter at the base of the nose cone.
            dF (float): Diameter at the front of a transition (if any).
            dR (float): Diameter at the rear of a transition (if any).
            Lt (float): Length of the transition.
            Xp (float): Distance from the tip of the nose to the front of the transition.
            CR (float): Fin root chord.
            CT (float): Fin tip chord.
            S (float): Fin semispan (the height of one fin).
            LF (float): Length of the fin mid-chord line.
            R (float): Radius of the rocket body at the aft end.
            XR (float): Fin sweep distance. Distance from the fin root leading edge
                        to the fin tip leading edge, parallel to the body.
            XB (float): Distance from the nose tip to the fin root chord leading edge.
            N (int): The number of fins.
        """

        nose_type = nose_type.lower()
        if nose_type not in {'ogive', 'cone'}:
            raise ValueError(f"Invalid nose_type '{nose_type}'. Must be 'ogive' or 'cone'.")
        

        self.nose_type = nose_type.lower()
        self.Ln = float(Ln)
        self.d = float(d)
        self.dF = float(dF)
        self.dR = float(dR)
        self.Lt = float(Lt)
        self.Xp = float(Xp)
        self.CR = float(CR)
        self.CT = float(CT)
        self.S = float(S)
        self.LF = float(LF)
        self.R = float(R)
        self.XR = float(XR)
        self.XB = float(XB)
        self.N = int(N)


    def constant_calculations(self):
        """Calculate the nose, transition and fin constants"""
        cnn = 2
        cnt = 2 * ((self.dR/self.d)**2 - (self.dF/self.d)**2)
        cnf = (1 + (self.R/(self.S + self.R))) * (4 * self.N * (self.S/self.d)**2) / (1 + np.sqrt(1 + ((2 * self.LF)/(self.CR + self.CT))**2 ))
        return cnn, cnt, cnf
    

    def nose_contribution(self):
        """Calculate the contribution of the nose to COP"""
        if self.nose_type == 'cone':
            return 0.666 * self.Ln
        elif self.nose_type == 'ogive':
            return 0.466 * self.Ln


    def transition_contribution(self):
        """Calculate the contribution of the transition to COP"""
        if self.dF == self.dR or self.Lt == 0 or self.Xp == 0:
            warnings = []
            if self.dF == self.dR:
                warnings.append("dF == dR (no diameter change in transition)")
            if self.Lt == 0:
                warnings.append("Lt == 0 (transition length is zero)")
            if self.Xp == 0:
                warnings.append("Xp == 0 (transition location is at nose tip)")

            print("Warning: Transition contribution ignored due to the following reason(s):")
            for reason in warnings:
                print(f" - {reason}")

            return 0
        else:
            return self.Xp + (self.Lt/3) * (1 + (1 - ((self.dF)/(self.dR)))/(1 - ((self.dF)/(self.dR))**2))
    

    def fin_contribution(self):
        """Calculate the contribution of the fins to COP"""
        return self.XB + ((self.XR/3) * ((self.CR + 2 * self.CT)/(self.CR + self.CT))) + (1/6) * ((self.CR + self.CT) - ((self.CR * self.CT)/(self.CR + self.CT)))

    def net_COP(self):
        """Calculate the location of COP as measured from the nose down the length of the rocket"""
        cnn, cnt, cnf = self.constant_calculations()
        Xn = self.nose_contribution()
        Xt = self.transition_contribution()
        Xf = self.fin_contribution()
        if self.dF == self.dR or self.Lt == 0 or self.Xp == 0:
            cnt = 0 
        return ((cnn * Xn) + (cnt * Xt) + (cnf * Xf)) / (cnn + cnt + cnf)

    def visualize_rocket(self, show_plot=True, save_path=None):
        """
        Generate 3D visualization of the rocket with COP location.
        
        Args:
            show_plot (bool): Whether to display the plot
            save_path (str): Path to save the plot image (optional)
            
        Returns:
            matplotlib.figure.Figure: The generated figure
        """

        from visualization import visualize_rocket
        
        # Calculate COP location
        cop_location = self.net_COP()
        
        # Create 3D plot using the new visualization function
        fig = visualize_rocket(
            nose_type=self.nose_type,
            Ln=self.Ln,
            d=self.d,
            Lt=self.Lt,
            dF=self.dF,
            dR=self.dR,
            Xp=self.Xp,
            N=self.N,
            CR=self.CR,
            CT=self.CT,
            S=self.S,
            XB=self.XB,
            XR=self.XR,
            cp_location=cop_location
        )
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show_plot:
            plt.show()
        
        return fig
            
if __name__ == '__main__':
    params = {
        'nose_type': 'ogive',
        'Ln': 12.5,
        'd': 5.54,
        'CR': 10.0,
        'CT': 0.0,
        'S': 5.25,
        'LF': 6.5,
        'R': 2.77,
        'XR': 9.0,
        'XB': 27.0,
        'N': 3,
        'dF': 5.54,
        'dR': 5.54,
        'Lt': 0.0,
        'Xp': 0.0,
    }

    COP = CalculateCOP(**params)
    print(COP.net_COP())