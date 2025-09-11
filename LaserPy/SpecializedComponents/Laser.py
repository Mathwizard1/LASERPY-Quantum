import matplotlib.pyplot as plt
import numpy as np

from ..Components import PhysicalComponent

from ..Constants import UniversalConstants
from ..Constants import LaserPyConstants
from ..Constants import ERR_TOLERANCE, FIG_WIDTH, FIG_HEIGHT

class Laser(PhysicalComponent):
    """
    Laser class for simulations
    """
    def __init__(self, save_simulation: bool = False, name: str = "default_physical_component"):
        super().__init__(save_simulation, name)
        self.photon = ERR_TOLERANCE
        """photon data for Laser"""

        self.carrier = LaserPyConstants.get('N_transparent')
        """carrier data for Laser"""

        self.electric_field = ERR_TOLERANCE
        """electric_field data for Laser"""

        self._simulation_data = {'current':[], 'photon':[], 'carrier':[], 'electric_field':[], 'phase':[]}
        self._simulation_data_units = {'current':r" $()$", 'photon':r" $()$", 
                                       'carrier':r" $()$", 'electric_field':r" $()$"}

        self._phase = ERR_TOLERANCE
        """phase data for Laser"""

        self._Dphase = ERR_TOLERANCE
        """Delta phase data for Laser"""

    def reset(self):
        """Laser reset method"""
        #return super().reset()
        self.photon = ERR_TOLERANCE
        self.carrier = LaserPyConstants.get('N_transparent')
        self.electric_field = ERR_TOLERANCE

        self._phase = ERR_TOLERANCE
        self._Dphase = ERR_TOLERANCE

###############################################################################
class L:
    def values(self):
        """
        Physical constraint check and get simulation values
        """
        self.N_t = max(err_fault, self.N_t)
        self.S_t = max(err_fault, self.S_t)

        # Phase and Photons gives Optical field
        self.E_t = np.sqrt(Power(self.S_t, self.fr_freq)) * np.exp2(1j * self.Phi_t)

        return (self.N_t, self.S_t, self.Phi_t, self.E_t)

    def dN_dt(self, I_t, Fn_t):
        """
        delta Number of Carriers
        """
        val = I_t / (universalConstants.charge.value * Vol) - self.N_t / Tau_n - g * ((self.N_t - self.N0) / (1.0 + Epsilon * self.S_t)) * self.S_t + Fn_t
        return val

    def dS_dt(self, Fs_t):
        """
        delta Photon density
        """
        val = Gamma_cap * g * ((self.N_t - self.N0) / (1.0 + Epsilon * self.S_t)) * self.S_t - self.S_t / Tau_p + Gamma_cap * Beta * self.N_t / Tau_n + Fs_t
        return val

    def dPhi_dt(self, Fphi_t):
        """
        delta Optical phase
        """
        val = (Alpha / 2.0) * (Gamma_cap * g * (self.N_t - self.N0) - 1.0 / Tau_p) + Fphi_t
        return val
    
class SlaveLaser(Laser):
    """
    Slave Laser class\n
    Parent: Laser class
    """
    def __init__(self, name, fr_freq=0, N0=N_transparent, S0= err_fault, Phi0= err_fault):
        super().__init__(name, fr_freq, N0, S0, Phi0)
        
        self.master_laser = None
        """ injection Master laser """

    def set_master_laser(self, master_laser: Laser):
        """
        Set stabilised master laser
        """
        self.master_laser = master_laser
        
        self.Delta_Winj = self.fr_freq - master_laser.fr_freq
        """ frequency detuning """

    def update(self, I_t, t, dt= 1e-3, Fn_t= 0.0, Fs_t= 0.0, Fphi_t= 0.0):
        """
        Update N, S, phi for slave laser and return current value
        """
        # Optical Injection Lock Terms
        if(self.master_laser is not None):
            Delta_phi = self.Phi_t - self.master_laser.Phi_t - self.Delta_Winj * t

            temp_N_t = self.N_t + self.dN_dt(I_t, Fn_t) * dt 
            temp_S_t = self.S_t + (self.dS_dt(Fs_t) + 2 * Kappa * np.sqrt(self.master_laser.S_t * self.S_t) * np.cos(Delta_phi)) * dt
            self.dPhi = (self.dPhi_dt(Fphi_t) - Kappa * np.sqrt(self.master_laser.S_t / self.S_t) * np.sin(Delta_phi)) * dt
        
            """ time step update """ 
            self.N_t = temp_N_t
            self.S_t = temp_S_t
            self.Phi_t += self.dPhi
        else:
            return super().update(I_t, t, dt, Fn_t, Fs_t, Fphi_t)
        return self.values()