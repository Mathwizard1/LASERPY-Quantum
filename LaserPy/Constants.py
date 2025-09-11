"""Constants for LaserPy"""

from enum import Enum

import json

# fixed Scientific Constants
class UniversalConstants(Enum):
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
    _Constants = {}

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
    def get(cls, key, default=None):
        """Retrieves a constant value by key."""
        return cls._Constants.get(key, default)

    @classmethod
    def set(cls, key, value):
        """Allows for runtime modification of a constant."""
        cls._Constants[key] = value

# Load the constants at the runtime
LaserPyConstants.load_from_json()

ERR_TOLERANCE = 1.0e-12

FIG_WIDTH = 12
FIG_HEIGHT = 6