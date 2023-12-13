from player import Player
from utils import Util
from config import Config
import os


util = Util()
config = Config()

MAIN_PATH = config.MAIN_PATH
SCANNER_PATH = config.SCANNER_PATH

resp = input("(1):Last saved memory location\n(2):Last saved player location\n(3):Find memory address\nInput: ")
resp = resp.lower()
if resp == "3":
    input("Please use the ecaflip teleport and press enter...")
    os.startfile(SCANNER_PATH)
elif resp == "2":
    with open(config.PLAYER_LAST_LOCATION, 'r') as file:
        x, y = file.readlines()
        print(f"Last saved player location: ({x},{y})")
        #TODO: Add players last location to byte array check for exe somehow
        #this will need to be done in the exe
        #IDEA: reformat the AOB scanner to take in an argument of hex to search for maybe? might make it easier.

input("Press enter to start...")
while(True):
    try:
        x, y = util.read_coordinates()
        print(f"\rLocation: ({x},{y})   ", end='', flush=True)
    except KeyboardInterrupt:
        break
    
print(f"\nGoodbye! Storing current location: ({x},{y}) for use on startup!")

with open(config.DATA_PATH, 'r') as file:
    x_data = file.readlines()
with open(config.PLAYER_LAST_LOCATION, 'w') as file:
    for x in range(4):
        file.write(str(util.read_byte_values(int(x_data[0], 16)+x))+"\n")

    #TODO: Add players last location to byte array check for exe somehow
    #Shit i dont need to go back into the EXE i can use MemoryReader to read the value


#rwm = ReadWriteMemory()
# process = rwm.get_process_by_id(util.get_pid_by_name("java.exe"))
# process.open()
# st_val = process.read(int("716C8B8B8", 16))
# yt_val = process.read(int("716C8B8B8", 16)+4)
# process.close()
# print(util.convert_to_float(st_val), util.convert_to_float(yt_val))


# while(True):
#     try:
#         print(f"\rLocation: {player.read_coordinates()}       ", end='', flush=True)
#         time.sleep(0.1)
#         break
#     except Exception as e:
#         print(e)
#         break
