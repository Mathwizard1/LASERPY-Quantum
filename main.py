from LaserPy import Clock, PhysicalComponent
from LaserPy import Connection, Simulator

physical_device1 = PhysicalComponent(name="device1")
physical_device2 = PhysicalComponent(save_simulation=True, name="device2")

simulator_clock = Clock(dt=0.025)
simulator_clock.set(2)

simulator = Simulator(simulator_clock, save_simulation=True)

connection = Connection(None, physical_device1)
connection2 = Connection(physical_device1, physical_device2)

simulator.set((connection,connection2))

simulator.simulate()
time_data = simulator.get_data()

physical_device2.display_data(time_data)
