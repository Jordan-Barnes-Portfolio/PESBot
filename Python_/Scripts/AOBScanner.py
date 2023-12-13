from utils import Util
import ctypes
from ctypes import wintypes
import time

util = Util()

# Constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MAX_BUFFER_SIZE = 512 * 512

num_results = 0
addresses_found = []
start_address, end_address = 0x700000000, 0x780000000

# Dlls and wintype handles
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
ReadProcessMemory.restype = wintypes.BOOL

#function for reading 16 bytes
def read_16_bytes(process_handle, address):
    buffer = ctypes.create_string_buffer(16)
    bytes_read = ctypes.c_size_t()

    success = ReadProcessMemory(process_handle, address, buffer, 16, ctypes.byref(bytes_read))

    if success:
        return buffer.raw[:bytes_read.value]
    else:
        return None

# Function for ReadProcessMemory
def read_process_memory(process_handle, address, size):
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()

    success = ReadProcessMemory(process_handle, address, buffer, size, ctypes.byref(bytes_read))

    if success:
        return buffer.raw[:bytes_read.value]
    else:
        return None

"""
This function scans the memory of a specified process to find a specific pattern of bytes.
It opens the process, reads the memory, and searches for the pattern using a sliding window approach.
If the pattern is found, it writes the memory address to a file.
"""
def scan_memory(start_address=start_address, end_address=end_address):
    print("Scanning memory for player pointer...")
    # Open the process
    process_id = util.get_pid_by_name("java.exe")
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
    
    if process_handle:
        # Example memory address and size
        difference = end_address - start_address
        loops = difference // MAX_BUFFER_SIZE
        memory_address = start_address
        memory_size = MAX_BUFFER_SIZE

        # Read memory from the process
        for x in range(loops):
            try:
                progress = (memory_address-start_address)/difference*100
                print(f"\rProgress: {progress:.2f}%", end='', flush=True)

                result = read_process_memory(process_handle, memory_address, memory_size) #read result from memory
                
                larger_chunk = result
                #search_array = b'\x6A\x61\x72\x3A\x66\x69\x6C\x65\x3A\x2E\x2F\x63\x6F\x6E\x74\x65\x6E\x74\x73\x2F\x70\x61\x72\x74\x69\x63\x6C\x65\x73\x2F\x70\x61\x72\x74\x69\x63\x6C\x65\x73\x2E\x6A\x61\x72\x21\x2F\x38\x30\x30'
                search_array = b'\x00\x00\x00\x00\x00\x00\x60\xC1\x00\x00\xC0\x41\x00\x00\x00\x01'
                
                larger_chunk_array = (ctypes.c_byte * len(larger_chunk)).from_buffer_copy(larger_chunk)
                search_array_array = (ctypes.c_byte * len(search_array)).from_buffer_copy(search_array)

                # Use memory view to compare
                larger_chunk_memoryview = memoryview(larger_chunk_array)
                search_array_memoryview = memoryview(search_array_array)
                
                bytes_obj = bytes(larger_chunk_memoryview)
                index = -1
                index = bytes_obj.find(search_array_memoryview)
                if index != -1:
                    global num_results
                    num_results += 1
                    progress = 100
                    print(f"\rProgress: {progress:.2f}%", end='', flush=True)

                    addresses_found.append(hex(memory_address+index))
                    util.min_max_of_address(addresses_found[0])
                    print("\nAddress found. Writing to file...")
                    with open("C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/DATA.txt", "w") as f:
                        f.write(addresses_found[0].split("0x")[1])
                    break
                
                memory_address += MAX_BUFFER_SIZE #add buffer size
                memory_address = memory_address - len(search_array) #subtract pattern size
            except Exception as e:
                print(f"\rProgress: {progress:.2f}%", end='', flush=True)
                continue

        
        # with open("offset_data.txt", "a") as f:
        #     result_below = read_process_memory(process_handle, memory_address+index-16, 512)
        #     result_above = read_process_memory(process_handle, memory_address-index+16, 512)
        #     f.write(f"\nB: {result_below.hex()}\nA: {result_above.hex()}\n=======")
        
        # Close the process handle
        ctypes.windll.kernel32.CloseHandle(process_handle)

    else:
        print(f"Failed to open process with ID {process_id}.")

scan_memory()
if(num_results>0):  
    print("\nDone. ", addresses_found)
    input("Press enter to exit...")
else:
    progress = 100
    print(f"\rProgress: {progress:.2f}%", end='', flush=True)
    print("\nNo address found.\nThis could be for a number of reasons.  Try restarting your game and running the program again.")
    input("Press enter to exit...")

    

