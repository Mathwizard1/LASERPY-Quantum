import numpy as np

from ..Components.Component import Component

from ..Constants import ERR_TOLERANCE

class PhaseSample(Component):
    """
    PhaseSample class
    """
    def __init__(self, phase_delay: float = 0.0, name: str = "default_phase_sample"):
        super().__init__(name)

        self._phase_interval = 2 * np.pi
        """phase interval for PhaseSample"""

        phase_delay = np.mod(phase_delay, self._phase_interval)
        self._phase_change = np.exp(1j * phase_delay)
        """phase change for PhaseSample"""

        self._electric_field: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        """electric_field data for PhaseSample"""

    def reset(self):
        """PhaseSample reset method"""
        #return super().reset()
        self._electric_field = ERR_TOLERANCE * np.exp(1j * 0)
        self._phase_interval = 2 * np.pi
        self._phase_change = np.exp(1j * 0)

    def set(self, phase_delay: float, phase_interval: float|None= None):
        """PhaseSample set method"""
        #return super().set()
        if(phase_interval):
            self._phase_interval = phase_interval
        phase_delay = np.mod(phase_delay, self._phase_interval)
        self._phase_change = np.exp(1j * phase_delay)

    def simulate(self, electric_field: np.complexfloating):
        """PhaseSample simulate method"""
        #return super().simulate(args)

        # Add phase change
        self._electric_field = self._phase_change * electric_field

    def input_port(self):
        """PhaseSample input port method"""
        #return super().input_port()
        kwargs = {'electric_field':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """PhaseSample output port method"""
        #return super().output_port(kwargs)
        kwargs['electric_field'] = self._electric_field
        return kwargs
    
class BeamSplitter(Component):
    """
    BeamSplitter class
    """
    def __init__(self, name: str = "default_beam_splitter"):
        super().__init__(name)
        # TODO beam splitter