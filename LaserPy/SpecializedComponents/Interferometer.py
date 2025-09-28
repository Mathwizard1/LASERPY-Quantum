from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from ..Components.Component import Component
from ..Components import Clock

from .PhotonDetector import SinglePhotonDetector

#from collections import namedtuple

from .SimpleDevices import PhaseSample, Mirror
from .SimpleDevices import BeamSplitter

from ..Constants import EMPTY_FIELD
from ..Constants import FULL_PHASE_INTERVAL

from ..Constants import FIG_WIDTH, FIG_HEIGHT

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

        self._electric_field_port2: np.complexfloating = EMPTY_FIELD
        """electric_field_port2 data for AsymmetricMachZehnderInterferometer"""

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
        self._electric_field, self._electric_field_port2 = self._output_beam_joiner.simulate(E_short, E_long)
        
        # Photon Detection
        self._SPD0.simulate(self._electric_field)
        self._SPD1.simulate(self._electric_field_port2)

    def input_port(self):
        """AsymmetricMachZehnderInterferometer input port method"""
        #return super().input_port()
        kwargs = {'electric_field':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """AsymmetricMachZehnderInterferometer output port method"""
        #return super().output_port(kwargs)
        kwargs['electric_field'] = self._electric_field
        kwargs['electric_field_port2'] = self._electric_field_port2
        return kwargs
    
    def display_SPD_data(self, time_data:np.ndarray):
        """AsymmetricMachZehnderInterferometer display_SPD_data method"""        
        
        # Handle cases
        if(not self._save_simulation):
            print(f"{self.name} cannot display data")
            return

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        key_tuple = tuple(self._simulation_data_units)
        if(simulation_keys):
            key_tuple = simulation_keys

        max_hf_plots = 1 + (len(key_tuple) >> 1)
        sub_plot_idx = 1
        for key in key_tuple:
            plt.subplot(max_hf_plots, 2, sub_plot_idx)
            plt.plot(time_data, np.array(self._simulation_data[key]), label=f"{key}")

            plt.xlabel(r"Time $(s)$")
            plt.ylabel(key.capitalize() + self._simulation_data_units[key])
            
            plt.grid()
            plt.legend()
            sub_plot_idx += 1

        plt.tight_layout()
        plt.show()

    def get_SPD_data(self):
        # TODO get SPD data
        pass