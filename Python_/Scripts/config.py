import sys
import os

#[0] = MAIN
#[1] = SCANNER
#[2] = DATA
#[3] = ADDRESSES
class Config():
    def __init__(self):

        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

        with open(self.CURRENT_DIR + "\\changeme.txt", "r") as f:
            self.PATH = f.read()

        self.MAIN_PATH = self.PATH + "\\Python_\\Scripts\\main.py"
        self.SCANNER_PATH = self.PATH + "\\Executables\\AOBScanner.exe"
        self.DATA_PATH = self.PATH + "\\DATA_\\DATA.txt"
        self.ADDRESSES_PATH = self.PATH + "\\DATA_\\MIN_MAX_ADDRESSES.txt"
        self.PLAYER_LAST_LOCATION = self.PATH + "\\DATA_\\PLAYER_LAST_LOCATION.txt"

        with open(self.CURRENT_DIR + "\\path.txt", "w") as f:
            f.write(self.MAIN_PATH + "\n" + self.SCANNER_PATH + "\n" + self.DATA_PATH + "\n" + self.ADDRESSES_PATH)

        

    def main(self):
        pass

if __name__ == "__main__":
    config = Config()
    config.main()
