import pygame
import random

BLACK = (0,0,0)

class ability(object):
    def __init__(self,posx,posy):
        self.posx = posx
        self.posy = posy
        self.time_end = -1
        self.ability_num = random.randint(1,3)

    def excute_big_width(self,player):
        player.width = player.width * 2
        player.mult_forward_move = player.width + 2
        
    def excute_small_width(self,player):
        player.width = int(player.width / 2)

    def revert_mult_forward(self,player):
        player.mult_forward_move = player.width + 2

    def execute_clear_screan(self,screen):
        pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))