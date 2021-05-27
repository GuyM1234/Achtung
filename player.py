import pygame
import random
import math

BLACK = (0,0,0)
WHITE = (255, 255, 255)

class player(object):
    def __init__(self,move,color):
        self.color = color
        self.width = 4
        self.dir = random.randint(1,360)
        self.posx = random.randint(200,700)
        self.posy = random.randint(200,700)  
        self.is_playing = True
        self.points = 0
        self.left= move[0]
        self.right = move[1]
        self.move_square = False
        self.update_dir_value = 0
        self.move_times = 1
    
    # check to see if the move is legal
    def legal_move(self, screen):
        if self.is_border_touched():
            return False        
        posx = self.posx + math.cos(self.dir) * 6
        posy = self.posy + math.sin(self.dir) * 6
        color = screen.get_at((round(posx),round(posy)))
        if color != BLACK and color !=WHITE:
            return False
        return True

    def move(self):
        self.posx += math.cos(self.dir)
        self.posy += math.sin(self.dir)

    def update_dir(self):
        self.dir += self.update_dir_value

    def is_border_touched(self):
        if self.posx > 893 or self.posx < 7 or self.posy > 893 or self.posy < 7:
            return True
        return False