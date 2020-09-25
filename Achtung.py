import pygame
import random
import sys
import math
from time import sleep
import copy

pygame.init()
width = 1200
height = 900
size = (width,height)
screen = pygame.display.set_mode(size)
FONTMENU = pygame.font.SysFont(None ,60)
FONT = pygame.font.SysFont(None ,40)
SMALLFONT = pygame.font.SysFont(None ,30)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
ORNAGE = (255,127,80)
RED = (255,0,0)
GREEN = (0,255,0)
color_list = [BLUE, ORNAGE, RED, GREEN, WHITE]
SQUARESIZE = 100

class player(object):
    def __init__(self,num_player,move):
        self.color = color_list[num_player]
        self.width = 4
        self.dir = random.randint(1,360)
        self.posx = random.randint(200,700)
        self.posy = random.randint(200,700)  
        self.is_playing = True
        self.points = 0
        self.left= move[0]
        self.right = move[1]
        self.mult_forward_move = self.width + 2

    def legal_move(self, screen):
        
        if self.is_border_touched():
            return False        
        posx = self.posx + math.cos(self.dir) * self.mult_forward_move
        posy = self.posy + math.sin(self.dir) * self.mult_forward_move
        color = screen.get_at((round(posx),round(posy)))
        if color != BLACK:
            return False
        return True

    def move(self):
        self.posx += math.cos(self.dir)
        self.posy += math.sin(self.dir)

    def update_dir(self, num):
        self.dir += num

    def is_border_touched(self):
        if self.posx > 895 or self.posx < 5 or self.posy > 895 or self.posy < 5:
            return True
        return False

class ability(object):
    def __init__(self,posx,posy):
        self.posx = posx
        self.posy = posy
     
class big_width(ability):
    def execute(self,player):
        player.width = player.width*2
        player.mult_forward_move = player.width + 2

class small_width(ability):
    def execute(self,player):
        player.width = int(player.width - 1)
        player.mult_forward_move = player.width + 2

class clear_screen(ability):
    def execute(self,player):
        pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))

def update_board(playing_list):
    for player in playing_list:
        pygame.draw.circle(screen, player.color, [round(player.posx), round(player.posy)], player.width)
    pygame.display.update()

def message_to_screen(msg, color ,FONT, posx, posy):
    message = FONT.render(msg, True, color)
    screen.blit(message, [posx, posy])
    pygame.display.update()

def move_players(playing_list,player_list):
    for player1 in playing_list:
        if not player1.legal_move(screen):
            playing_list.remove(player1)
            for player2 in playing_list:
                player2.points += 1
        else:
            player1.move()
            
def update_players_dirs(playing_list, dir_list):
    i = 0
    for player in playing_list:
        if player.is_playing:
            player.update_dir(dir_list[i])
            i += 1

def create_players(move_list):
    player_list = []
    for i in range(len(players_index)):
        player_list.append(player(players_index[i], move_list[i]))
    return player_list

def update_scores(scores, player_list):
    for i in range(len(player_list)):
        scores[i] += player_list[i].points

def present_scores(scores):
    for i in range(len(players_index)):
        msg = "player = %s"%(scores[i])
        message_to_screen(msg,color_list[players_index[i]],FONT,925,(i+1) * 50 +150)

def draw_menu():
    for i in range(5):
        msg = "player %s"%(i+1)
        message_to_screen(msg,color_list[i],FONTMENU,200,(i+1) * 100)
        pygame.draw.rect(screen,WHITE,(450,(i+1) * 100, 100, 50))
        pygame.draw.rect(screen,BLACK,(455,(i+1) * 100 + 5, 90, 40))     
        pygame.draw.rect(screen,WHITE,(600,(i+1) * 100, 100, 50))
        pygame.draw.rect(screen,BLACK,(605,(i+1) * 100 + 5, 90, 40))
    message_to_screen("START",color_list[i],FONTMENU,700,700)  
    pygame.display.update()

def choose_players_moves():
    move_list = []
    global players_index
    players_index = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                if posx > 700 and posx < 850 and posy > 700 and posy< 745:
                    pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))
                    pygame.display.update()
                    return move_list
                for i in range(5):
                    if posx > 200 and posx < 370 and posy > (i + 1) * 100 and posy  <100 * (i + 1) + 50:
                        message_to_screen("choose",WHITE,SMALLFONT,465,(i + 1) * 100 + 10)
                        left = chr(get_input_from_keys())
                        pygame.draw.rect(screen,BLACK,(455,(i+1) * 100 + 5, 90, 40)) 
                        message_to_screen(left,WHITE,SMALLFONT,495,(i + 1) * 100 + 13)

                        message_to_screen("choose",WHITE,SMALLFONT,615,(i + 1) * 100 + 10)
                        right = chr(get_input_from_keys())
                        pygame.draw.rect(screen,BLACK,(605,(i+1) * 100 + 5, 90, 40))
                        message_to_screen(right,WHITE,SMALLFONT,645,(i + 1) * 100 + 13)
                        players_index.append(i)
                        move = (left,right)
                        move_list.append(move)
                                          
def get_input_from_keys():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return event.key

def create_ability(ability_list):
    num = random.randrange(1,3)
    found = False
    while not found:
        posx = random.randrange(100,801)
        posy = random.randrange(100,801)
        i = -15
        black = True
        while i <= 15 and black:
            color1 = screen.get_at((round(posx + i),round(posy - 15)))
            color2 = screen.get_at((round(posx - 15),round(posy + i)))
            color3 = screen.get_at((round(posx + i),round(posy + 15)))
            color4 = screen.get_at((round(posx + 15),round(posy + i)))
            if color1 != BLACK:
                black = False
            elif color2 != BLACK:
                black = False
            elif color3 != BLACK:
                black = False
            elif color4 != BLACK:
                black = False
            i += 1
        if i == 16:
            found = True

    if num == 1:
        ability_list.append(big_width(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))
    if num == 2:
        ability_list.append(small_width(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))
    if num == 3:
        ability_list.append(clear_screen(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))

def check_square(posx,posy,ability):
    i = -15
    while i <= 15:
        if round(posx) == ability.posx + i and round(posy) == ability.posy - 15:
            return True
        if round(posx) == ability.posx - 15 and round(posy) == ability.posy + i:
            return True
        if round(posx) == ability.posx + 15 and round(posy) == ability.posy + i:
            return True
        if round(posx) == ability.posx + i and round(posy) == ability.posy + 15:
            return True
        i+=1
    return False

def abilitys_touched(playing_list,ability_list):
    for player in (playing_list):
        posx = player.posx + math.cos(player.dir) * player.mult_forward_move
        posy = player.posy + math.sin(player.dir) * player.mult_forward_move
        for ability in (ability_list):
            if check_square(posx,posy,ability):
                ability.execute(player)
                pygame.draw.rect(screen,BLACK,(ability.posx-15,ability.posy-15,30,30))
                pygame.display.update()
                ability_list.remove(ability)
                return True
    return False

def run_round(move_list,scores):
    player_list = create_players(move_list)
    playing_list = copy.copy(player_list)
    dir_list = [0,0,0,0,0]
    ability_list = []
    count_rounds = 20
    while len(playing_list) > 0:
        sleep(0.0070)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for i in range(len(players_index)):
                    if chr(event.key) == player_list[i].left:
                        dir_list[i] = -1/55
                    if chr(event.key) == player_list[i].right:
                        dir_list[i] = 1/55
            if event.type == pygame.KEYUP:
                for i in range(len(players_index)):
                    if chr(event.key) == player_list[i].left or chr(event.key) == player_list[i].right:
                        dir_list[i] = 0
                            
        update_players_dirs(playing_list,dir_list)
        
        if abilitys_touched(playing_list,ability_list):
            pass
        move_players(playing_list,player_list)
     
        if not (count_rounds % 300 > 0 and count_rounds % 300 < 25):
            update_board(playing_list)
        if count_rounds % 500 == 0:
            create_ability(ability_list)
        count_rounds += 1
    update_scores(scores,player_list)
    
def is_game_over(scores):
    for i in range(len(players_index)):
        if scores[i] >= 5 * len(players_index):
            return True
    return False

def main():
    pygame.draw.rect(screen, WHITE, (900, 0, 5, 900))
    game_over = False 
    draw_menu()
    scores = [0,0,0,0,0]
    move_list = choose_players_moves()
    present_scores(scores)
    msg = "winning score is %s "%(5 * len(players_index))
    message_to_screen(msg,RED,SMALLFONT,960,50)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))
                run_round(move_list,scores)
                pygame.draw.rect(screen, BLACK, (905, 200, 200, 500))
                present_scores(scores)
                game_over = is_game_over(scores)           
    pygame.draw.rect(screen, BLACK, (905, 0, 200, 900))
    pygame.time.wait(10000)

main()