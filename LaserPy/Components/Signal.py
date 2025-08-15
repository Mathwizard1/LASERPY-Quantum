import numpy as np

class ArbitaryWave:
    def __init__(self, signal_name:str, t_unit:float= None, central_offset:float = 0.0, total_spread:float = 1.0):
        self.name = signal_name
        self.t_unit = t_unit
        self.central_offset = central_offset
        self.signal_spread = 0.5 * total_spread 

    def __call__(self, t, args= None):
        if(self.t_unit):
            t = np.mod(t, self.t_unit)
        return self.WaveSignal(t, args)
    
    def WaveSignal(self, t, args):
        return 0

class LangevinNoise:
    def __init__(self, Mu:float =0, Std_dev:float= 0, noise_name:str ="default_langevin_noise"):
        self.noise_name = noise_name
        self.Mu = Mu
        self.Std_dev = Std_dev

    def __call__(self):
        return np.random.normal(loc= self.Mu, scale= self.Std_dev)
