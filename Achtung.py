import pygame
import random
import sys
import math
from time import sleep
import copy
import datetime
from player import player
from ability import ability
from ability import big_width
from ability import small_width
from ability import clear_screen
from ability import move_square

pygame.init()
width = 1200
height = 900
size = (width, height)
screen = pygame.display.set_mode(size)
FONTMENU = pygame.font.SysFont(None, 60)
FONT = pygame.font.SysFont(None, 40)
SMALLFONT = pygame.font.SysFont(None, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORNAGE = (255, 127, 80)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
color_list = [BLUE, ORNAGE, RED, GREEN, WHITE]
SQUARESIZE = 100

def update_board1(playing_list):
    for player in playing_list:
        pygame.draw.circle(screen, player.color, [round(player.posx), round(player.posy)], player.width)
    pygame.display.update()

def update_board(milliseconds, seconds, playing_list):
    sum = seconds * 1000000 + milliseconds
    if not (sum % 4500000 >= 0 and sum % 4500000 <= 200000):
        update_board1(playing_list)

def message_to_screen(msg, color, FONT, posx, posy):
    message = FONT.render(msg, True, color)
    screen.blit(message, [posx, posy])
    pygame.display.update()

def move_players(playing_list, player_list):
    for player1 in playing_list:
        if not player1.legal_move(screen):
            playing_list.remove(player1)
            for player2 in playing_list:
                player2.points += 1
        else:
            player1.move()
           
def update_players_dirs(playing_list):
    for player in playing_list:
        if player.is_playing:
            player.update_dir()

def create_players(move_list):
    player_list = []
    for i in range(len(players_index)):
        player_list.append(player(move_list[i], color_list[players_index[i]]))
    return player_list

def update_scores(scores, player_list):
    for i in range(len(player_list)):
        scores[i] += player_list[i].points

def present_scores(scores):
    for i in range(len(players_index)):
        msg = "player = %s"%(scores[i])
        message_to_screen(msg, color_list[players_index[i]], FONT, 925, (i+1) * 50 + 150)

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

def create_ability1(ability_list):
    num = random.randrange(4,5)
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
    if num == 2:
        ability_list.append(small_width(posx,posy))    
    if num == 3:
        ability_list.append(clear_screen(posx,posy))
    if num == 4:
        ability_list.append(move_square(posx,posy))
        
    pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))        

def create_ability(ability_list,get_in,seconds):
    if seconds % 7 == 0:
        if get_in:
            create_ability1(ability_list)
            return False
    else:
        return True

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

def ability_touched(playing_list,ability_list,active_ability_list):
    for player in (playing_list):
        posx = player.posx + math.cos(player.dir) * player.mult_forward_move
        posy = player.posy + math.sin(player.dir) * player.mult_forward_move
        for ability in (ability_list):
            if check_square(posx,posy,ability):
                active_ability_list.append((ability,player))
                return True           
    return False

def clear_ability(ability,ability_list):
    pygame.draw.rect(screen,BLACK,(ability.posx-15,ability.posy-15,30,30))
    pygame.display.update()
    ability_list.remove(ability)

def run_abilities(playing_list,ability_list,active_ability_list,seconds,ability_before_finish):
    if ability_touched(playing_list,ability_list,active_ability_list):
        active_ability_list[-1][0].execute(active_ability_list[-1][1])
        clear_ability(active_ability_list[-1][0],ability_list)
        if seconds >= 53:
            num = 60 - seconds
            active_ability_list[-1][0].time_end = 7 - num
        else:
            active_ability_list[-1][0].time_end = seconds + 7
    
    for ability in active_ability_list:
        if ability[0].time_end == seconds:
            ability[0].revert_ability(ability[1])
            ability[0].time_end += 1
            ability_before_finish.append(ability)
            active_ability_list.remove(ability)
        
    for ability in ability_before_finish:
        if ability[0].time_end == seconds:
            ability[0].update_mult_forward(ability[1])
            ability_before_finish.remove(ability)

def run_round(move_list,scores):
    player_list = create_players(move_list)
    playing_list = copy.copy(player_list)
    ability_list = []
    get_in = True
    active_ability_list = []
    ability_before_finish = []
    while len(playing_list) > 0:
        x = datetime.datetime.now()
        seconds = int(x.strftime("%S"))
        milliseconds = int(x.strftime("%f"))
        sleep(0.007)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for player in playing_list:
                    if not player.move_square:
                        if chr(event.key) == player.left:
                            player.update_dir_value = -1/55
                        if chr(event.key) == player.right:
                            player.update_dir_value = 1/55
                    else:
                        player.update_dir_value = 0
                        if chr(event.key) == player.left:
                            player.dir -= 89.55
                        if chr(event.key) == player.right:
                            player.dir += 89.55
            if event.type == pygame.KEYUP:
                for player in playing_list:
                    if chr(event.key) == player.left or chr(event.key) == player.right:
                        player.update_dir_value = 0

        update_players_dirs(playing_list)
        move_players(playing_list,player_list)
        run_abilities(playing_list,ability_list,active_ability_list,seconds,ability_before_finish)
        update_board(milliseconds,seconds,playing_list)
        get_in = create_ability(ability_list,get_in,seconds)


        
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