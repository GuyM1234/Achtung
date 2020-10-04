import pygame

BLACK = (0,0,0)
class ability(object):
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.time_end = -1

    def update_mult_forward(self,player):
        player.mult_forward_move = player.width + 2

class big_width(ability):
    def execute(self, player):
        player.width = player.width * 2
        super().update_mult_forward(player)

    def revert_ability(self, player):
        player.width = int(player.width / 2)
        
class small_width(ability):
    def execute(self, player):
        player.width = player.width - 1
        super().update_mult_forward(player)

    def revert_ability(self, player):
        player.width = int(player.width / 2)
        super().update_mult_forward(player)
        
class clear_screen(ability):
    def execute(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))

class move_square(ability):
    def execute(self, player):
        player.update_dir_value = 0
        player.move_square = True

    def revert_ability(self, player):
        player.move_square = False

class move_fast(ability):
    def execute(self,player):
        player.move_times += 1
        
    def revert_ability(self, player):
        player.move_times -= 1