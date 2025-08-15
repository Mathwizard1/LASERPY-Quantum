from typing import Literal
from collections import namedtuple

import numpy as np

from enum import Enum

# General Scientific Constants
class universalConstants(float, Enum):
    charge = 1.602 * (1.0e-19)
    """
    single unit of charge of elctron / proton
    """

    h = 6.626 * (1.0e-34)
    """
    Plank's Constant 
    """

    c = 2.997 * (1.0e+8)
    """
    Speed of light in vacuum 
    """

ERR_TOLERANCE = 1e-12

#######################################
TAU_N = 0.74 * (1.0e-9)
""" Carrier lifetime (seconds) """

TAU_P = 0.74 * (1.0e-12)
""" Photon lifetime (seconds) """

G = 1.27 * (1.0e-12)
""" Differential gain coefficient (m^3 seconds^-1) """

EPSILON = 1.18 * (1.0e-23)    
""" Gain Compression factor (m^3) """

N_TRANSPARENT = 0.85 * (1.0e+24)         
""" Carrier density at transparency (m^-3) """

BETA = 0.5 * (1.0e-5)         
""" Spontaneous enhancement factor """

ALPHA = 2.7                 
""" Linewidth sample enhancement factor """

ETHA = 0.2                   
""" Differential quantum efficiency """

ACTV_VOLUME = 1.72 * (1.0e-17)          
""" Active layer volume (m^3) """

GAMMA_CAP = 0.27           
""" Mode confinement factor """

KAPPA = 1.13 * (1.0e+11)      
""" OIL coupling term (Hz) """

T0 = 300
""" Base Temperature (K) """

ROOM_TEMP = 300
""" Current Room Temperature (K) """

LASER_LAMBDA = 1550 * (1.0e-9)
""" Laser wavelength (m) """

LASER_FREQ = universalConstants.c.value / LASER_LAMBDA
""" Ideal free running frequency """

#######################################
I_TH = universalConstants.charge.value * ACTV_VOLUME / TAU_N * (N_TRANSPARENT  + 1 / (G * GAMMA_CAP * TAU_P))
""" Threshold Current for Lasing """

#######################################
def phase_modulation_current(dPhi, dt):
    """
    Delta Current needed for phase change\n
    dPhi: radians, dt: sec
    """
    return (2 * universalConstants.charge.value * ACTV_VOLUME) / (ETHA * ALPHA * GAMMA_CAP * G * dt**2) * dPhi

#######################################
class Component:
    """
    Component class
    """
    def __init__(self, name:str = "default_component"):
        self.name = name
        self.simulation_data = []

    def reset(self):
        """Component reset method to override"""
        print("Component reset method")

    def set(self):
        """Component set method to override"""
        print("Component set method")

    def update(self):
        """Component update method to override"""
        print("Component update method")

    def input_port(self, args= None):
        """Component input port method to override"""
        print("Component input method")   

    def output_port(self, args= None):
        """Component output port method to override"""
        print("Component output method")

class Clock(Component):
    """
    Clock class
    """
    def __init__(self, dt:float, t:float =0, t_final:float =None, name = "default_clock"):
        super().__init__(name)
        self.dt = dt
        self.t = t
        self.t_final = dt
        if(t_final):
            self.t_final = t_final
        self.running = True

    def reset(self, set_t0_time= False):
        #return super().reset()
        if(set_t0_time):
            self.t = 0
        self.running = True

    def set(self, t_final:float):
        #return super().set()
        self.t_final = t_final

    def update(self):
        #return super().update()
        if(self.t_final and (self.t >= self.t_final)):
            self.running = False
            return None
        self.t += self.dt

class PhysicalComponent(Component):
    """
    PhysicalComponent class
    """
    def __init__(self, name = "default_physical_component"):
        super().__init__(name)

    def simulate(self, clock:Clock):
        """PhysicalComponent simulate method to override"""
        print("PhysicalComponent simulate method")  

class Connection(PhysicalComponent):
    """
    Connection class
    """
    def __init__(self, input_components:Component|tuple[Component], output_components:Component|tuple[Component] = (), name= "default_connection"):
        super().__init__(name)
        if(isinstance(input_components, Component)):
            input_components = tuple(input_components)
        self.input_components = input_components

        if(isinstance(output_components, Component)):
            output_components = tuple(output_components)
        self.output_components = output_components

    def simulate(self, clock:Clock):
        #return super().simulate(clock)
        pass

class Simulator(Component):
    def __init__(self, simulation_clock:Clock, name = "default_simulator"):
        super().__init__(name)
        self.simulation_clock = simulation_clock

    def set(self, connection_simulations:tuple[Connection]):
        #return super().set()
        self.connection_simulations = connection_simulations

    def update(self):
        #return super().update()
        while(self.simulation_clock.running):
            for connection in self.connection_simulations:
                    connection.simulate(self.simulation_clock)
            self.simulation_clock.update()
        print("Simulations Complete")

#######################################
class ArbitaryWave:
    """
    Base custom signals for current
    """
    def __init__(self, signal_name:str, t_unit:float= None, central_offset:float = 0.0, total_spread:float = 1.0):
        self.name = signal_name
        self.t_unit = t_unit
        self.central_offset = central_offset
        self.signal_spread = 0.5 * total_spread 

    def __call__(self, t, args= None):
        """
        For arbitary signal output wrapped t ∈ (0, t_unit)
        """
        if(self.t_unit):
            t = np.mod(t, self.t_unit)
        return self.WaveSignal(t, args)
    
    def WaveSignal(self, t, args):
        """
        method override for actual wave
        """
        return 0

class LangevinNoise:
    """ 
    Langevin noise sources 
    """
    def __init__(self, Mu:float =0, Std_dev:float= 0, noise_name:str ="default_langevin_noise"):
        self.noise_name = noise_name
        self.Mu = Mu
        self.Std_dev = Std_dev

    def __call__(self):
        return np.random.normal(loc= self.Mu, scale= self.Std_dev)

#######################################
class ArbitaryWaveGenerator(PhysicalComponent):
    """
    ArbitaryWaveGenerator class
    """
    def __init__(self, name="default_AWG"):
        super().__init__(name)
        self.signal_waves = {}

    def reset(self):
        self.signal_waves.clear()

    def set(self, signal_objects: ArbitaryWave | list[ArbitaryWave]):
        if(isinstance(signal_objects, list)):
            for signal_object in signal_objects:
                self.signal_waves[signal_object.name] = signal_object
        else:
            signal_object = signal_objects
            self.signal_waves[signal_object.name] = signal_object

    def simulate(self, clock:Clock, signal_key:str, args= None):
        #return super().simulate(clock, args)
        if(signal_key in self.signal_waves):
            return self.signal_waves[signal_key](clock.t, args)
        return 0

class CurrentDriver(ArbitaryWaveGenerator):
    """ 
    Current Driver class
    """
    def _init__(self, name = "default_current_driver"):
        super().__init__(name)
        self.I_t = 0
        self.modulation_function = None
        self.modulation_ON = []
        self.modulation_OFF = []

    def set(self, modulation_OFF: list[ArbitaryWave], modulation_ON: list[ArbitaryWave]= [], modulation_function:ArbitaryWave = None):
        self.modulation_function = modulation_function

        for arbitarywaves in modulation_ON:
            self.modulation_ON.append(arbitarywaves.name)
        #print(self.modulation_ON)

        for arbitarywaves in modulation_OFF:
            self.modulation_OFF.append(arbitarywaves.name)
        #print(self.modulation_OFF)

        super().reset()
        super().set(modulation_ON + modulation_OFF)

    def simulate(self, clock:Clock, args=None):
        #return super().simulate(clock, signal_key, args)
        I_t = 0
        signal_list = []

        if(self.modulation_function and self.modulation_function(clock.t)):
            signal_list = self.modulation_ON
        else:
            signal_list = self.modulation_OFF

        for signal_key in signal_list:
            I_t += super().simulate(signal_key, args)
        self.I_t = I_t
    
    def output_port(self, args=None):
        #return super().output_port(args)
        return self.I_t

class Laser(Component):
    def __init__(self, fr_freq =LASER_FREQ, N0 =N_TRANSPARENT, S0 =ERR_TOLERANCE, Phi0=ERR_TOLERANCE, name="default_laser"):
        super().__init__(name)

        self.N0 = N0
        self.S0 = S0
        self.Phi0 = Phi0

        # Lagevin Noise Terms
        self.Fn_t = LangevinNoise()
        self.Fs_t = LangevinNoise()
        self.Fphi_t = LangevinNoise()

        self.fr_freq = fr_freq
        """
        free running frequency
        """

        self.N_t = self.N0
        """
        Number of Carriers
        """

        self.S_t = self.S0
        """
        Photon density
        """

        self.Phi_t = self.Phi0
        """
        Optical phase
        """

        self.dPhi = 0
        """
        Stored instantaneous delta phase change
        """

        self.E_t = 0
        """
        Laser Optical field (complex)
        """
    
    def set(self, N0, S0, Phi0, fr_freq):
        self.N0 = N0
        self.S0 = S0
        self.Phi0 = Phi0

        self.fr_freq = fr_freq

    def set_Langevin_Noise(self, Fn_t:LangevinNoise, Fs_t:LangevinNoise, Fphi_t:LangevinNoise):
        self.Fn_t = Fn_t
        self.Fs_t = Fs_t
        self.Fphi_t = Fphi_t

    def reset(self):
        """
        Reset all data
        """
        self.N_t = self.N0
        self.S_t = self.S0
        self.Phi_t = self.Phi0

        self.dPhi = 0
        self.E_t = 0

    def simulate(self, I_t, t, dt):
        """
        Update N, S, phi and return current value
        """
        temp_N_t = self.N_t + self.dN_dt(I_t, self.Fn_t(t)) * dt 
        temp_S_t = self.S_t + self.dS_dt(self.Fs_t(t)) * dt
        self.dPhi = self.dPhi_dt(self.Fphi_t(t)) * dt

        """ time step update """ 
        self.N_t = temp_N_t
        self.S_t = temp_S_t
        self.Phi_t += self.dPhi

        self.E_t = np.sqrt(self.Power(self.S_t)) * np.exp(1j * self.Phi_t)

    def dN_dt(self, I_t, Fn_t):
        """
        delta Number of Carriers
        """
        val = I_t / (universalConstants.charge.value * ACTV_VOLUME) - self.N_t / TAU_N - G * ((self.N_t - self.N0) / (1.0 + EPSILON * self.S_t)) * self.S_t + Fn_t
        return val

    def dS_dt(self, Fs_t):
        """
        delta Photon density
        """
        val = GAMMA_CAP * G * ((self.N_t - self.N0) / (1.0 + EPSILON * self.S_t)) * self.S_t - self.S_t / TAU_P + GAMMA_CAP * BETA * self.N_t / TAU_N + Fs_t
        return val

    def dPhi_dt(self, Fphi_t):
        """
        delta Optical phase
        """
        val = (ALPHA / 2.0) * (GAMMA_CAP * G * (self.N_t - self.N0) - 1.0 / TAU_P) + Fphi_t
        return val

    def Power(self, S_t) -> np.ndarray:
        """ 
        Power of laser 
        """
        Pval = np.array(S_t) * ACTV_VOLUME * ETHA * universalConstants.h.value * self.fr_freq / (2 * GAMMA_CAP * TAU_P)
        return Pval

    def output_port(self, args=None):
        #return super().output_port(args)
        return self.E_t

class MachZehnderInterferometer(Component):
    def __init__(self, name="default_component"):
        super().__init__(name)

class AsymmetricMachZehnderInterferometer(Component):
    def __init__(self, name="default_component"):
        super().__init__(name)

class SinglePhotonDetector(Component):
    def __init__(self, name="default_component"):
        super().__init__(name)