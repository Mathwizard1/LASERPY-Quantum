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

class Clock(Component):
    """
    Clock class
    """
    def __init__(self, dt:float, name:str="default_clock"):
        super().__init__(name)
        self.dt = dt
        self.t = 0
        self.t_final = 0
        self.running = True

    def reset(self, set_t0_time:bool=False):
        """Clock reset method to override"""
        #return super().reset()
        if(set_t0_time):
            self.t = 0
        self.running = True

    def set(self, t_final:float, t:float|None=None):
        """Clock set method to override"""
        #return super().set()
        self.t_final = t_final
        if(t):
            self.t = t

    def update(self):
        """Clock update method to override"""
        #return super().update()
        if(self.t >= self.t_final):
            self.running = False
            return
        self.t += self.dt

class TimeComponent(Component):
    """
    TimeComponent class
    """
    def __init__(self, name:str="default_time_component"):
        super().__init__(name)

    def simulate(self, clock:Clock):
        #return super().simulate(args)
        """TimeComponent simulate method to override"""
        print("TimeComponent simulate method")

class DataComponent(Component):
    """
    DataComponent class
    """
    def __init__(self, save_simulation:bool=False, name:str="default_data_component"):
        super().__init__(name)
        self.save_simulation = save_simulation
        self.simulation_data = None

    def store_data(self):
        """DataComponent store_data method to override"""
        print("DataComponent store_data method")

    def reset_data(self):
        """DataComponent reset_data method to override"""
        print("DataComponent reset_data method")

    def display_data(self):
        """DataComponent display_data method to override"""
        print("DataComponent display_data method")

    def get_data(self):
        """DataComponent get_data method to override"""
        print("DataComponent get_data method")

class PhysicalComponent(DataComponent, TimeComponent):
    """
    PhysicalComponent class
    """
    def __init__(self, save_simulation:bool=False, name:str="default_physical_component"):
        super().__init__(save_simulation, name)  
        self.data = -1
        self.simulation_data = {'data':[]}
        self.simulation_data_units = {'data':r" ($u$)"}

    def store_data(self):
        """PhysicalComponent store_data method to override"""
        #return super().store_data()
        for key in self.simulation_data:
            if hasattr(self, key):
                self.simulation_data[key].append(getattr(self, key))

    def reset_data(self):
        """PhysicalComponent reset_data method to override"""
        #return super().reset_data()
        for key in self.simulation_data:
            self.simulation_data[key].clear()

    def display_data(self, time_data:np.ndarray):
        """PhysicalComponent display_data method to override"""
        #return super().display_data()
        if(not self.save_simulation):
            print(f"{self.name} did not save simulation data\n")
            return
        
        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        max_hf_plots = 1 + (len(self.simulation_data_units) // 2)
        sub_plot_idx = 1
        for key in self.simulation_data:
            plt.subplot(max_hf_plots, 2, sub_plot_idx)
            plt.plot(time_data, np.array(self.simulation_data[key]), label=f"{key}")

            plt.xlabel(r"Time $(s)$")
            plt.ylabel(key.capitalize() + self.simulation_data_units[key])
            
            plt.grid()
            plt.legend()
            sub_plot_idx += 1

        plt.show()

    def get_data(self):
        """PhysicalComponent get_data method to override"""
        #return super().get_data()
        if(not self.save_simulation):
            print(f"{self.name} did not save simulation data\n")
            return
        
        data_dict = {}
        for key in self.simulation_data:
            data_dict[key] = np.array(self.simulation_data[key])
        return data_dict

    def simulate(self, clock: Clock, data=None):
        """PhysicalComponent simulate method to override"""
        #return super().simulate(args)
        if(data):
            self.data = np.square(data) * np.sin(100 * clock.t) * np.exp(-clock.t)
        else:
            self.data = 100 * np.exp(-clock.t)

        if(self.save_simulation):
            self.store_data()

    def input_port(self):
        """PhysicalComponent input port method to override"""
        #print("PhysicalComponent input method")   
        kwargs = {'clock':None, 'data':None}
        return kwargs

    def output_port(self, kwargs:dict={}):
        """PhysicalComponent output port method to override"""
        #print("PhysicalComponent output method")
        for key in kwargs:
            if hasattr(self, key):
                kwargs[key] = getattr(self, key)
        return kwargs