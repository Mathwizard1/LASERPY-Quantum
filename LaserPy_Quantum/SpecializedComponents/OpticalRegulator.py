from LaserPy_Quantum.Components.Component import Clock
from ..Components.Component import Component

class VariableOpticalAttenuator(Component):
    def __init__(self, name: str = "default_variable_optical_attenuator"):
        super().__init__(name)


    def simulate(self, clock: Clock):
        return super().simulate(clock)