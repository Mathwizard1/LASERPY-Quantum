import matplotlib.pyplot as plt
import numpy as np

class PhaseSample:
    """
    PhaseSample class
    """
    def __init__(self, phase_delay= 0):
        phase_delay = np.mod(phase_delay, 2 * np.pi)
        self.phi = np.exp(1j * phase_delay)
        """ Phase delay """

    def set_value(self, phase_delay):
        phase_delay = np.mod(phase_delay, 2 * np.pi)
        self.phi = np.exp(1j * phase_delay)

    def __call__(self, E):
        return self.phi * E

class SinglePhotonDetector:
    """
    Single Photon Detector class
    """
    def __init__(self, click_phase= 0, name= "SPD"):
        self.name= name

        self.click_phase = click_phase
        """ Phase set for SPD click """

        self.interference_data = []

    def set_value(self, click_phase):
        self.click_phase = click_phase

    def __call__(self, signal: tuple[float,float,float]):
        """
        To simulate Intensity data according to the phase set for click
        """
        signal_abs, signal_diff, signal_phi = signal
        signal_data = signal_abs + signal_diff * np.cos(signal_phi + self.click_phase)

        self.interference_data.append(signal_data)

    def reset(self):
        self.interference_data.clear()

    def values(self):
        return np.array(self.interference_data)