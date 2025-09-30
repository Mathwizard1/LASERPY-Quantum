from ..Components import TimeComponent

class VariableOpticalAttenuator(TimeComponent):
    def __init__(self, name: str = "default_variable_optical_attenuator"):
        super().__init__(name)