from __future__ import annotations

import numpy as np

from ..Components.Component import Component
from ..Components import Clock

from .PhotonDetector import SinglePhotonDetector

#from collections import namedtuple

from .SimpleDevices import PhaseSample, Mirror
from .SimpleDevices import BeamSplitter

from ..Constants import EMPTY_FIELD
from ..Constants import FULL_PHASE_INTERVAL

# TODO multiport
# Handling multiport SinglePhotonDetector
# SPD = namedtuple('SPD', ['target_phase', 'SinglePhotonDetector'])

class AsymmetricMachZehnderInterferometer(Component):
    """
    AsymmetricMachZehnderInterferometer class
    """
    def __init__(self, clock:Clock, time_delay:float, 
                 splitting_ratio_ti:float = 0.5, splitting_ratio_tf:float = 0.5,
                save_simulation: bool = False, name: str = "default_asymmetric_machzehnder_interferometer"):
        super().__init__(name)

        # Simulation parameters
        self._save_simulation = save_simulation

        # AMZI parameters
        self._time_delay = time_delay
        self._input_beam_splitter = BeamSplitter(splitting_ratio_ti, name="input_beam_splitter")
        self._output_beam_joiner = BeamSplitter(splitting_ratio_tf, name="output_beam_joiner")

        # Phase controls
        self._mirror = Mirror(name=f"common_mirror")
        self._short_arm_phase_sample = PhaseSample(name="short_arm_phase_sample")
        self._long_arm_phase_sample = PhaseSample(name="long_arm_phase_sample")

        # Measure ports
        self._SPD0 = SinglePhotonDetector(self._save_simulation, name=f"SPD_0")
        self._SPD1 = SinglePhotonDetector(self._save_simulation, name=f"SPD_1")

        self._electric_field: np.complexfloating = EMPTY_FIELD
        """electric_field data for AsymmetricMachZehnderInterferometer"""

        self._intensity: float = 0.0
        """intensity data for AsymmetricMachZehnderInterferometer"""

        # Delay buffer
        self._buffer_size: int = max(1, int(time_delay / clock.dt))
        self._field_buffer: list[np.complexfloating] = []

    def reset(self, save_simulation: bool = False):
        """AsymmetricMachZehnderInterferometer reset method"""
        #return super().reset()
        pass

        #TODO propagate the changes

    def set(self, clock: Clock, time_delay: float, 
            splitting_ratio_ti: float = 0.5, splitting_ratio_tf: float = 0.5):
        """AsymmetricMachZehnderInterferometer set method"""
        #return super().set()

        # Beam splitters
        self._input_beam_splitter.set(splitting_ratio_ti)
        self._output_beam_joiner.set(splitting_ratio_tf)

        # Delay buffer
        self._buffer_size = max(1, int(time_delay / clock.dt))
        self._field_buffer.clear()

    def set_phases(self, short_arm_phase: float, long_arm_phase: float, 
                short_arm_phase_interval: float = FULL_PHASE_INTERVAL, long_arm_phase_interval: float = FULL_PHASE_INTERVAL):
        """AsymmetricMachZehnderInterferometer set phases method"""
        self._short_arm_phase_sample.set(short_arm_phase, phase_interval= short_arm_phase_interval)
        self._long_arm_phase_sample.set(long_arm_phase, phase_interval= long_arm_phase_interval)

    def simulate(self, electric_field: np.complexfloating):
        """AsymmetricMachZehnderInterferometer simulate method"""
        #return super().simulate(clock)

        # input field
        E_short, E_long = self._input_beam_splitter.simulate(electric_field)

        # long arm
        E_long = self._long_arm_phase_sample.simulate(E_long)
        E_long = self._mirror.simulate(E_long)

        # Handle buffer
        self._field_buffer.append(E_long)
        E_long = self._field_buffer.pop(0) if len(self._field_buffer) > self._buffer_size else EMPTY_FIELD

        # short arm
        E_short = self._mirror.simulate(E_short)
        E_short = self._short_arm_phase_sample.simulate(E_short)

        # Recombine
        electric_field, electric_field_port2 = self._output_beam_joiner.simulate(E_short, E_long)

    def input_port(self):
        """AsymmetricMachZehnderInterferometer input port method"""
        #return super().input_port()
        kwargs = {'electric_field':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """AsymmetricMachZehnderInterferometer output port method"""
        #return super().output_port(kwargs)
        kwargs['intensity'] = self._intensity
        kwargs['electric_field'] = self._electric_field
        return kwargs

class AsymmetricMachZehnder(TimeComponent):
    """
    AMZI component for time-bin encoding with your Laser.electric_field
    """
    def __init__(self, path_difference: float = 5e-9, splitting_ratio: float = 0.5,
                 insertion_loss_db: float = 3.0, name: str = "default_amzi"):
        super().__init__(name)
        
        # AMZI parameters
        self.path_difference: float = path_difference  # Time delay [s]
        self.splitting_ratio: float = splitting_ratio  # Power split ratio
        self.insertion_loss_db: float = insertion_loss_db  # Loss [dB]
        
        # Calculate transmission factors
        self.transmission_factor: float = np.sqrt(10 ** (-insertion_loss_db / 10))
        self.short_arm_amplitude: float = np.sqrt(1 - splitting_ratio) * self.transmission_factor
        self.long_arm_amplitude: float = np.sqrt(splitting_ratio) * self.transmission_factor
        
        # Phase controls
        self.short_arm_phase: float = 0.0
        self.long_arm_phase: float = 0.0
        
        # Fields
        self.input_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        self.short_arm_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        self.long_arm_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        self.combined_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        
        # Delay buffer
        self._field_buffer: list[np.complexfloating] = []
        self._buffer_size: int = 0
    
    def set_arm_phases(self, short_phase: float, long_phase: float):
        """Set phase delays for both arms"""
        self.short_arm_phase = np.mod(short_phase, 2 * np.pi)
        self.long_arm_phase = np.mod(long_phase, 2 * np.pi)
    
    def simulate(self, clock: Clock, electric_field: np.complexfloating = None):
        """Simulate AMZI with time-bin encoding"""
        if electric_field is not None:
            self.input_field = electric_field
        else:
            self.input_field = ERR_TOLERANCE * np.exp(1j * 0)
        
        # Initialize buffer
        if self._buffer_size == 0:
            self._buffer_size = max(1, int(self.path_difference / clock.dt))
            self._field_buffer = [ERR_TOLERANCE * np.exp(1j * 0)] * self._buffer_size
        
        # Short arm (immediate)
        short_phase_factor = np.exp(1j * self.short_arm_phase)
        self.short_arm_field = self.input_field * self.short_arm_amplitude * short_phase_factor
        
        # Long arm (delayed)
        self._field_buffer.append(self.input_field)
        delayed_field = self._field_buffer.pop(0) if len(self._field_buffer) > self._buffer_size else ERR_TOLERANCE * np.exp(1j * 0)
        
        long_phase_factor = np.exp(1j * self.long_arm_phase)
        self.long_arm_field = delayed_field * self.long_arm_amplitude * long_phase_factor
        
        # Combined output
        self.combined_field = self.short_arm_field + self.long_arm_field
    
    def input_port(self):
        return {'clock': None, 'electric_field': None}
    
    def output_port(self, kwargs: dict = {}):
        kwargs['electric_field'] = self.combined_field
        kwargs['short_arm_field'] = self.short_arm_field
        kwargs['long_arm_field'] = self.long_arm_field
        kwargs['combined_field'] = self.combined_field
        return kwargs