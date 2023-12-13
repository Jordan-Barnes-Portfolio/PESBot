import psutil
import win32gui
import ast
from ReadWriteMemory import ReadWriteMemory
import numpy
import struct
import math
import ctypes as c
from pymem import Pymem


"""
    This class contains utility functions that are used throughout the project.
"""
class Util:

    """
        Initialize the Util class.

        @param DATA_PATH: Path to the data file.
        @param AOB_PATH: Path to the Cheat Engine executable.

        Example initialization of this class:
        =======================================
        from utils import Util
        util = Util()
        util.run_aob_scan()
        =======================================

    """
    def __init__(self, DATA_PATH = None, AOB_PATH = None):
        self.DATA_PATH = "C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/DATA.txt"
        self.PID = self.get_pid_by_name("java.exe")


        
    """
        Formats a byte string to be used in a scan.
        @param: byte_string: a string of hex values IE "0x00 0x00 0x00 0x00"
        @return: formatted byte string IE "00 00 00 00"
    """
    def format_byte_string(self, byte_string):
        byte_string = byte_string.replace("0x", "")
        if(len(byte_string) == 1):
            byte_string = "0" + byte_string

        
        length = len(byte_string)
        
        if(length<8):
            x = 8 - length
            st_added = '0' * x
            byte_string = Util.reverse_byte_order(byte_string)
            result = byte_string + st_added
            #if length is not already 8 and we are appending 0's
            #we recieve 45 c8 b0 and append 00
            #we want to flip 45 c8 b0 before we append.
        else:
            result = Util.reverse_byte_order(byte_string)
            #if length is already 8 we do a byte flip
            #IE 40 00 00 00 becomes  00 00 00 40
        
        return ' '.join([result[i:i+2] for i in range(0, len(result), 2)])
    


    """
        Calculates the vector of two points, scales it by {scale_factor} factor, and sets
        the maximum length of the radial line by {max_length}.
        @param: p1: x1, y1
        @param: p2: x2, y2
        @param: scale_factor: factor to scale the vector by
        @param: max_length: maximum length of the radial line
        @return: scaled_p2: scaled x2, y2

        # Example usage:
        # pixel_cord_1 = (500, 400)
        # pixel_cord_2 = (630, 699)

        #These are defaulted and do not need to be added
        # scale_factor = 0.8 # Set your factor
        # max_length = 100  # Set your desired maximum length

        # pg.moveTo(calculate_vector(p1, p2))
    """
    def calculate_vector(self, p1, p2, scale_factor=0.8, max_length=100):
        x1, y1 = p1
        x2, y2 = p2

        # Calculate the components of the original vector
        original_vector = (x2 - x1, y2 - y1)

        # Scale the vector components
        scaled_vector = (scale_factor * original_vector[0], scale_factor * original_vector[1])

        # Check if a maximum length is specified
        if max_length is not None:
            # Calculate the magnitude of the scaled vector
            scaled_magnitude = math.sqrt(scaled_vector[0] ** 2 + scaled_vector[1] ** 2)

            # If the magnitude exceeds the maximum length, normalize the vector
            if scaled_magnitude > max_length:
                normalized_vector = (scaled_vector[0] / scaled_magnitude, scaled_vector[1] / scaled_magnitude)
                scaled_vector = (max_length * normalized_vector[0], max_length * normalized_vector[1])

        # Calculate the coordinates of the scaled vector
        scaled_p2 = (x1 + scaled_vector[0], y1 + scaled_vector[1])

        return scaled_p2
    


    """
        Calculates the cells required to mvoe between two points on an isometric grid.
        @param: start_pos: x1, y1 (player position)
        @param: target_pos: x2, y2 (target position (Mineral, NPC, etc))
        @return: cells: x, y (cells required to move between the two points)
    """
    def calculate_cells(self, start_pos, target_pos):
        return (target_pos[0]-start_pos[0], start_pos[1]-target_pos[1])
    
    """
        Reads players x pointer, and adds the y pointer offset to it.

        @Return: both the x and y pointer values.
    """
    def read_coordinates(self, flag):
        try:
            with open(self.DATA_PATH, 'r') as file:
                data = file.readlines()

            data = data[0].upper()
            x_ptr,  y_ptr = int(data, 16), int(data, 16) + 4
        
            #testing pymem
            pymem = Pymem("java.exe")
            
            return [int(pymem.read_float(x_ptr)), int(pymem.read_float(y_ptr))]
        except Exception as e:
            print("Error in reading memory: ", e)


            #     x_other = int(data, 16) + 40
            #     y_other = x_other + 4
            #     rwm = ReadWriteMemory()
            #     process = rwm.get_process_by_id(self.PID)

            #     process.open()
                
            #     # Initializes pointers from DATA file.
            #     if x_ptr is None or y_ptr is None:
            #         raise ValueError("Failed to get valid pointers from the data file.")
                
            #     #Checks if pointer values are valid, if they arent we run the flag check.
            #     if(flag):
            #         # Read the values from the pointers.
            #         x_val = process.read(x_ptr)
            #         y_val = process.read(y_ptr)
            #     else:
            #         # Read the values from the pointers.
            #         x_val = process.read(x_other)
            #         y_val = process.read(y_other)   

            #     return int(Util.convert_to_float(self, x_val)), int(Util.convert_to_float(self, y_val))
            # finally:
            #     try:
            #         if process:
            #             process.close()
            #     except Exception as e:
            #         pass
    


    """
        Reads a byte value from a given address.
        @param: address: memory address to read from
        @return: byte_val: byte value at the given address
    """
    def read_byte_values(self, address):
        try:
            rwm = ReadWriteMemory()
            process = rwm.get_process_by_id(self.PID)
            process.open()
            byte_val = process.read(address)
            return byte_val
        except Exception as e:
            print(e)
            return None
        finally:
            process.close()



    """
        Reads a float value from a given address, and converts it to little endian.
        @param: address: memory address to read from
        @return: float_val: bytes X and Y at the given address
    """
    def coords_to_little_endian(self, x, y):
        # Decimal value
        decimal_value_x = x
        decimal_value_y = y

        # Convert to 4-byte float in little-endian format
        float_bytes_x = struct.pack('<f', decimal_value_x)

        # Convert bytes to hexadecimal
        hex_representation_x = ''.join(format(byte, '02x') for byte in float_bytes_x)

        # Decimal value
        # Convert to 4-byte float in little-endian format
        float_bytes_y = struct.pack('<f', decimal_value_y)

        # Convert bytes to hexadecimal
        hex_representation_y = ''.join(format(byte, '02x') for byte in float_bytes_y)

        # Convert hexadecimal strings to bytes
        bytes_x = bytes.fromhex(hex_representation_x.upper())
        bytes_y = bytes.fromhex(hex_representation_y.upper())
    
        return [bytes_x + bytes_y]
    """
        Gets a process ID given its name, IE Java.exe = 32800
    """    
    def get_pid_by_name(self, name):
        pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if name.lower() in proc.info['name'].lower():
                pid = proc.info['pid']
                break
        return pid
    


    """
        Returns the slope of a line given x1, y1, x2, y2

        @param x1, y1, x2, y2: x/y pixel coordinates of the requested slope
        @return: slope of the line

    """
    def get_slope(self, x1, y1, x2, y2):
       
        return ((y2 - y1) / (x2 - x1)) if (x2 - x1) != 0 else None
    


    """
        Sets the windows frame to static dimensions.

        @param name: name of the window
    """
    def set_dimensions(self, name, width=1000, height=800):
        
        hwnd = win32gui.FindWindow(None, name)
        win32gui.MoveWindow(hwnd, 0, 0, width, height, True)




    """
        Gets a Window handle based on its name, IE "WAKFU"
        This is different than the process name.  IE "WAKFU" window name, is process "JAVA.EXE"

        @param name: name of the WINDOW (not process)
        @return: x, y, w, h: returns position of the window on screen, width, and height
    """
    def get_window_rect(self, name):

        hwnd = win32gui.FindWindow(None, name)
        rect = win32gui.GetWindowRect(hwnd)
        x, y, w, h = rect[0], rect[1], rect[2], rect[3]
        return x, y, w, h
    
    def get_min_max_addresses(self):
        with open("C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/MIN_MAX_ADDRESSES.txt", 'r') as f:
            data = f.readlines()
            for x in data:
                if("MAX:" in x):
                    max_address = hex(int(x.split(":")[1], 16))
                elif("MIN:" in x):
                    min_address = hex(int(x.split(":")[1], 16))
        return min_address, max_address

    """
        Converts a float to a hex string.
        @param float_val: a float value IE 0.0
        @return: hex string IE "0x00 0x00 0x00 0x00"
    """
    @staticmethod
    def convert_float_to_hex(float_val):
        return hex(struct.unpack('<I', struct.pack('<f', float_val))[0])
    
    """
        Parses the input string as a list of lists.
        @param input_string: a string representing a list of lists IE "[[l,l][x,x]]"
        @return: list of lists
    """
    @staticmethod
    def parse_input(input_string):
        try:
            # Safely evaluate the input string as a literal expression
            result = ast.literal_eval(input_string)
            # Check if the result is a list of lists
            if isinstance(result, list) and all(isinstance(sublist, list) and len(sublist) == 2 for sublist in result):
                return result
            else:
                raise ValueError("Input is not a valid list of lists.")
        except (SyntaxError, ValueError) as e:
            print(f"Error: {e}", " ERROR IS HERE")
            return None
    

    """
        Reverses the byte order of a hex string.
        @param hex_string: a string of hex values IE "0x00 0x00 0x00 0x00"
        @return: reversed hex string IE "0x00 0x00 0x00 0x00" becomes "0x00 0x00 0x00 0x00"    
    """
    @staticmethod
    def reverse_byte_order(hex_string):
        # Split the hex string into chunks of two characters
        chunks = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

        # Reverse the order of the chunks
        reversed_chunks = reversed(chunks)

        # Join the reversed chunks back into a string
        reversed_hex_string = ''.join(reversed_chunks)

        return reversed_hex_string
    
    """
        Writes the min and max address to a file.
        @param address: address to compare against the min and max address
    """
    @staticmethod
    def min_max_of_address(address):
        try:
            with open("C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/MIN_MAX_ADDRESSES.txt", 'r') as f:
                data = f.readlines()
            for x in data:
                if("MAX:" in x):
                    max_address = max(int(x.split(":")[1], 16), int(address, 16))
                    max_address = str(hex(max_address))
                elif("MIN:" in x):
                    min_address = min(int(x.split(":")[1], 16), int(address, 16))
                    min_address = str(hex(min_address))
            with open("C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/MIN_MAX_ADDRESSES.txt", 'w') as f:
                f.write(f"MIN:{min_address}\nMAX:{max_address}")
        except Exception as e:
            print(f"Error: {e}")

    """
        Convert binary value to a floating-point number.

        @param value: Binary value to be converted.
        @return: Floating-point number.
    """
    @staticmethod
    def convert_to_float(self, value):
        integer_value = numpy.array(value).astype(numpy.int32)
        return struct.unpack('!f', struct.pack('!i', integer_value))[0]
    