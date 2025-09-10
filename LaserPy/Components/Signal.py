import numpy as np

from .Component import Clock
from .Component import TimeComponent

class LangevinNoise:
    """
    LangevinNoise class
    """
    def __init__(self, Mu:float=0, Std_dev:float=0, noise_name:str="default_langevin_noise"):
        self.noise_name = noise_name
        self.Mu = Mu
        self.Std_dev = Std_dev

    def __call__(self):
        return np.random.normal(loc=self.Mu, scale=self.Std_dev)


class ArbitaryWave:
    """
    ArbitaryWave class
    """
    def __init__(self, signal_name:str, t_unit:float|None=None, central_offset:float=0.0, total_spread:float=1.0):
        self.name = signal_name
        self.t_unit = t_unit
        self.central_offset = central_offset
        self.signal_spread = 0.5 * total_spread 

    def __call__(self, t, args):
        if(self.t_unit):
            t = np.mod(t, self.t_unit)
        return self.WaveSignal(t, args)
    
    def WaveSignal(self, t, args):
        """ArbitaryWave WaveSignal method to override"""
        return 0

class ArbitaryWaveGenerator(TimeComponent):
    """
    ArbitaryWaveGenerator class
    """
    def __init__(self, name:str="default_awg_component"):
        super().__init__(name)
        self.signals = {}

    def reset(self):
        """ArbitaryWaveGenerator reset method"""
        #return super().reset()
        self.signals.clear()

    def set(self, arbitarywaves:ArbitaryWave|tuple[ArbitaryWave,...]):
        """ArbitaryWaveGenerator set method"""
        #return super().set()
        if(isinstance(arbitarywaves, ArbitaryWave)):
            arbitarywaves = (arbitarywaves,)

        for arbitarywave in arbitarywaves:
            self.signals[arbitarywave.name] = arbitarywave

    def simulate(self, clock:Clock, signal_key:str, args=None):
        """ArbitaryWaveGenerator simulate method"""
        #return super().simulate(clock)
        if(signal_key in self.signals):
            return self.signals[signal_key](clock.t, args)
        return 0