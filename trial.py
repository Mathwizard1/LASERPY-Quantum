from LaserPy import Clock, PhysicalComponent
from LaserPy import Connection, Simulator

from LaserPy import display_class_instances_data

simulator_clock = Clock(dt=0.01)
simulator_clock.set(2)

simulator = Simulator(simulator_clock, save_simulation= True)

physical_device1 = PhysicalComponent(save_simulation= True, name="other component")
physical_device2 = PhysicalComponent(save_simulation= True)

simulator.set((
    Connection(simulator_clock, physical_device1),
    Connection(physical_device1, physical_device2)
))

simulator.simulate()
time_data = simulator.get_data()

physical_device1.display_data(time_data)
physical_device2.display_data(time_data)

display_class_instances_data((physical_device1, physical_device2), time_data)