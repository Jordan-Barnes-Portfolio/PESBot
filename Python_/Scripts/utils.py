import psutil
import win32gui
import ast
from ReadWriteMemory import ReadWriteMemory
import numpy
import struct


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

    # """
    #     !!!!!!!!!!!! NOT USED !!!!!!!!!!!!

    #     Runs an Array of Bytes scan.

    #     Opens the scanner, performs a scan, and saves the result to a file.
    # """
    # def run_aob_scan(self):
        
    #     file = open(self.DATA_PATH, 'w')
    #     file.close()

    #     try:
    #         # Use subprocess.run() to start the executable
    #         proc = subprocess.Popen([self.AOB_PATH])
    #     except Exception as e:
    #         print(f"Error: {e}")

    #     time.sleep(2)

    #     if "cheatengine-x86_64-SSE4-AVX2.exe" in (i.name() for i in psutil.process_iter()):
    #         while(True):
    #             if(os.stat(self.DATA_PATH).st_size == 0):
    #                 print("\rProcessing, please wait.", end='', flush=True)
    #             else:
    #                 print("\rData loaded.             ", end='', flush=True)
    #                 break
    
    

    """
        Reads players x pointer, and adds the y pointer offset to it.

        @Return: both the x and y pointer values.
    """
    def read_coordinates(self):
        try:
            with open(self.DATA_PATH, 'r') as file:
                data = file.readlines()

            data = data[0].upper()
            x_ptr,  y_ptr = int(data, 16), int(data, 16) + 4

            rwm = ReadWriteMemory()
            process = rwm.get_process_by_id(self.PID)

            process.open()
                
            # Initializes pointers from DATA file.
            if x_ptr is None or y_ptr is None:
                raise ValueError("Failed to get valid pointers from the data file.")

            x_val = process.read(x_ptr)
            y_val = process.read(y_ptr)

            return int(Util.convert_to_float(self, x_val)), int(Util.convert_to_float(self, y_val))
        except Exception as e:
            print(e)
            return None, None
        finally:
            process.close()

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
    