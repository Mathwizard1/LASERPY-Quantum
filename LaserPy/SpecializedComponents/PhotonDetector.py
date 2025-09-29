import numpy as np

from ..Components import Clock
from ..Components import DataComponent

from ..Constants import FULL_PHASE_INTERVAL

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
        self._simulation_data = {'intensity': []}#, 'photon_count': [], 'clicked': []}
        self._simulation_data_units = {'intensity': r" $(W/m^2)$"}#, 'photon_count': r' $(counts)$', 'clicked': r' $(boolean)$'}

    def reset_data(self):
        """SinglePhotonDetector reset_data method""" 
        # Value reset  
        self.intensity = 0
        self.photon_count = 0
        self.clicked = False

        return super().reset_data()

    def reset(self, save_simulation: bool = False):
        """SinglePhotonDetector reset method"""        
        return super().reset(save_simulation)

    def simulate(self, electric_field: np.complexfloating):
        """SinglePhotonDetector simulate method"""
        #return super().simulate(args)
        

        self.intensity = np.square(np.abs(electric_field))

        # TODO implement clicked
        # TODO implement photon count

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """SinglePhotonDetector input port method"""
        #return super().input_port()
        kwargs = {'electric_field': None}
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


        if(self._save_simulation):
            self.store_data()