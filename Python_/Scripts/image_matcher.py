import cv2
import pyautogui
import numpy as np
import keyboard
import os
import time
import torch
import PIL
from torchvision import transforms

class ImageMatcher:
    def __init__(self):
        self.image_folder = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/images/templates_folder'
        self.templates = []

        # Load all images in the folder
        for filename in os.listdir(self.image_folder):
            if filename.endswith('.PNG') or filename.endswith('.png'):
                template = cv2.imread(os.path.join(self.image_folder, filename), cv2.IMREAD_GRAYSCALE)
                self.templates.append(template)
    
    def take_screenshot(self, counter, mineral):
        # Create the "images" folder if it doesn't exist
        image_folder = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/images/screenshots'

        # Get the mouse position
        mouse_x, mouse_y = pyautogui.position()

        # Calculate the coordinates for the image region around the mouse position
        image_x = max(0, mouse_x - 25)
        image_y = max(0, mouse_y - 25)
        image_width = 50
        image_height = 50

        # Capture the image region
        screenshot = pyautogui.screenshot(region=(image_x, image_y, image_width, image_height))
        screenshot.save(os.path.join(image_folder, f'{mineral}{counter}.png'))
   
    @staticmethod
    def take_screenshot_at_position(coordinates):
        # Get the mouse position
        mouse_x, mouse_y = coordinates[0], coordinates[1]

        # Calculate the coordinates for the image region around the mouse position
        image_x = max(0, int(mouse_x) - 40)
        image_y = max(0, int(mouse_y) - 40)
        image_width = 80
        image_height = 80

        temp_image_folder = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/images/temp_check'
        

        # Capture the image region
        screenshot = pyautogui.screenshot(region=(image_x, image_y, image_width, image_height))
        screenshot.save(os.path.join(temp_image_folder, 'temp_img.png'))
        
    def match_image(self, coordinates):

        # Calculate the coordinates for the image region around the mouse position
        ImageMatcher.take_screenshot_at_position(coordinates)

        temp_image_folder = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/images/temp_check'
        screenshot = cv2.imread(os.path.join(temp_image_folder, 'temp_img.png'), cv2.IMREAD_GRAYSCALE)

        # Perform template matching for each template
        try:
            for template in self.templates:
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.80
                matches = np.where(result >= threshold)
                
                # Check if there is a match
                if len(matches[0]) > 0:
                    return True
            else:
                return False
        except Exception as e:
            print(e)
    
    def match_image_nn_captcha(self, image):

        model = torch.load('C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\model.pt')
        if torch.cuda.is_available():
            model.cuda()
        model.eval()

        labels = ['1', '2', '3', '4', '5', '6', '7', '8', 'x']

        # Perform template matching for each template
        try:
            
            transform = transforms.ToTensor()
            x = transform(image)
            x = x.cuda()
            with torch.inference_mode():
                output = model(x.unsqueeze(0))

            _, index = torch.max(output, 1)
            
            percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100
            
            return (labels[index], percentage[index[0]].item())
            
        except Exception as e:
            print(e)

    def match_image_nn_mineral(self, image):

        model = torch.load('C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\mineral_model.pt')
        if torch.cuda.is_available():
            model.cuda()
        model.eval()

        labels = ['mineral', 'not_mineral']

        # Perform template matching for each template
        try:
            
            transform = transforms.ToTensor()
            x = transform(image)
            x = x.cuda()
            with torch.inference_mode():
                output = model(x.unsqueeze(0))

            _, index = torch.max(output, 1)
            
            percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100
            
            return (labels[index], percentage[index[0]].item())
            
        except Exception as e:
            print(e)

    def check_for_captcha(self):
        # Calculate the coordinates for the image region around the mouse position
        ImageMatcher.take_screenshot_at_position((600, 460))

        temp_image_folder = 'C:/Users/Jordan/Desktop/Programming/GIT/PESBot/DATA_/images/temp_check'
        screenshot = cv2.imread(os.path.join(temp_image_folder, 'temp_img.png'), cv2.IMREAD_GRAYSCALE)

        # Perform template matching for each template
        try:
            for template in self.templates:
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.80
                matches = np.where(result >= threshold)
                
                # Check if there is a match
                if len(matches[0]) > 0:
                    return True
            else:
                return False
        except Exception as e:
            print(e)


# Usage example
"""
matcher = ImageMatcher()

counter=1
mineral = 'coal'
while True:
    if keyboard.is_pressed(('a')):
        matcher.match_image()
        time.sleep(0.25)
    elif keyboard.is_pressed('b'):
        matcher.take_screenshot(counter, mineral)
        counter+=1
        time.sleep(0.25)
        continue
    elif(keyboard.is_pressed('q')):
        break
"""