from .benchmark import benchmark

############################################################################
from LaserPy_Quantum import Clock
from LaserPy_Quantum import Connection, Simulator
from LaserPy_Quantum import ArbitaryWave, ArbitaryWaveGenerator
from LaserPy_Quantum import CurrentDriver
from LaserPy_Quantum import Laser

############################################################################
dt = 1e-12
t_unit = 1e-9
t_final = 10 * 1e-9
#sampling_rate = 2 * dt

# Current Constants
I_th = 0.0178
MASTER_BASE_DC = 1.4 * I_th

class master_Base_signal(ArbitaryWave):
    def __init__(self, signal_name: str, t_unit: float | None = None, central_offset: float = 0, total_spread: float = 1):
        super().__init__(signal_name, t_unit, central_offset, total_spread)

    def WaveSignal(self, t, args):
        return MASTER_BASE_DC

mBase = master_Base_signal("mBase", t_unit)

AWG = ArbitaryWaveGenerator()
AWG.set(mBase)

############################################################################

current_driver1 = CurrentDriver(AWG)
current_driver1.set(mBase)

master_laser = Laser(name= "master_laser")

simulator_clock = Clock(dt)
simulator_clock.set(t_final)

simulator = Simulator(simulator_clock)

simulator.set((
    Connection(simulator_clock, current_driver1),
    Connection(current_driver1, master_laser),
))

simulator.reset(False)

# ------------------------------------------------------------------

@benchmark(number=1, repeat=10)
def benchmarked_simulate():
    """Wrapper function to benchmark the instance's simulate method."""
    simulator.reset_time_only(t_final)
    return simulator.simulate()

# ------------------------------------------------------------------

print("Starting the benchmarked simulation...")
benchmarked_simulate()
print("Benchmarked simulation complete.")