import matplotlib.pyplot as plt
import numpy as np

from ..Constants import FIG_WIDTH, FIG_HEIGHT

class Component:
    """
    Component class
    """
    def __init__(self, name:str="default_component"):
        self.name = name

    def reset(self):
        """Component reset method to override"""
        print("Component reset method")

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
        """Component input_port method to override"""  
        kwargs = {}
        return kwargs

    def output_port(self, kwargs:dict={}):
        """Component output_port method to override"""  
        return kwargs

class Clock(Component):
    """
    Clock class
    """
    def __init__(self, dt:float, name:str="default_clock"):
        super().__init__(name)
        self.dt = dt
        self.t = 0
        self.running = True

        self._t_final = 0

    def reset(self, set_t0_time:bool=False):
        """Clock reset method"""
        #return super().reset()
        if(set_t0_time):
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

    def simulate(self, clock:Clock):
        """TimeComponent simulate method to override"""
        #return super().simulate(args)
        print("TimeComponent simulate method")

    def input_port(self):
        """TimeComponent input_port method to override"""
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

        self._simulation_data = {}
        self._simulation_data_units = {}

    def store_data(self):
        """DataComponent store_data method"""
        for key in self._simulation_data:
            if hasattr(self, key):
                self._simulation_data[key].append(getattr(self, key))

    def reset_data(self):
        """DataComponent reset_data method"""
        for key in self._simulation_data:
            self._simulation_data[key].clear()

    def display_data(self, time_data:np.ndarray|None):
        """DataComponent display_data method"""
        if(not self._save_simulation):
            print(f"{self.name} did not save simulation data")
            return
        elif(time_data is None):
            print(f"{self.name} got None for time_data")
            return
        
        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        max_hf_plots = 1 + (len(self._simulation_data_units) // 2)
        sub_plot_idx = 1
        for key in self._simulation_data:
            plt.subplot(max_hf_plots, 2, sub_plot_idx)
            plt.plot(time_data, np.array(self._simulation_data[key]), label=f"{key}")

            plt.xlabel(r"Time $(s)$")
            plt.ylabel(key.capitalize() + self._simulation_data_units[key])
            
            plt.grid()
            plt.legend()
            sub_plot_idx += 1

        plt.show()

    def get_data(self):
        """DataComponent get_data method"""
        if(not self._save_simulation):
            print(f"{self.name} did not save simulation dat")
            return
        
        data_dict = {}
        for key in self._simulation_data:
            data_dict[key] = np.array(self._simulation_data[key])
        return data_dict

class PhysicalComponent(DataComponent, TimeComponent):
    """
    PhysicalComponent class
    """
    def __init__(self, save_simulation:bool=False, name:str="default_physical_component"):
        super().__init__(save_simulation, name)  

        self._simulation_data = {'data':[]}
        self._simulation_data_units = {'data':r" $(u)$"}
        self.data = -1

    def simulate(self, clock: Clock, data=None):
        """PhysicalComponent simulate method to override"""
        #return super().simulate(args)
        if(data):
            self.data = np.square(data) * np.sin(100 * clock.t) * np.exp(-clock.t)
        else:
            self.data = 100 * np.exp(-clock.t)

        if(self._save_simulation):
            self.store_data()

    def input_port(self):
        """PhysicalComponent input port method to override"""
        #return super().input_port() 
        kwargs = {'clock':None, 'data':None}
        return kwargs

    def output_port(self, kwargs:dict={}):
        """PhysicalComponent output port method to override"""
        #return super().output_port(kwargs)
        for key in kwargs:
            if hasattr(self, key):
                kwargs[key] = getattr(self, key)
        return kwargs