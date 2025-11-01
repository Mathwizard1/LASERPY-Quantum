from LaserPy_Quantum import Clock, PhysicalComponent
from LaserPy_Quantum import Connection, Simulator

from LaserPy_Quantum import display_class_instances_data

simulator_clock = Clock(dt=0.01)
simulator_clock.set(2)

simulator = Simulator(simulator_clock)

physical_device1 = PhysicalComponent()
physical_device2 = PhysicalComponent()

simulator.set((
    Connection(simulator_clock, physical_device1),
    Connection(physical_device1, physical_device2)
))

simulator.reset(True)
simulator.simulate()
time_data = simulator.get_data()

physical_device1.display_data(time_data)
physical_device2.display_data(time_data)

display_class_instances_data((physical_device1, physical_device2), time_data)