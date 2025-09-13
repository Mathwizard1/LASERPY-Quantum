from __future__ import annotations

import numpy as np

from ..Components import Clock
from ..Components import PhysicalComponent

from ..Components.Signal import NoNoise

from ..Constants import UniversalConstants
from ..Constants import LaserPyConstants
from ..Constants import ERR_TOLERANCE

class Laser(PhysicalComponent):
    """
    Laser class for simulations
    """

    # Class variables for Laser
    _TAU_N = LaserPyConstants.get('Tau_N')
    _TAU_P = LaserPyConstants.get('Tau_P')

    _g = LaserPyConstants.get('g')
    _Epsilon = LaserPyConstants.get('Epsilon')
  
    _N_transparent = LaserPyConstants.get('N_transparent')

    _Beta = LaserPyConstants.get('Beta')
    _Alpha = LaserPyConstants.get('Alpha')
    _Eta = LaserPyConstants.get('Eta')

    _Laser_Vol = LaserPyConstants.get('Laser_Vol')

    _Gamma_cap = LaserPyConstants.get('Gamma_cap')
    _Kappa = LaserPyConstants.get('Kappa')

    def __init__(self, laser_wavelength:float = 1550.0e-9, save_simulation: bool = False, name: str = "default_laser_component"):
        super().__init__(save_simulation, name)
        self.photon: float = ERR_TOLERANCE
        """photon data for Laser"""

        self.carrier: float = self._N_transparent
        """carrier data for Laser"""

        self.electric_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        """electric_field data for Laser"""

        self.phase: float = ERR_TOLERANCE
        """phase data for Laser"""

        self.current: float = ERR_TOLERANCE
        """current data for Laser"""

        self._simulation_data = {'current':[], 'photon':[], 'carrier':[], 'phase':[]}
        self._simulation_data_units = {'current':r" $()$", 'photon':r" $()$", 
                                       'carrier':r" $()$", 'phase':r" $()$"}

        # Laser class private data
        self._free_running_freq = UniversalConstants.C.value / laser_wavelength
        """free running frequency data for Laser"""

        # Noise classes for simulations
        self._Fn_t = NoNoise('carrier_NoNoise')
        self._Fs_t = NoNoise('photon_NoNoise')
        self._Fphi_t = NoNoise('phase_NoNoise')

        # Optical Injection locking data
        self._slave_locked = False
        self._master_freq_detuning: float|None = None

    def _dN_dt(self):
        """Delta number of carrier method"""
        dN_dt = self.current / (UniversalConstants.CHARGE.value * self._Laser_Vol) - self.carrier / self._TAU_N - self._g * ((self.carrier - self._N_transparent) / (1 + self._Epsilon * self.photon)) * self.photon + self._Fn_t()
        return dN_dt

    def _dS_dt(self):
        """Delta number of photon method"""
        dS_dt = self._Gamma_cap * self._g * ((self.carrier - self._N_transparent) / (1 + self._Epsilon * self.photon)) * self.photon - self.photon / self._TAU_P + self._Gamma_cap * self._Beta * self.carrier / self._TAU_N + self._Fs_t()
        return dS_dt

    def _dPhi_dt(self):
        """Delta phase method"""
        dPhi_dt = self._Alpha / 2 * (self._Gamma_cap * self._g * (self.carrier - self._N_transparent) - 1 / self._TAU_P) + self._Fphi_t()
        return dPhi_dt

    def reset(self):
        """Laser reset method"""
        #return super().reset()
        self.current = ERR_TOLERANCE
        self.photon = ERR_TOLERANCE
        self.carrier = self._N_transparent
        self.electric_field = ERR_TOLERANCE * np.exp(1j * 0)
        self.phase = ERR_TOLERANCE

        # Remove masters
        self._slave_locked = False
        self._master_freq_detuning = None

    def set_Noise(self, Fn_t:NoNoise, Fs_t:NoNoise, Fphi_t:NoNoise):
        """Laser set noise method""" 
        self._Fn_t = Fn_t
        self._Fs_t = Fs_t
        self._Fphi_t = Fphi_t

    def set_master_Laser(self, master_Laser:Laser):
        """Laser set master laser method""" 
        self._slave_locked = True
        self._master_freq_detuning = self._free_running_freq - master_Laser._free_running_freq

    def simulate(self, clock: Clock, current: float, injection_field = None):
        """Laser simulate method"""
        #return super().simulate(clock, data)

        # Save current in its variable
        self.current = current

        # Base Laser rate equations
        dN_dt = self._dN_dt()
        dS_dt = self._dS_dt()
        dPhi_dt = self._dPhi_dt()

        # Injection_field equations
        if(self._slave_locked):
            print("Laser slave locked not implemented")

        # Time step update
        self.carrier += dN_dt * clock.dt
        self.photon += dS_dt * clock.dt
        self.phase += dPhi_dt * clock.dt

        # Value corrections
        self.carrier = max(self.carrier, ERR_TOLERANCE)
        self.photon = max(self.photon, ERR_TOLERANCE)

        # Optical field
        self.electric_field = np.sqrt(self.photon) * np.exp(1j * self.phase)

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """Laser input port method""" 
        #return super().input_port()
        kwargs = {'clock':None, 'current':None, 'injection_field':None}
        return kwargs