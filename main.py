import numpy as np

from LaserPy import Clock
from LaserPy import Connection, Simulator
from LaserPy import ArbitaryWave, ArbitaryWaveGenerator
from LaserPy import CurrentDriver
from LaserPy import Laser

from LaserPy import AsymmetricMachZehnderInterferometer

# Control Constants (all in SI units)
modulation_bits = [0] * 10
dt = 1e-12
t_unit = 1e-9
t_final = t_unit * len(modulation_bits)
#sampling_rate = 2 * dt

# Current Constants
I_th = 0.0178
MASTER_BASE_DC = 1.4 * I_th

# Time duration are in fration of t_unit
MASTER_AC_DURATION = 0.4
MASTER_AC = 0.3 * I_th

# Time duration are in fration of t_unit
SLAVE_DC_DURATION = 0.6
SLAVE_DC = 0.85 * I_th

SLAVE_PULSE = 1.15 * I_th

# Steady above lasing current
class master_Base_signal(ArbitaryWave):
    def __init__(self, signal_name: str, t_unit: float | None = None, central_offset: float = 0, total_spread: float = 1):
        super().__init__(signal_name, t_unit, central_offset, total_spread)

    def WaveSignal(self, t, args):
        return MASTER_BASE_DC

mBase = master_Base_signal("mBase", t_unit)

# Modulation current
class master_Modulation_signal(ArbitaryWave):
    def __init__(self, signal_name: str, t_unit: float | None = None, central_offset: float = 0, total_spread: float = 1):
        super().__init__(signal_name, t_unit, central_offset, total_spread)
        self.sign = 1

    def WaveSignal(self, t, args):
        if(t <= dt):
            self.sign *= -1
        elif(t > self._t_unit * (0.5 - self._signal_spread) and t < self._t_unit * (0.5 + self._signal_spread)): # type: ignore
            return MASTER_AC * self.sign
        return super().WaveSignal(t, args)

mModulation = master_Modulation_signal("mModulation", t_unit, total_spread=MASTER_AC_DURATION)

# Pulse below lasing and above lasing current
class slave_Base_signal(ArbitaryWave):
    def __init__(self, signal_name: str, t_unit: float | None = None, central_offset: float = 0, total_spread: float = 1):
        super().__init__(signal_name, t_unit, central_offset, total_spread)

    def WaveSignal(self, t, args):
        if(t > self._t_unit * (0.5 - self._signal_spread) and t < self._t_unit * (0.5 + self._signal_spread)): # type: ignore
            return SLAVE_DC
        return SLAVE_PULSE

sBase = slave_Base_signal("sBase", t_unit, total_spread=SLAVE_DC_DURATION)

AWG = ArbitaryWaveGenerator()
AWG.set((mBase, mModulation))
AWG.set(sBase)

class ModulationFunction(ArbitaryWave):
    def __init__(self, signal_name: str, t_unit: float | None = None, central_offset: float = 0, total_spread: float = 1):
        super().__init__(signal_name, t_unit, central_offset, total_spread)
        self.idx = 0
        self.modulation_bit = 1

    def WaveSignal(self, t, args):
        if(t <= dt):
            self.idx += 1
            self.idx = self.idx % len(modulation_bits)
        return modulation_bits[self.idx] == self.modulation_bit

mod_func = ModulationFunction("modulation_function", t_unit)

############################################################################

current_driver1 = CurrentDriver(AWG)
current_driver1.set(mBase, (mBase, mModulation), mod_func)

current_driver2 = CurrentDriver(AWG)
current_driver2.set(sBase)

master_laser = Laser(name= "master_laser")
slave_laser = Laser(name= "slave_laser")

simulator_clock = Clock(dt)
simulator_clock.set(t_final)

AMZI = AsymmetricMachZehnderInterferometer(simulator_clock, time_delay= t_unit)

simulator = Simulator(simulator_clock)

simulator.set((
    Connection(simulator_clock, (current_driver1, current_driver2)),
    Connection(current_driver1, master_laser),
    Connection((current_driver2, master_laser), slave_laser),
    Connection(slave_laser, AMZI),
))

simulator.simulate()

#time_data = simulator.get_data()
#master_laser.display_data(time_data)
#slave_laser.display_data(time_data)

############################################################################

simulator.reset(True)

modulation_bits = [0,0,1,0,1,0,1,1,1,0]
t_final = t_unit * len(modulation_bits)

simulator_clock.set(t_final, t=0)

slave_laser.set_master_Laser(master_laser)

simulator.simulate()
time_data = simulator.get_data()

master_laser.display_data(time_data)
slave_laser.display_data(time_data)

AMZI.display_SPD_data(time_data)
