from LaserPy import Clock, PhysicalComponent
from LaserPy import Connection, Simulator
from LaserPy import ArbitaryWave, ArbitaryWaveGenerator
from LaserPy import CurrentDriver
from LaserPy import Laser

# Control Constants (all in SI units)
modulation_bits = [1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
dt = 1e-12
t_unit = 1e-9
t_final = t_unit * 5
sampling_rate = 2 * dt


class SquareWave(ArbitaryWave):
    def __init__(self, signal_name:str, t_unit: float = t_unit, val= 0.0250):
        super().__init__(signal_name, t_unit, central_offset = 0, total_spread = 1.0)
        self.val = val

    def WaveSignal(self, t:float, args):
        #return super().WaveSignal(t, args)
        if(self._t_unit and t < self._t_unit / 2):
            return 0
        return self.val

myWave1 = SquareWave(signal_name="master_wave")
myWave2 = SquareWave(signal_name="slave_wave", val= 1.0)

AWG = ArbitaryWaveGenerator()
AWG.set(myWave1)
AWG.set(myWave2)

current_driver1 = CurrentDriver(AWG)
current_driver1.set((myWave1,))

current_driver2 = CurrentDriver(AWG)
current_driver2.set((myWave2,))

master_laser = Laser(save_simulation= True, name= "master_laser")
slave_laser = Laser(save_simulation= True, name= "slave_laser")

simulator_clock = Clock(dt)
simulator_clock.set(t_final)

simulator = Simulator(simulator_clock)

simulator.set((
    Connection(simulator_clock, (current_driver1, current_driver2)),
    Connection(current_driver1, master_laser),
    Connection(current_driver2, slave_laser),
))

simulator.simulate()
time_data = simulator.get_data()

master_laser.display_data(time_data)
slave_laser.display_data(time_data)