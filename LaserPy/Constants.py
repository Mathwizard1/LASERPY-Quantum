"""Constants for LaserPy"""

from enum import Enum

import json

from numpy import exp
from numpy import pi, complexfloating

import rust_optimizer

# fixed Scientific Constants
class UniversalConstants(float, Enum):
    """
    Universal Constants for LaserPy
    """

    CHARGE = 1.602 * (1.0e-19)
    """
    single unit of charge of elctron / proton
    """

    H = 6.626 * (1.0e-34)
    """
    Plank's Constant 
    """

    C = 2.997 * (1.0e+8)
    """
    Speed of light in vacuum 
    """

class LaserPyConstants:
    """
    Simulation Constants for LaserPy
    """
    _Constants: dict[str, float] = {}

    @classmethod
    def load_from_json(cls, filepath='./LaserPy/Constants.json'):
        """Loads constants from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                cls._Constants = json.load(f)
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
            exit()

    @classmethod
    def get(cls, key, default=1.0):
        """Retrieves a constant value by key."""
        return cls._Constants.get(key, default)

    @classmethod
    def set(cls, key, value):
        """Allows for runtime modification of a constant."""
        cls._Constants[key] = value

# Load the constants at the runtime
LaserPyConstants.load_from_json()

ERR_TOLERANCE = 1.0e-12

EMPTY_FIELD: complexfloating = ERR_TOLERANCE * exp(1j * 0)
FULL_PHASE_INTERVAL: float = 2 * pi

FIG_WIDTH = 12
FIG_HEIGHT = 6

if __name__ == "__main__":
    constants = rust_optimizer.UniversalConstant
    print(constants.SpeedOfLight.value())        # 299792458.0