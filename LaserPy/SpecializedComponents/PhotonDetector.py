import numpy as np

from ..Components import Clock
from ..Components import DataComponent

class SinglePhotonDetector(DataComponent):
    """
    SinglePhotonDetector class
    """
    def __init__(self, save_simulation: bool = False, name: str = "default_single_photon_detector"):
        super().__init__(save_simulation, name)

        self.intensity = 0
        """intensity data for SinglePhotonDetector"""

        self.photon_count = 0
        """photon count data for SinglePhotonDetector"""
    
        self.clicked: int = 0
        """clicked data for SinglePhotonDetector"""

        # Data storage
        if save_simulation:
            self._simulation_data = {'intensity': []}#, 'photon_count': [], 'clicked': []}
            self._simulation_data_units = {'intensity': r' $(W/m^2)$'}#, 'photon_count': r' $(counts)$', 'clicked': r' $(boolean)$'}

    def reset(self):
        """SinglePhotonDetector reset method"""
        #return super().reset()
        self.intensity = 0
        self.photon_count = 0
        self.clicked = False

    def simulate(self, args=None):
        """SinglePhotonDetector simulate method"""
        #return super().simulate(args)
        # TODO implement SPD
        pass

    def input_port(self):
        """SinglePhotonDetector input port method"""
        #return super().input_port()
        kwargs = {'intensity': None}
        return kwargs

class PhaseSensitiveSPD(SinglePhotonDetector):
    """
    PhaseSensitiveSPD class
    """
    def __init__(self, target_phase: float = 0.0, phase_tolerance: float = 0.1, save_simulation: bool = False, name: str = "default_phase_sensitive_SPD"):
        super().__init__(save_simulation, name)

        self._target_phase = target_phase
        """target phase data for PhaseSensitiveSPD"""

        self._phase_tolerance = phase_tolerance
        """phase error data for PhaseSensitiveSPD"""

    def set(self, target_phase: float = 0.0, phase_tolerance: float = 0.1):
        """PhaseSensitiveSPD set method"""
        #return super().set()
        self._target_phase = target_phase
        self._phase_tolerance = phase_tolerance

    def simulate(self, electric_field: np.complexfloating):
        """PhaseSensitiveSPD simulate method"""
        #return super().simulate(args)
        E_magnitude = np.abs(electric_field)
        E_angle = np.angle(electric_field)

        self.intensity = max(np.square(E_magnitude) * np.cos(E_angle - self._target_phase), 0.0)

        # TODO implement clicked
        # TODO implement photon count

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """PhaseSensitiveSPD input port method"""
        #return super().input_port()
        kwargs = {'electric_field': None}
        return kwargs