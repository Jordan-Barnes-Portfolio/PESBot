from ReadWriteMemory import ReadWriteMemory
import numpy
import struct
from utils import Util



"""
    Represents a player in the game.

    This class provides functionality to read the coordinates of the player
    based on given pointers.

    Attributes:
    - PID (int): Process ID of the player's game IE (2780).
    - util (Util): Instance of the Util class for utility functions.

    Methods:
    - read_coordinates(x_ptr, y_ptr): Reads and converts player coordinates.
"""
class Player:

    """
        Initialize the Player object.

        @param PID: Process ID of the player's game.
    """
    def __init__(self, PID = None):
        self.util = Util()
        self.PID = self.util.get_pid_by_name("java.exe")
        