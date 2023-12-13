from utils import Util
import pyautogui as pg

class Pathing():
    def __init__(self):
        self.util = Util()
        self.util.set_dimensions("WAKFU")
        self.center = (500, 400)
        self.captcha_center = (425, 370)

    def main():
        pass
    
    def move_mouse(self, cells):
        start = self.center
        if(cells[0] > 0):
            start = Pathing.move_mouse_down(cells[0], start)
        elif(cells[0] < 0):
            start = Pathing.move_mouse_up(abs(cells[0]), start)
        
        if(cells[1] > 0):
            start = Pathing.move_mouse_right(cells[1], start)
        elif(cells[1] < 0):
            start = Pathing.move_mouse_left(abs(cells[1]), start)
        
        return(start)

    def captcha_move(self, cells):
        start = self.captcha_center
        if(cells[0] > 0):
            start = Pathing.move_mouse_down(cells[0], start)
        elif(cells[0] < 0):
            start = Pathing.move_mouse_up(abs(cells[0]), start)
        
        if(cells[1] > 0):
            start = Pathing.move_mouse_right(cells[1], start)
        elif(cells[1] < 0):
            start = Pathing.move_mouse_left(abs(cells[1]), start)
        
        return(start)

    @staticmethod
    def move_mouse_up(cells, start):
        return start[0] - (43.42857142857143 * cells), start[1] - (20 * cells)
    @staticmethod
    def move_mouse_down(cells, start):
        return start[0] + (43.42857142857143 * cells), start[1] + (23.02857142857143 * cells)
    @staticmethod
    def move_mouse_left(cells, start):
        return start[0] - (43.42857142857143 * cells), start[1] + (23.02857142857143 * cells)
    @staticmethod
    def move_mouse_right(cells, start):
        return start[0] + (42.42857142857143 * cells), start[1] - (20.02857142857143 * cells)


    """
    Example usage:

    //Player x, y coordinates
    start_pos = get_player_position

    //point of interest x, y coordinates
    target_pos = read_from_points_of_interest
    
    //move mouse to target_pos
    cells = (target_pos[0]-start_pos[0], start_pos[1]-target_pos[1])
    pg.moveTo(move_mouse(cells, center))
    
    """
    