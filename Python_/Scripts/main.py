from player import Player
from utils import Util
import os

util = Util()
SCANNER_PATH = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/Python_/Scripts/dist/AOBScanner/AOBScanner.exe'
MAIN_PATH = "C:/Users/Jordan/Desktop/Programming/GIT/PESBot/Python_/Scripts/main.py"

resp = input("Do you want to use last saved memory location? (y/n) \nInput: ")
resp = resp.lower()
if resp == "n" or resp == "no":
    input("Please use the ecaflip teleport and press enter...")
    os.startfile(SCANNER_PATH)

input("Press enter to start...")
while(True):
    try:
        x, y = util.read_coordinates()
        print(f"\rLocation: ({x},{y})   ", end='', flush=True)
    except Exception as e:
        print(f"\r{e}", flush=True, end='')
        break
    

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
