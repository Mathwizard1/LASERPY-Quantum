import numpy as np

from .Component import Clock

class NoNoise:
    """
    NoNoise class
    """
    def __init__(self, noise_name:str="default_no_noise"):
        self.noise_name = noise_name

    def __call__(self):
        """NoNoise __call__ method to override"""
        return 0

class LangevinNoise(NoNoise):
    """
    LangevinNoise class
    """
    def __init__(self, Mu: int, Std_dev: int, noise_name: str = "default_langevin_noise"):
        super().__init__(noise_name)

        self._Mu = Mu
        self._Std_dev = Std_dev

    def __call__(self):
        """LangevinNoise __call__ method"""
        return np.random.normal(loc=self._Mu, scale=self._Std_dev)

class ArbitaryWave:
    """
    ArbitaryWave class
    """
    def __init__(self, signal_name:str, t_unit:float|None=None, central_offset:float=0.0, total_spread:float=1.0):
        self.name = signal_name

        self._t_unit = t_unit
        self._central_offset = central_offset
        self._signal_spread = 0.5 * total_spread 

    def __call__(self, t, args=None):
        """ArbitaryWave __call__ method"""
        if(self._t_unit):
            t = np.mod(t, self._t_unit)
        return self.WaveSignal(t, args)
    
    def WaveSignal(self, t, args):
        """ArbitaryWave WaveSignal method to override"""
        return 0

class ArbitaryWaveGenerator:
    """
    ArbitaryWaveGenerator class
    """
    def __init__(self, name:str="default_awg_component"):
        self.name = name

        self.signals = {}
        """Signals dictionary for ArbitaryWaves"""

    def reset(self):
        """ArbitaryWaveGenerator reset method"""
        self.signals.clear()

    def set(self, arbitarywaves:ArbitaryWave|tuple[ArbitaryWave,...]):
        """ArbitaryWaveGenerator set method"""
        if(isinstance(arbitarywaves, ArbitaryWave)):
            arbitarywaves = (arbitarywaves,)

        for arbitarywave in arbitarywaves:
            self.signals[arbitarywave.name] = arbitarywave

    def simulate(self, clock:Clock, signal_keys:str|tuple[str,...], args=None) -> float:
        """ArbitaryWaveGenerator simulate method"""
        if(isinstance(signal_keys, str)):
            return self.signals[signal_keys](clock.t, args)
        else:
            superimposed_signal = 0
            for signal_key in signal_keys:
                superimposed_signal += self.signals[signal_key](clock.t, args)
            return superimposed_signal