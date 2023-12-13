import keyboard
import time
import pyautogui as pg
from image_matcher import ImageMatcher
import os
import keyboard
import time
import pyautogui as pg
from image_matcher import ImageMatcher
from torchvision import transforms
from pathing import Pathing
from utils import Util

matcher = ImageMatcher()

grid = Pathing()
util = Util()

top_rows = {"1":[-4, -4], "2":[-3,-4], "3":[-2,-4], "4":[-1,-4], "5":[0,-4]}
bottom_rows = {"1":[7, -4], "2":[6,-4], "3":[5,-4], "4":[4,-4], "5":[3,-4]}

coord = grid.captcha_move(util.calculate_cells(util.read_coordinates(True), [-3, -11]))
            
pg.moveTo(coord)
# while True:
#     if(keyboard.is_pressed("a")):
#         coord = pg.position()

#         try:
#             mouse_x, mouse_y = coord[0], coord[1]

#             # Calculate the coordinates for the image region around the mouse position
#             image_x = max(0, int(mouse_x) - 25)
#             image_y = max(0, int(mouse_y) - 25)
#             image_width = 50
#             image_height = 50
            
#             ss = pg.screenshot(region=(image_x, image_y, image_width, image_height))
            
#             p = matcher.match_image_nn_mineral(ss)
#             if(p[1] > 69):
#                 pg.moveTo(coord[0], coord[1])


#         except Exception:
#             pass

#600, 460
# counter = 22
# name = "captcha_check_"
# while True:
#     if(keyboard.is_pressed("q")):
#         break
#     elif(keyboard.is_pressed("a")):
#         matcher.take_screenshot(counter, name)
#         time.sleep(0.25)
#         counter += 1
#         print("Snap!!")


# # Create the damn csv file.
# check = ["mineral_", "not_mineral", "captcha_3", "captcha_4", "captcha_5",
#          "captcha_6", "captcha_7", "captcha_8", "captcha_x", "captcha_empty"]
# path = "C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\mineral_images"
# png_files = [f for f in os.listdir(path) if f.endswith('.png')]

# with open("C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\minerals.csv", "a") as f:
#     for png in png_files:
#         if(check[0] in png and check[1] not in png):
#             f.write(png + ",0\n")
#         elif(check[1] in png):
#             f.write(png + ",1\n")
#         elif(check[2] in png):
#             f.write(png + ",2\n")
#         elif(check[3] in png):
#             f.write(png + ",3\n")
#         elif(check[4] in png):
#             f.write(png + ",4\n")
#         elif(check[5] in png):
#             f.write(png + ",5\n")
#         elif(check[6] in png):
#             f.write(png + ",6\n")
#         elif(check[7] in png):
#             f.write(png + ",7\n")
#         elif(check[8] in png):
#             f.write(png + ",8\n")
#         elif(check[9] in png):
#             f.write(png + ",9\n")
