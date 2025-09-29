from __future__ import annotations
from typing import TypedDict

import numpy as np

from ..Components import Clock
from ..Components import PhysicalComponent

from ..Components.Signal import NoNoise

from ..Constants import UniversalConstants
from ..Constants import LaserPyConstants

from ..Constants import ERR_TOLERANCE
from ..Constants import EMPTY_FIELD

class InjectionField(TypedDict):
    """
    InjectionField class\n
    A dictionary type for {'photon', 'phase'}.
    """
    photon: float
    phase: float

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

    def __init__(self, laser_wavelength:float = 1550.0e-9, save_simulation: bool = False, name: str = "default_laser"):
        super().__init__(save_simulation, name)
        self.photon: float = ERR_TOLERANCE
        """photon data for Laser"""

        self.carrier: float = self._N_transparent
        """carrier data for Laser"""

        self.phase: float = ERR_TOLERANCE
        """phase data for Laser"""

        self.current: float = ERR_TOLERANCE
        """current data for Laser"""

        # Data storage
        self._simulation_data = {'current':[], 'photon':[], 'carrier':[], 'phase':[]}
        self._simulation_data_units = {'current':r" $(Amp)$", 'photon':r" $(m^{-3})$",
                                           'carrier':r" $(m^{-3})$", 'phase':r" $(rad)$"}

        self._data: np.complexfloating = EMPTY_FIELD
        """electric_field data for Laser"""

        # Laser class private data
        self._free_running_freq = UniversalConstants.C.value / laser_wavelength
        """free running frequency data for Laser"""

        # Noise classes for simulations
        self._Fn_t = NoNoise('carrier_NoNoise')
        self._Fs_t = NoNoise('photon_NoNoise')
        self._Fphi_t = NoNoise('phase_NoNoise')

        # Optical Injection locking data
        self._slave_locked: bool = False
        self._master_freq_detuning: float = 0

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

    def set_noise(self, Fn_t:NoNoise, Fs_t:NoNoise, Fphi_t:NoNoise):
        """Laser set noise method""" 
        self._Fn_t = Fn_t
        self._Fs_t = Fs_t
        self._Fphi_t = Fphi_t

    def set_master_Laser(self, master_Laser:Laser):
        """Laser set master laser method""" 
        self._slave_locked = True
        self._master_freq_detuning = self._free_running_freq - master_Laser._free_running_freq

    def simulate(self, clock: Clock, current: float, injection_field: InjectionField|None = None):
        """Laser simulate method"""
        #return super().simulate(clock, _data)

        # Save current in its variable
        self.current = current

        # Base Laser rate equations
        dN_dt = self._dN_dt()
        dS_dt = self._dS_dt()
        dPhi_dt = self._dPhi_dt()

        # Injection_field equations
        if(self._slave_locked and injection_field):
            # Phase difference between master and slave output
            delta_phase = self.phase - injection_field['phase']

            # Injection terms effects
            dS_dt += 2 * self._Kappa * np.sqrt(injection_field['photon'] * self.photon) * np.cos(delta_phase - self._master_freq_detuning * clock.t)
            dPhi_dt -= self._Kappa * np.sqrt(injection_field['photon'] / self.photon) * np.sin(delta_phase - self._master_freq_detuning * clock.t)

        # Time step update (Euler Integration)
        self.carrier += dN_dt * clock.dt
        self.photon += dS_dt * clock.dt
        self.phase += dPhi_dt * clock.dt

        # Value corrections
        self.carrier = max(self.carrier, ERR_TOLERANCE)
        self.photon = max(self.photon, ERR_TOLERANCE)

        # Optical field
        # TODO correct it
        self._data = np.sqrt(self.photon) * np.exp(1j * self.phase)

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """Laser input port method""" 
        #return super().input_port()
        kwargs = {'clock':None, 'current':None, 'injection_field':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """Laser output port method""" 
        #return super().output_port(kwargs)
        if('injection_field' in kwargs):
            kwargs['injection_field'] = {'photon': self.photon, 'phase': self.phase}
        elif('electric_field' in kwargs):
            kwargs['electric_field'] = self._data
        return kwargs