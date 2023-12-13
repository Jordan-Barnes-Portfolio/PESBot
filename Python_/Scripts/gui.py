import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
from utils import Util
import threading
import time
import json
import os
from config import Config
from pathing import Pathing
import pyautogui as pg
from image_matcher import ImageMatcher
import keyboard
from captcha_solver import solve_captcha

class GUI:
    def __init__(self, root):
        
        print("Starting GUI...")

        self.mineral_json = "C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\DATA_\\json\\mineral_points.json"
        self.pathing_json = "C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\DATA_\\json\\pathing_points.json"
        
        self.dynamic_message = tk.StringVar()
        
        self.root = root
        self.root.title("PESBot")
        self.root.geometry("500x400")

        self.x0 = 200
        self.y0 = 200
        self.player_pos = (0, 0)
        self.time_between_mining_int = 7
        self.time_between_mining_str = "7"

        # Create a Canvas to hold the background image
        self.canvas = tk.Canvas(self.root, background="#fcfcfc")
        self.canvas.pack(fill="both", expand=True)

        # Load the background image
        background_image = Image.open("C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Config_\\background.jpg")
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Create a label to hold the background image on the canvas
        self.background_label = self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Create a frame with an off-white background and a black border
        self.frame_1 = tk.Frame(self.canvas, bg="#c7c3a7", bd=2, relief="solid")  # Use an off-white color
        #self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame_1.place(x=self.x0, y=self.y0, anchor="center")

        # Create a frame with an off-white background and a black border
        self.frame_2 = tk.Frame(self.canvas, bg="#c7c3a7", bd=2, relief="solid")  # Use an off-white color
        #self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame_2.place(x=self.x0, y=self.y0, anchor="center")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.util = Util()
        self.config = Config()
        self.grid = Pathing()
        self.image_matcher = ImageMatcher()

        self.util.set_dimensions("WAKFU")
        self.start_stop = False
        self.start_stop_string = "Start"
        
        #Get mineral points from last session
        with open(self.mineral_json, 'r') as file:
            json_mineral_points = json.load(file)

        self.mineral_points = json_mineral_points['mineral_points']
        
        #Get pathing points from last session
        with open(self.pathing_json, 'r') as file: 
            json_pathing_points = json.load(file)
        
        self.pathing_points = json_pathing_points['pathing_points']

        self.player_position = tk.StringVar()
        self.mouse_position = tk.StringVar()
        self.time_variable = tk.StringVar()
        self.hold_variable = tk.StringVar()

        self.time_between_mining_int = 7
        self.time_between_mining_str = "7"

        self.hold_move = 1

        self.disabled = "normal"  # Set this to "disabled" when you want to disable the save buttons
        self.start_stop_loop_thread = threading.Thread(target=self.start_stop_loop)
        
        self.create_widgets_page_1()

    def create_widgets_page_1(self):

        self.welcome_label = tk.Label(self.frame_1, text="PESBot", bg="#c7c3a7", fg="black", font=("Bodoni", 20))
        self.welcome_label.grid(row=0, column=0, pady=5, padx=5)

        # Memory buttons
        self.use_last_memory_location_button = tk.Button(self.frame_1, text="Use last saved memory location", command=self.create_widgets_page_2, bg="#a6a390", fg="black")
        self.use_last_memory_location_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.find_memory_location_button = tk.Button(self.frame_1, text="Find memory location", command=self.read_memory_option, bg="#a6a390", fg="black") #add command=self.find_memory_location,
        self.find_memory_location_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Quit Button
        quit_button = tk.Button(self.frame_1, text="Quit", command=self.quit_application, bg="#a6a390", fg="black")
        quit_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.reminder_label = tk.Label(self.frame_1, text="Reminder: If you have restarted your game, select find memory location..", bg="#a6a390", fg="black")
        self.reminder_label.grid(row=4, column=0, pady=5, padx=5)

    def create_widgets_page_2(self):
        # Destroy the widgets from the previous page
        self.frame_1.destroy()

        self.welcome_label_2 = tk.Label(self.frame_2, text="PESBot", bg="#c7c3a7", fg="black", font=("Bodoni", 20))
        self.welcome_label_2.grid(row=0, column=0, pady=5, padx=5)

        # Player Position Label
        player_label = tk.Label(self.frame_2, text="Player Position:", bg="#a6a390", fg="black")
        player_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        player_display = tk.Label(self.frame_2, textvariable=self.player_position, bg="#a6a390", fg="black")
        player_display.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Mouse Position Label
        mouse_label = tk.Label(self.frame_2, text="Mouse Position:", bg="#a6a390", fg="black")
        mouse_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")
        mouse_display = tk.Label(self.frame_2, textvariable=self.mouse_position, bg="#a6a390", fg="black")
        mouse_display.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # Start/Stop Button
        self.start_stop_button = tk.Button(self.frame_2, text=f"{self.start_stop_string}", command=self.toggle_start_stop, bg="#a6a390", fg="black")
        self.start_stop_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Save Mineral Points Button
        save_mineral_button = tk.Button(self.frame_2, text="Save Mineral Point", command=self.save_mineral_point, state=f"{self.disabled}", bg="#a6a390", fg="black")
        save_mineral_button.grid(row=4, column=0, pady=5, padx=5, sticky="w")

        # Label for updating time
        update_time_label = tk.Label(self.frame_2, textvariable=f"{self.time_variable}", bg="#a6a390", fg="black")
        update_time_label.grid(row=1, column=2, pady=5, padx=5, sticky="w")

        # Add time button
        add_time_button = tk.Button(self.frame_2, text="+", command = self.add_time, state=f"{self.disabled}", bg="#a6a390", fg="black")
        add_time_button.grid(row=2, column=2, pady=5, padx=5, sticky="w")

        # Subtract time button 
        subtract_time_button = tk.Button(self.frame_2, text="-", command= self.subtract_time, state=f"{self.disabled}", bg="#a6a390", fg="black")
        subtract_time_button.grid(row=2, column=3, pady=5, padx=5, sticky="w")

        # Label for updating time
        update_move_label = tk.Label(self.frame_2, textvariable=f"{self.hold_variable}", bg="#a6a390", fg="black")
        update_move_label.grid(row=3, column=2, pady=5, padx=5, sticky="w")

        # Add time button
        add_move_button = tk.Button(self.frame_2, text="+", command = self.add_hold, state=f"{self.disabled}", bg="#a6a390", fg="black")
        add_move_button.grid(row=4, column=2, pady=5, padx=5, sticky="w")

        # Subtract time button 
        subtract_move_button = tk.Button(self.frame_2, text="-", command= self.subtract_hold, state=f"{self.disabled}", bg="#a6a390", fg="black")
        subtract_move_button.grid(row=4, column=3, pady=5, padx=5, sticky="w")


        #Clear Mineral Points Button
        clear_mineral_points_button = tk.Button(self.frame_2, text="Clear Mineral Points", command=self.clear_mineral_points, state=f"{self.disabled}", bg="#a6a390", fg="black")
        clear_mineral_points_button.grid(row=5, column=0, pady=5, padx=5, sticky="e")

        # Save Pathing Points Button
        save_pathing_button = tk.Button(self.frame_2, text="Save Pathing Point", command=self.save_pathing_point, state=f"{self.disabled}", bg="#a6a390", fg="black")
        save_pathing_button.grid(row=4, column=1, pady=5, padx=5, sticky="e")
        
        # Clear Pathing Points Button
        clear_pathing_points_button = tk.Button(self.frame_2, text="Clear Pathing Points", command=self.clear_pathing_points, state=f"{self.disabled}", bg="#a6a390", fg="black")
        clear_pathing_points_button.grid(row=5, column=1, pady=5, padx=5, sticky="e")

        # Quit Button
        quit_button = tk.Button(self.frame_2, text="Quit", command=self.quit_application, bg="#a6a390", fg="black")
        quit_button.grid(row=7, column=0, columnspan=2, pady=5)

        #Message at the bottom
        message_label = tk.Label(self.root, textvariable=self.dynamic_message)
        message_label.pack(side=tk.BOTTOM)
    
    def add_time(self):
        self.time_between_mining_int += 0.25
        print(self.time_between_mining_int)
        self.time_between_mining_str = str(self.time_between_mining_int)
    
    def subtract_time(self):
        self.time_between_mining_int -= 0.25
        print(self.time_between_mining_int)
        self.time_between_mining_str = str(self.time_between_mining_int)

    def add_hold(self):
        self.hold_move += 0.25
        self.hold_variable.set(f"{self.hold_move}")
    
    def subtract_hold(self):
        self.hold_move -= 0.25
        self.hold_variable.set(f"{self.hold_move}")
        
    def quit_application(self):
        with open(self.config.PLAYER_LAST_LOCATION, 'w') as file:
            x, y = self.player_pos[0], self.player_pos[1]
            file.write(f"{x}:{y}")
        print(f"Saved last player location: {x},{y}")
        self.root.destroy()
    
    def read_memory_option(self):
        os.startfile(self.config.SCANNER_PATH)

    def update_positions(self):
        self.x0 = self.root.winfo_width()//2
        self.y0 = self.root.winfo_height()//2
        
        if(self.frame_1.winfo_exists()):
            self.frame_1.place(x=self.x0, y=self.y0, anchor="center")
        else:
            self.frame_2.place(x=self.x0, y=self.y0, anchor="center")

        # Update player and mouse positions
        self.player_pos = self.util.read_coordinates(True)
        self.player_position.set(f"X: {self.player_pos[0]}, Y: {self.player_pos[1]}")

        mouse_pos = pyautogui.position()
        self.mouse_position.set(f"X: {mouse_pos.x}, Y: {mouse_pos.y}")

        self.time_variable.set(f"{self.time_between_mining_str}")

        self.root.after(100, self.update_positions)

    def toggle_start_stop(self):
        if not self.start_stop:
            self.start_stop = True
            self.start_stop_loop_thread = threading.Thread(target=self.start_stop_loop)
            self.start_stop_loop_thread.start()
        else:
            self.start_stop = False
            self.start_stop_string = "Start"
            self.start_stop_loop_thread.join()
            if(self.start_stop_loop_thread.is_alive()):
                print("\nThread is still alive!")
            else:
                print("\nThread is dead!")
        
        
        self.start_stop_button.config(text=f"{self.start_stop_string}")

    def start_stop_loop(self):
        self.disabled = "disabled"
        self.start_stop_string = "Stop"
        print("Thread started")
        i=0
        found_minerals = []
        maxLength = 300
        fail_count = 0
        mount = False
        failed = False

        while self.start_stop and keyboard.is_pressed('q') == False:
            if i == len(self.pathing_points):
                i = 0
            #checking range of minerals for each mineral in list.
            for x in range(len(self.mineral_points)):
                
                #Check minerals list, for each mineral in mineral list,
                #check to see if its within a 6 cell range, if it is, use
                #image_matcher, if it returns true, add x,y to found_minerals
                #list, and mine it.

                #send pixel coordinates of each mineral to match image instead of moving mouse
                coord = self.grid.move_mouse(self.util.calculate_cells(self.util.read_coordinates(True), self.mineral_points[x]))
                if int(coord[0]) in range(0, 1000) and int(coord[1]) in range(0, 800):
                    try:
                        mouse_x, mouse_y = coord[0], coord[1]

                        # Calculate the coordinates for the image region around the mouse position
                        image_x = max(0, int(mouse_x) - 25)
                        image_y = max(0, int(mouse_y) - 25)
                        image_width = 50
                        image_height = 50
                        
                        ss = pg.screenshot(region=(image_x, image_y, image_width, image_height))
                        
                        p = self.image_matcher.match_image_nn_mineral(ss)
                        if(p[1] > 96 and p[0] == "mineral" and self.mineral_points[x] not in found_minerals):
                            found_minerals.append(self.mineral_points[x])        

                    except Exception as e:
                        print("Error in image matching.." + e)
                        pass

            
            
            if(len(found_minerals)>0 and not failed):
                
                #if it is, mine it.
                for x in found_minerals:
                    ctm = self.util.calculate_cells(self.util.read_coordinates(True), x)

                    if(abs(ctm[0] > 3) or abs(ctm[1]>3) and not mount):
                        mount = True
                        keyboard.press_and_release('1')

                    print("\rMining...                                                 ", flush=True, end="")
                    time.sleep(0.69)
                    coords = self.grid.move_mouse(self.util.calculate_cells(self.util.read_coordinates(True), x))
                    if(int(coords[0]) in range(0, 1000) and int(coords[1]) in range(0, 800)):
                        pg.moveTo(coords[0], coords[1]-25)
                        time.sleep(0.1)
                        pg.rightClick()
                        time.sleep(0.25)
                        pg.moveRel(0, -40)
                        temp_pos = self.util.read_coordinates(True)
                        time.sleep(0.1)
                        pg.rightClick()
                        mount=False
                    else:
                        break
                    
                    if(fail_count>=2):
                        failed = True
                        break
                    
                    for x in range(2):
                        if temp_pos == self.util.read_coordinates(True):
                            time.sleep(1)

                    if temp_pos == self.util.read_coordinates(True):
                        print("\rChecking for captcha..                                ", flush=True, end="")
                        if(self.image_matcher.check_for_captcha()):
                            print("\rCaptcha detected. Solving..                       ", flush=True, end="")
                            solve_captcha()
                            break
                        print("\rMining error. Restarting loop..                       ", flush=True, end="")
                        fail_count+=1
                        break
                    
                    else:
                        time.sleep(self.time_between_mining_int)
                found_minerals.clear()

            #else move to next pathing point
            else:

                if(not mount):
                        mount=True
                        keyboard.press_and_release('1')

                #send pixel coordinates of each mineral to match image
                print("\rPathing..                                        ", flush=True, end="")
                while(self.start_stop and keyboard.is_pressed('q') == False):
                    #time.sleep(1)
                    ctm = self.util.calculate_cells(self.util.read_coordinates(True), self.pathing_points[i])
                    coord = self.grid.move_mouse(ctm)
                    if(int(coord[0]) in range(0, 1000) and int(coord[1]) in range(0, 800)):
                        pg.moveTo(self.grid.move_mouse(ctm))
                        pg.leftClick()
                        time.sleep(2)
                        break
                    
                    coords_to_pathing_point = self.grid.move_mouse(ctm)
                    pointed_vector = self.util.calculate_vector((500, 400), coords_to_pathing_point, 0.8, maxLength)
                    
                    temp_pos = self.util.read_coordinates(True)
                    pg.moveTo(pointed_vector)
                    pg.mouseDown(button="left")
                    time.sleep(self.hold_move)
                    pg.mouseUp(button="left")
                    
                    for x in range(2):
                        if temp_pos != self.util.read_coordinates(True):
                            maxLength = 300
                            fail_count = 0
                            failed = False
                            while(True):
                                temp_pos = self.util.read_coordinates(True)
                                time.sleep(0.2)
                                if(temp_pos == self.util.read_coordinates(True)):
                                    break
                            
                        elif temp_pos == self.util.read_coordinates(True):
                            print("\rChecking for captcha..                            ", flush=True, end="")
                            if(self.image_matcher.check_for_captcha()):
                                print("\rCaptcha detected. Solving..                   ", flush=True, end="")
                                solve_captcha()
                                break
                            print("\rPathing error. Changing max length..              ", flush=True, end="")
                            maxLength -= 50
                            fail_count+=1
                        if(fail_count>4):
                            fail_count = 0
                            i+=1
                            break
                            
                    
                i+=1
            
            if(failed):
                failed = False

                #if it isnt, move to next check.
                #mine each mineral until the list is empty, then move to next
                #pathing point.

                #if the pathing point is the last one, check to see if we can
                #reverse pathing iterator and go back, repeat this loop.
            
           
                
            
        

    def clear_mineral_points(self):
        # Clear the mineral points list
        self.mineral_points = []
        GUI.update_mineral_points(self)
    
    def clear_pathing_points(self):
        # Clear the mineral points list
        self.pathing_points = []
        GUI.update_pathing_points(self)

    def save_mineral_point(self):
        # Save the current player position as a mineral point
        self.mineral_points.append(self.util.read_coordinates(True))
        GUI.update_mineral_points(self)
    
    def save_pathing_point(self):
        # Save the current player position as a pathing point
        self.pathing_points.append(self.util.read_coordinates(True))
        GUI.update_pathing_points(self)

    @staticmethod
    def save_list_to_json(data, filepath):
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving JSON to {filepath}: {e}")
    
    @staticmethod
    def update_mineral_points(self):
        # Load existing data from the file
        with open(self.mineral_json, 'r') as file:
            existing_data = json.load(file)

        # Update the mineral_points key with the new list
        existing_data['mineral_points'] = self.mineral_points

        # Save the updated data back to the file
        GUI.save_list_to_json(existing_data, self.mineral_json)
    
    @staticmethod
    def update_pathing_points(self):
        # Load existing data from the file
        with open(self.pathing_json, 'r') as file:
            existing_data = json.load(file)

        # Update the pathing_points key with the new list
        existing_data['pathing_points'] = self.pathing_points

        # Save the updated data back to the file
        GUI.save_list_to_json(existing_data, self.pathing_json)
    
    #checks to see if thread is alive, if it is destroy it.
    def final_exit(self):
        try:
            if(self.start_stop_loop_thread.is_alive()):
                self.start_stop_loop_thread.join()
                print("Exitting.. Thread was still alive!")
            else:
                print("Exitting.. Thread was dead!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    # Initial message
    app.dynamic_message.set("Have fun!")

    app.create_widgets_page_1()  # Start with the initial page
    app.update_positions()  # Call update_positions initially
    root.mainloop()
    app.final_exit()
    
    


"""
MINING LOOP:

in this loop we need to do the following:
    1. check if player can see mineral points
        .. to check if we can see mineral points, we need to
        calculate the cells from the player position to the 
        mineral point, and if its over 10, we cannot see it.
        if its under 10, we can see it.

        @TODO: use the util function i just made

    2. if player can see mineral points, mine them
    3. if player cannot see mineral points, move to the next pathing point
    4. if player is at the end of the pathing points, check if it can see the
        last pathing point (the [len(pathing_points)-1] in the list)
    5. if player can see the last pathing point, move to the first pathing point
        by incrementing from len(pathing_points)-1 to 0

    
        #probably would be faster if we added a key of the pathing point
                #to each mineral point, check what pathing point we're at, then
                #check the minerals in range from that.

                #example:
                    #pathing point 41, -134 correlates to mineral points
                    #for x in mineral_points["41,-134"]:(mineral points)
                    #could be useful later, not for now.
"""