import keyboard
import time
import pyautogui as pg
from image_matcher import ImageMatcher
from torchvision import transforms
from pathing import Pathing
from utils import Util

def solve_captcha(counter=0):
    path = Pathing()
    util = Util()
    matcher = ImageMatcher()

    keyboard.press_and_release("space")
            
    top_rows = {"1":[-4, -4], "2":[-3,-4], "3":[-2,-4], "4":[-1,-4], "5":[0,-4]}
    bottom_rows = {"1":[7, -4], "2":[6,-4], "3":[5,-4], "4":[4,-4], "5":[3,-4]}

    found_bottom = []

    for x in bottom_rows.values():
        print(x)
        pos = x
        for y in range(11):

            coord = path.captcha_move(util.calculate_cells(util.read_coordinates(True), x))
    
            try:
                mouse_x, mouse_y = coord[0], coord[1]-12

                # Calculate the coordinates for the image region around the mouse position
                image_x = max(0, int(mouse_x) - 25)
                image_y = max(0, int(mouse_y) - 25)
                image_width = 50
                image_height = 50
                
                ss = pg.screenshot(region=(image_x, image_y, image_width, image_height))
                
                p = matcher.match_image_nn_captcha(ss)
                if(p[1] > 69):
                    time.sleep(0.1)
                    found_bottom.append(p[0])
            except Exception:
                pass
            pos[1] -= 1

    for x in top_rows.values():
        pos = x
        for y in range(11):
            coord = path.captcha_move(util.calculate_cells(util.read_coordinates(True), x))
            
            try:
                mouse_x, mouse_y = coord[0], coord[1]

                # Calculate the coordinates for the image region around the mouse position
                image_x = max(0, int(mouse_x) - 25)
                image_y = max(0, int(mouse_y) - 25)
                image_width = 50
                image_height = 50
                
                ss = pg.screenshot(region=(image_x, image_y, image_width, image_height))
                
                p = matcher.match_image_nn_captcha(ss)
            
                if(p[1] > 69):
                    if(p[0] in found_bottom):
                        pg.moveTo(coord)
                        time.sleep(0.1)
                        keyboard.press_and_release("1")
                        time.sleep(0.34)
                        pg.leftClick()

            except Exception:
                pass
            pos[1] -= 1
    
    if(matcher.check_for_captcha() and counter<=3):
        time.sleep(1)
        print("\rCaptcha detected still.. retrying..              ", flush=True, end="")
        solve_captcha(counter+1)
    elif(counter>3 and matcher.check_for_captcha()):
        print("\rSkipping captcha... too many failed attempts     ", flush=True, end="")
        keyboard.press_and_release("1")
        coord = path.captcha_move(util.calculate_cells(util.read_coordinates(True), [-3, -11]))
        pg.moveTo(coord)
        time.sleep(0.1)
        pg.leftClick()
        time.sleep(2)
        keyboard.press_and_release("esc")
    elif(not matcher.check_for_captcha()):
        time.sleep(2)
        keyboard.press_and_release("esc")