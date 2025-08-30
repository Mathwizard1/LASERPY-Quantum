from typing import Union, Tuple

from .Components.Component import Component
from .Components.Clock import Clock

class Connection(Component):
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

    def execute(self, clock:Clock):
        #return super().execute()
        pass

class Simulator(Component):
    def __init__(self, simulation_clock:Clock, name="default_simulator"):
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