import matplotlib.pyplot as plt
import numpy as np

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