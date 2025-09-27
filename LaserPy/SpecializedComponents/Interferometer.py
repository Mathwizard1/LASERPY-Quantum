from __future__ import annotations

import numpy as np

from ..Components.Component import Component
from ..Components import Clock

from .PhotonDetector import SinglePhotonDetector

from collections import namedtuple

from .SimpleDevices import PhaseSample
from .SimpleDevices import BeamSplitter

from ..Constants import ERR_TOLERANCE

class AsymmetricMachZehnderInterferometer(Component):
    """
    AsymmetricMachZehnderInterferometer class
    """

    # Handling multiport SinglePhotonDetector
    SPD = namedtuple('SPD', ['target_phase', 'SinglePhotonDetector'])

    def __init__(self, clock:Clock, time_delay:float, splitting_ratio:float = 0.5,
                detector_port_phases: tuple[float,...] = (0.0, np.pi),
                save_simulation: bool = False,
                name: str = "default_asymmetric_machzehnder_interferometer"):
        super().__init__(name)

        # Simulation parameters
        self._save_simulation = save_simulation

        # AMZI parameters
        self._time_delay = time_delay
        self._beam_splitter = BeamSplitter()

        # Phase controls
        self._short_arm_phase = PhaseSample(name="short_arm_phase")
        self._long_arm_phase = PhaseSample(name="long_arm_phase")

        # Measure ports
        rad_to_deg = 180 / np.pi

        self._SPDs: list[AsymmetricMachZehnderInterferometer.SPD] = []
        """single photon detectors list for AsymmetricMachZehnderInterferometer"""
        for port_phase in detector_port_phases:
            _SPD = SinglePhotonDetector(self._save_simulation, name=f"SPD_{str(int(port_phase * rad_to_deg))}")
            self._SPDs.append(self.SPD(target_phase= port_phase, SinglePhotonDetector= _SPD))

        self._electric_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        """electric_field data for AsymmetricMachZehnderInterferometer"""

        self._intensity: float = 0.0
        """intensity data for AsymmetricMachZehnderInterferometer"""

        # Delay buffer
        self._buffer_size: int = int(time_delay / clock.dt)
        self._field_buffer: list[np.complexfloating] = list([ERR_TOLERANCE * np.exp(1j * 0)] * self._buffer_size)

    def reset(self, splitting_ratio: float = 0.5, save_simulation: bool = False):
        """AsymmetricMachZehnderInterferometer reset method"""
        #return super().reset()
        pass

        #TODO propagate the changes

    def set(self, clock: Clock, time_delay: float, detector_port_phases: tuple[float,...] = (0.0, np.pi)):
        """AsymmetricMachZehnderInterferometer set method"""
        #return super().set()

        #TODO propagate the changes
        pass

    def simulate(self, electric_field: np.complexfloating):
        """AsymmetricMachZehnderInterferometer simulate method"""
        #return super().simulate(clock)
        pass

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