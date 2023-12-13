from utils import Util
from config import Config
import os
import time
import keyboard

util = Util()
config = Config()

MAIN_PATH = config.MAIN_PATH
SCANNER_PATH = config.SCANNER_PATH

os.system('cls')
monkey = ("┈┈╱▔▔▔▔▔╲┈┈┈\n╱┈┈╱▔╲╲╲▏┈┈┈\n╱┈┈╱━╱▔▔▔▔▔╲━╮┈┈\n▏┈▕┃▕╱▔╲╱▔╲▕╮┃┈┈\n▏┈▕╰━▏▊▕▕▋▕▕━╯┈┈\n╲┈┈╲╱▔╭╮▔▔┳╲╲┈┈┈\n┈╲┈┈▏╭━━━━╯▕▕┈┈┈\n┈┈╲┈╲▂▂▂▂▂▂╱╱┈┈┈\n┈┈┈┈▏┊┈┈┈┈┊┈┈┈╲┈\n┈┈┈┈▏┊┈┈┈┈┊▕╲┈┈╲\n┈╱▔╲▏┊┈┈┈┈┊▕╱▔╲▕\n┈▏ ┈┈┈╰┈┈┈┈╯┈┈┈▕▕\n┈╲┈┈┈╲┈┈┈┈╱┈┈┈╱┈╲\n┈┈╲┈┈▕▔▔▔▔▏┈┈╱╲╲╲▏\n┈╱▔┈┈▕┈┈┈┈▏┈┈▔╲▔▔\n┈╲▂▂▂╱┈┈┈┈╲▂▂▂╱┈\n")
print(monkey)
print("Welcome to PESBot!\n")
resp = input("(PRESS ENTER):Last saved memory location\n(2):Search memory\nInput: ")
resp = resp.lower()
if resp == "2":
    os.startfile(SCANNER_PATH)


input("Press ENTER to continue...")
print("Starting PESBot...")

flag = True
counter = 0
with open(config.PLAYER_LAST_LOCATION, 'r') as file:
    line = file.readline()
    temp_x, temp_y = line.split(":")

temp__x, temp__y = util.read_coordinates(flag)

print("\n\nPress Q to exit")
while(True):
    try:
        x, y = util.read_coordinates(flag)
        print(f"\rLocation: ({x},{y})          ", end='', flush=True)
    
        if(int(x) == int(temp_x) and int(y) == int(temp_y) and flag):
            counter += 1
            if(counter>40):
                flag = False

        if(keyboard.is_pressed('q')):
            break

    except KeyboardInterrupt or UnboundLocalError:
        break
    
