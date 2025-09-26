import matplotlib.pyplot as plt
import numpy as np

from ..Constants import FIG_WIDTH, FIG_HEIGHT

from .Component import Component
from .Component import Clock
from .Component import TimeComponent
from .Component import DataComponent

class Connection(TimeComponent):
    """
    Connection class
    """
    def __init__(self, input_components:Component|tuple[Component,...]|None, output_components:Component|tuple[Component,...], name:str="default_connection"):
        super().__init__(name)
        if(isinstance(input_components, Component)):
            input_components = (input_components,)
        self._input_components = input_components

        if(isinstance(output_components, Component)):
            output_components = (output_components,)
        self._output_components = output_components

    def simulate(self, clock: Clock):
        """Connection simulate method"""
        #return super().simulate(clock)
        
        # Input-Output device ports
        component_kwargs = []
        for idx, component in enumerate(self._output_components):
            component_kwargs.append(component.input_port())
            if('clock' in component_kwargs[idx]):
                component_kwargs[idx]['clock'] = clock

        # Input devices required
        if(self._input_components):
            for idx in range(len(component_kwargs)):
                for component in self._input_components:
                    component_kwargs[idx] = component.output_port(component_kwargs[idx])

        # Output device simulations
        for idx, component in enumerate(self._output_components):
            component.simulate(**component_kwargs[idx])

class Simulator(DataComponent):
    """
    Simulator class
    """
    def __init__(self, simulation_clock:Clock, name:str="default_simulator"):
        super().__init__(True, name)
        self.simulation_clock = simulation_clock

        # Data storage
        self._simulation_data = []
        self._simulation_data_units = r" $(s)$"

    def store_data(self):
        """Simulator store_data method"""
        #return super().store_data()
        self._simulation_data.append(self.simulation_clock.t)

    def reset_data(self):
        """Simulator reset_data method"""
        #return super().reset_data()
        self._simulation_data.clear()

        # TODO propagate clear data to all connection components

    def display_data(self):
        """Simulator display_data method"""
        #return super().display_data()
        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        time_data = np.array(self._simulation_data)

        plt.plot(time_data, time_data, label="Time")
        plt.xlabel(self._simulation_data_units)
        plt.ylabel(self._simulation_data_units)
        plt.grid()

        plt.legend()
        plt.show()

    def get_data(self):
        """Simulator get_data method"""
        #return super().get_data()
        return np.array(self._simulation_data)

    def set(self, connections:Connection|tuple[Connection,...]):
        """Simulator set method"""
        #return super().set()
        if(isinstance(connections, Connection)):
            connections = (connections,)
        self._connections = connections

    def simulate(self, args=None):
        """Simulator simulate method"""
        #return super().simulate(args)
        while(self.simulation_clock.running):
            for connection in self._connections:
                    connection.simulate(self.simulation_clock)
            
            self.store_data()
            self.simulation_clock.update()
        print("Simulations Complete")