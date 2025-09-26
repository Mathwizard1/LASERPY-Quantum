import matplotlib.pyplot as plt
import numpy as np

from ..Components import TimeComponent

from .SimpleDevices import PhaseSample
from .SimpleDevices import SinglePhotonDetector


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
        self._field_buffer: List[np.complexfloating] = []
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


class AsymetricMachZehnderInterferometer:
    """
    Asymetric Mach-Zehnder Interferometer class
    """
    def __init__(self, t_delay):
        self.t_delay = t_delay
        """ time delay of pulse"""

        self.time = None

        # Arm phase change
        self.phase_sample_long = PhaseSample()
        self.phase_sample_short = PhaseSample()

        self.SPD_1 = SinglePhotonDetector(np.pi, name= "D1(0)")
        self.SPD_2 = SinglePhotonDetector(name= "D2(1)")

    def adjust_arm_phases(self, long_arm_phase= 0, short_arm_phase= 0):
        """ Adjust component values """

        self.phase_sample_long.set_value(long_arm_phase)
        self.phase_sample_short.set_value(short_arm_phase)

    def adjust_SPD_ClickPhases(self, SPD1_phase= 0, SPD2_phase= 0):
        """ Adjust SPD click phases """

        self.SPD_1.set_value(SPD1_phase)
        self.SPD_2.set_value(SPD2_phase)

    def interference(self, E_t1, E_t2):
        """
        Simulate inteference
        """

        # Optical field after passing through arms (phase changes)
        E1 = self.phase_sample_long(E_t1)
        E2 = self.phase_sample_short(E_t2)

        #print("Phase changes:", np.angle(E_t1), np.angle(E1), np.angle(E_t2), np.angle(E2))

        # Intensity data
        I1 = np.abs(E1) ** 2
        I2 = np.abs(E2) ** 2
        E1E2_2 = 2 * np.sqrt(I1 * I2)

        return (I1 + I2, E1E2_2, np.angle(E1) - np.angle(E2))

    def reset(self):
        self.SPD_1.reset()
        self.SPD_2.reset()

    def simulate(self, signal, time):
        """
        Simulate inteference with time delay for Differential Phase Shifted keys
        """
        delt_idx = time_to_index(time, self.t_delay)
        self.time = np.array(time[:-delt_idx])

        num_values = len(time)
        t_idx = 0
        while(t_idx + delt_idx < num_values):
            interference_data = self.interference(signal[t_idx], signal[t_idx + delt_idx])
            
            # Send interfered signal to detectors
            self.SPD_1(interference_data)
            self.SPD_2(interference_data)

            t_idx += 1

    def plot_SPD_data(self):
        """
        Plot the simulation data from Detectors
        """
        plt.figure(figsize=(12, 6)) # Create a figure for the plot
        plt.ylabel(r"Intensity ($W/m^{2}$)")
        plt.xlabel(r"time ($s$)")

        # Magnitude plot
        plt.plot(self.time, self.SPD_1.values(), label= self.SPD_1.name)
        plt.plot(self.time, self.SPD_2.values(), label= self.SPD_2.name)

        plt.grid()
        plt.legend()
        plt.show()