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

class Clock(Component):
    """
    Clock class
    """
    def __init__(self, dt:float, t:float=0, t_final:float=None, name:str="default_clock"):
        super().__init__(name)
        self.dt = dt
        self.t = t
        self.t_final = dt
        if(t_final):
            self.t_final = t_final
        self.running = True

    def reset(self, set_t0_time=False):
        #return super().reset()
        if(set_t0_time):
            self.t = 0
        self.running = True

    def set(self, t_final:float):
        #return super().set()
        self.t_final = t_final

    def update(self):
        #return super().update()
        if(self.t_final and (self.t >= self.t_final)):
            self.running = False
            return None
        self.t += self.dt

class DataComponent(Component):
    """
    DataComponent class
    """
    def __init__(self, name = "default_physical_component"):
        super().__init__(name)

    def simulate(self, clock:Clock):
        """DataComponent simulate method to override"""
        print("DataComponent simulate method")  

    def input_port(self, args=None):
        """DataComponent input port method to override"""
        print("DataComponent input method")   

    def output_port(self, args=None):
        """DataComponent output port method to override"""
        print("DataComponent output method")