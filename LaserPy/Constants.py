"""Constants for LaserPy"""

from enum import Enum

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

class SpecificConstants:
    """
    Specific Constants for LaserPy
    """

    __instance = None

    TAU_N = 0.74 * (1.0e-9)
    """ 
    Carrier lifetime (seconds) 
    """

    TAU_P = 0.74 * (1.0e-12)
    """ 
    Photon lifetime (seconds) 
    """

ERR_TOLERANCE = 1.0e-12