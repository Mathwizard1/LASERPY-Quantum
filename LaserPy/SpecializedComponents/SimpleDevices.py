import numpy as np

from ..Components import Clock
from ..Components import TimeComponent
from ..Components import DataComponent

from ..Constants import ERR_TOLERANCE

class PhaseSample(TimeComponent):
    """
    PhaseSample class
    """
    def __init__(self, phase_delay: float = 0.0, name: str = "default_phase_sample"):
        super().__init__(name)

        self._phase_interval = 2 * np.pi
        """phase interval for PhaseSample"""

        phase_delay = np.mod(phase_delay, self._phase_interval)
        self._phase_change = np.exp(1j * phase_delay)
        """ Phase delay for PhaseSample"""

        self._data: np.complexfloating = ERR_TOLERANCE * np.exp(1j * 0)
        """electric_field data for PhaseSample"""

    def reset(self):
        """PhaseSample reset method"""
        #return super().reset()
        self._data = ERR_TOLERANCE * np.exp(1j * 0)
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
        self._data = self._phase_change * electric_field

    def input_port(self):
        """PhaseSample input port method"""
        #return super().input_port()
        kwargs = {'electric_field':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """PhaseSample output port method"""
        #return super().output_port(kwargs)
        kwargs['electric_field'] = self._data
        return kwargs

class SinglePhotonDetector(DataComponent):
    """
    SinglePhotonDetector class
    """
    def __init__(self, target_phase: float = 0.0, phase_tolerance: float = 0.1, save_simulation: bool = False, name: str = "default_data_component"):
        super().__init__(save_simulation, name)

        self.intensity = 0
        """intensity data for SinglePhotonDetector"""

        self.photon_count = 0
        """photon count data for SinglePhotonDetector"""
    
        self.clicked: int = 0
        """clicked data for SinglePhotonDetector"""

        # Data storage
        if save_simulation:
            self._simulation_data = {'intensity': [], 'photon_count': [], 'clicked': []}
            self._simulation_data_units = {'intensity': r' $(W/m^2)$', 
                                           'photon_count': r' $(counts)$', 'clicked': r' $(boolean)$'}

        self._target_phase = target_phase
        """target phase data for SinglePhotonDetector"""

        self._phase_tolerance = phase_tolerance
        """phase error data for SinglePhotonDetector"""

    def reset(self):
        """SinglePhotonDetector reset method"""
        #return super().reset()
        self.intensity = 0
        self.photon_count = 0
        self.clicked = False

    def set(self, target_phase: float = 0.0, phase_tolerance: float = 0.1):
        """SinglePhotonDetector set method"""
        #return super().set()
        self._target_phase = target_phase
        self._phase_tolerance = phase_tolerance

    def simulate(self, electric_field: np.complexfloating):
        """SinglePhotonDetector simulate method"""
        #return super().simulate(args)
        E_magnitude = np.abs(electric_field)
        E_angle = np.angle(electric_field)

        self.clicked = int(np.abs(E_angle - self._target_phase) <= self._phase_tolerance)
        self.intensity = max(np.square(E_magnitude) * np.cos(E_angle - self._target_phase), 0.0)

        # TODO implement photon count

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """SinglePhotonDetector input port method"""
        #return super().input_port()
        kwargs = {'electric_field': None}
        return kwargs