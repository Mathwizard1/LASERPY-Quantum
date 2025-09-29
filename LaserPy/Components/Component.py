import matplotlib.pyplot as plt
import numpy as np

from ..Constants import FIG_WIDTH, FIG_HEIGHT

# TODO add unique component id on runtime instance
# TODO refine reset and reset_data behaviour

class Component:
    """
    Component class
    """
    def __init__(self, name:str="default_component"):
        self.name = name
        """Component name data"""

    def __repr__(self) -> str:
        """Component __repr__ method to override"""
        return f"Component: {self.name}"

    def reset_data(self):
        """Component reset_data method to override"""
        # Empty method
        pass

    def reset(self, args=None):
        """Component reset method to override"""
        # Empty method
        pass

    def set(self):
        """Component set method to override"""
        print("Component set method")

    def update(self):
        """Component update method to override"""
        print("Component update method")

    def simulate(self, args=None):
        """Component simulate method to override"""
        # Empty method
        pass

    def input_port(self):
        """Component input port method to override"""  
        kwargs = {}
        return kwargs

    def output_port(self, kwargs:dict={}):
        """Component output port method to override"""  
        return kwargs

class Clock(Component):
    """
    Clock class
    """
    def __init__(self, dt:float, name:str="default_clock"):
        super().__init__(name)
        self.dt = dt
        """Clock Delta time data"""

        self.t = 0
        """Clock time data"""

        self.running = True
        """Clock running state data"""

        self._t_final = 0
        """Clock final time data"""

    def reset(self, set_t0:bool=False):
        """Clock reset method"""
        #return super().reset()
        if(set_t0):
            self.t = 0
        self.running = True

    def set(self, t_final:float, t:float|None=None):
        """Clock set method"""
        #return super().set()
        self._t_final = t_final
        if(t):
            self.t = t

    def update(self):
        """Clock update method"""
        #return super().update()
        if(self.t >= self._t_final):
            print(f"{np.format_float_scientific(self._t_final, precision= 3, exp_digits= 3)} sec has elapsed.")
            self.running = False
            return
        self.t += self.dt

    def output_port(self, kwargs: dict = {}):
        """Clock output_port method"""
        #return super().output_port(kwargs)
        kwargs['clock'] = self
        return kwargs

class TimeComponent(Component):
    """
    TimeComponent class
    """
    def __init__(self, name:str="default_time_component"):
        super().__init__(name)

        self._data = 0
        """data for TimeComponent"""

    def simulate(self, clock:Clock):
        """TimeComponent simulate method to override"""
        #return super().simulate(args)
        print("TimeComponent simulate method")

    def input_port(self):
        """TimeComponent input port method to override"""
        #return super().input_port()
        kwargs = {'clock':None}
        return kwargs

class DataComponent(Component):
    """
    DataComponent class
    """
    def __init__(self, save_simulation:bool=False, name:str="default_data_component"):
        super().__init__(name)
        
        self._save_simulation = save_simulation
        """DataComponent save simulation state"""

        self._simulation_data = {}
        """DataComponent simulation data"""

        self._simulation_data_units = {}
        """DataComponent simulation data units"""

    def _handle_display_data(self, time_data:np.ndarray):
        """DataComponent _handle_display_data method"""
        if(self._handle_get_data()):
            return True
        elif(time_data is None):
            print(f"{self.name} got None for time_data")
            return True
        else:
            for key in self._simulation_data:
                if(len(time_data) != len(self._simulation_data[key])):
                    print(f"{self.name} {key} has {len(self._simulation_data[key])} while time_data has {len(time_data)}")
                    return True
        return False

    def _handle_get_data(self):
        """DataComponent _handle_get_data method"""
        if(not self._save_simulation):
            print(f"{self.name} did not save simulation data")
            return True
        elif(len(self._simulation_data) == 0):
            print(f"{self.name}'s simulation data is empty")
            return True
        return False

    def store_data(self):
        """DataComponent store_data method"""
        for key in self._simulation_data:
            if hasattr(self, key):
                self._simulation_data[key].append(getattr(self, key))

    def reset_data(self):
        """DataComponent reset_data method"""
        for key in self._simulation_data:
            self._simulation_data[key].clear()

    def display_data(self, time_data:np.ndarray, simulation_keys:tuple[str,...]|None=None):
        """DataComponent display_data method"""        
        
        # Handle cases
        if(self._handle_display_data(time_data)):
            print(f"{self.name} cannot display data")
            return

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        key_tuple = tuple(self._simulation_data_units)
        
        # Display fixed tuple of data
        if(simulation_keys):
            key_list = []
            for key in simulation_keys:
                if(key in self._simulation_data_units):
                    key_list.append(key)
            key_tuple = tuple(key_list)

        max_hf_plots = 1 + (len(key_tuple) >> 1)
        sub_plot_idx = 1
        for key in key_tuple:
            plt.subplot(max_hf_plots, 2, sub_plot_idx)
            plt.plot(time_data, np.array(self._simulation_data[key]), label=f"{key}")

            plt.xlabel(r"Time $(s)$")
            plt.ylabel(key.capitalize() + self._simulation_data_units[key])
            
            plt.grid()
            plt.legend()
            sub_plot_idx += 1

        plt.tight_layout()
        plt.show()

    def get_data(self):
        """DataComponent get_data method"""

        # Handle cases
        val = self._handle_get_data()
        
        data_dict = {}
        for key in self._simulation_data:
            data_dict[key] = np.zeros(1) if(val) else np.array(self._simulation_data[key])
        return data_dict

    def get_data_units(self):
        """DataComponent get_data_units method"""        
        return dict(self._simulation_data_units)

    def reset(self, save_simulation:bool=False):
        """DataComponent reset method to override"""
        #return super().reset()
        self._save_simulation = save_simulation

    def output_port(self, kwargs:dict={}):
        """DataComponent output port method to override"""
        #return super().output_port(kwargs)
        for key in kwargs:
            if hasattr(self, key):
                kwargs[key] = getattr(self, key)
        return kwargs

class PhysicalComponent(DataComponent, TimeComponent):
    """
    PhysicalComponent class
    """
    def __init__(self, save_simulation:bool=False, name:str="default_physical_component"):
        super().__init__(save_simulation, name)  

        self._simulation_data = {'_data':[]}
        self._simulation_data_units = {'_data':r" $(u)$"}

    def simulate(self, clock: Clock, _data=None):
        """PhysicalComponent simulate method to override"""
        #return super().simulate(args)
        if(_data):
            self._data = np.square(_data) * np.sin(100 * clock.t) * np.exp(-clock.t)
        else:
            self._data = 100 * np.exp(-clock.t)

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """PhysicalComponent input port method to override"""
        kwargs = super().input_port() 
        kwargs['_data'] = None
        return kwargs