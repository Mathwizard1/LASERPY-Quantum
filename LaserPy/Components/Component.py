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

    def execute(self):
        """Component execute method to override"""
        print("Component execute method")

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

    def reset(self, set_t0_time=False):
        #return super().reset()
        if(set_t0_time):
            self.t = 0
        self.running = True

    def set(self, t_final:float, t:float=None):
        #return super().set()
        self.t_final = t_final
        if(t):
            self.t = t

    def update(self):
        #return super().update()
        if(self.t >= self.t_final):
            self.running = False
            return
        self.t += self.dt

class DataComponent(Component):
    """
    DataComponent class
    """
    def __init__(self, name = "default_data_component"):
        super().__init__(name)
        self.simulation_data = []

    def simulate(self, clock:Clock):
        """DataComponent simulate method to override"""
        self.simulation_data.append(clock.t)
        print("DataComponent simulate method")  

    def input_port(self):
        """DataComponent input port method to override"""
        print("DataComponent input method")   

    def output_port(self):
        """DataComponent output port method to override"""
        print("DataComponent output method")