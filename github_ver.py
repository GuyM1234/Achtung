import pygame
import random
import sys
import math
from time import sleep
import copy
import datetime
from player import player 
from ability import ability, clear_screen, move_square, move_fast


QuestionMark = pygame.image.load(r'QuestionMark.png')

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
YELOW = (255,255,0)
color_list = [BLUE, ORNAGE, RED, GREEN,YELOW]
SQUARESIZE = 100

# update every move of each player on to the board
def update_board1(playing_list):
    for player in playing_list:
        pygame.draw.circle(screen, player.color, [round(player.posx), round(player.posy)], player.width)
    pygame.display.update()

# making spaces in the player trace every specific period of time
def update_board(milliseconds, seconds, playing_list):
    sum = seconds * 1000000 + milliseconds
    if not (sum % 4500000 >= 0 and sum % 4500000 <= 200000):
        update_board1(playing_list)


def message_to_screen(msg, color, FONT, posx, posy):
    message = FONT.render(msg, True, color)
    screen.blit(message, [posx, posy])
    pygame.display.update()

# call the move function for each player given that his move is legal
def move_players(playing_list, player_list,ability_list):
    for player1 in playing_list:
        for i in range(player1.move_times):
            if not player1.legal_move(screen):
                playing_list.remove(player1)
                for player2 in playing_list:
                    player2.points += 1
                break
            else:
                player1.move()

# for ech player update his dir coordinated to what button the player pushed
def update_players_dirs(playing_list):
    for player in playing_list:
        if player.is_playing:
            player.update_dir()

# creating all the players and making a list of them so we could trace them easily
def create_players(move_list):
    player_list = []
    for i in range(len(players_index)):
        player_list.append(player(move_list[i], color_list[players_index[i]]))
    return player_list

#  update the scores each round
def update_scores(scores, player_list):
    for i in range(len(player_list)):
        scores[i] += player_list[i].points

# updaing the scores on the screen
def present_scores(scores):
    for i in range(len(players_index)):
        msg = "player = %s"%(scores[i])
        message_to_screen(msg, color_list[players_index[i]], FONT, 925, (i+1) * 50 + 150)

    message_to_screen("PRESS ANY KEY", WHITE, FONT, 950, 600)
    message_to_screen("TO START", WHITE, FONT, 950, 650)

# draw the menu: where tha players choose their buttons in oreder to move at any direction
def draw_menu():
    for i in range(5):
        msg = "player %s"%(i+1)
        message_to_screen(msg,color_list[i],FONTMENU,200,(i+1) * 100)
        pygame.draw.rect(screen,WHITE,(450,(i+1) * 100, 100, 50))
        pygame.draw.rect(screen,BLACK,(455,(i+1) * 100 + 5, 90, 40))     
        pygame.draw.rect(screen,WHITE,(600,(i+1) * 100, 100, 50))
        pygame.draw.rect(screen,BLACK,(605,(i+1) * 100 + 5, 90, 40))
    pygame.draw.rect(screen,WHITE,(690, 690, 155, 55))
    pygame.draw.rect(screen,BLACK,(695, 695, 145, 45))     
    message_to_screen("START",WHITE,FONTMENU,700,700)  
    pygame.display.update()

# let the players choose their moves, keeping track with each player moves in move_list
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
                #  if pressed start: continue the game
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

# get the key pushed and return the key as a move for the player
def get_input_from_keys():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return event.key

#create a random ability
def create_ability1(ability_list):
    num = random.randint(3,5)
    found = False
    # loop until a legal position for the ability in other words a vacant place for the ability to show
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
    # create one type of ability correspondingly to the random the number and paint it in white and question mark
    if num == 3:
        ability_list.append(clear_screen(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))
        screen.blit(QuestionMark,(posx-15,posy-15))
    elif num == 4:
        ability_list.append(move_square(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))
        screen.blit(QuestionMark,(posx-15,posy-15))
    elif num == 5:
        ability_list.append(move_fast(posx,posy))
        pygame.draw.rect(screen,WHITE,(posx-15,posy-15,30,30))
        screen.blit(QuestionMark,(posx-15,posy-15))   

# calls for create_ability1 every 7 seconds
def create_ability(ability_list,get_in,seconds):
    if seconds % 7 == 0:
        if get_in:
            create_ability1(ability_list)
            return False
    else:
        return True

# checks fo each player if he touched any of the abilities on the screen, if so, return the apecific ability and player
def return_ability_touched(playing_list,ability_list):
    # loop through players
    for player in playing_list:       
        if not player.is_border_touched():
            posx = player.posx + math.cos(player.dir) * 6
            posy = player.posy + math.sin(player.dir) * 6
            color = screen.get_at((round(posx),round(posy)))
            # checks to see if tocuched
            if color == WHITE:
                # loop through abilities
                for ability in ability_list:
                    range_x = posx - (ability.posx - 15)
                    range_y = (posy - (ability.posy - 15))
                    if range_x <=40  and range_x >= -10 \
                        and range_y <=40 and range_y >=-10:
                        return (ability,player)
    return None

# set the time when tha ability will stop
def update_time_end(ability,seconds):
    if seconds >= 53:
        num = 60 - seconds
        ability.time_end = 7 - num
    else:
        ability.time_end = seconds + 7

# delete the ability from ability_list and deleting the white sqare
def clear_ability(ability,ability_list):
    pygame.draw.rect(screen,BLACK,(ability.posx-15,ability.posy-15,30,30))
    pygame.display.update()
    ability_list.remove(ability)

# if ability is touched, exectue the ability and set the time when the ability will stop
def check_abilities(playing_list,ability_list,active_ability_list,seconds):
    a_and_p = return_ability_touched(playing_list,ability_list)
    if a_and_p != None:
        if type(a_and_p[0]) == clear_screen:
            a_and_p[0].execute(screen)
        else:
            a_and_p[0].execute(a_and_p[1])     
            update_time_end(a_and_p[0],seconds)
            active_ability_list.append(a_and_p)
            clear_ability(a_and_p[0],ability_list)

# checks to see if any ability has come to its end, if so rever her and remove her from the active list
def revert_abilities(active_ability_list,seconds):
    for ability in active_ability_list:
        if ability[0].time_end == seconds:
            ability[0].revert_ability(ability[1])
            active_ability_list.remove(ability)
        
# this function is all that happens during one round.
# waiting for input from player(where to move), if no input just go straight
# 1. update all the dirs correspondingly to move square
# 2. check to see if any ability was activated
# 3. check to see if any ability is finished, if so revert her influence
def run_round(move_list,scores):
    pygame.draw.rect(screen, BLACK, (940, 590, 250, 200))
    player_list = create_players(move_list)
    playing_list = copy.copy(player_list)
    ability_list = []
    get_in = True
    active_ability_list = []
    # loop untill only one is left
    while len(playing_list) > 1:
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

        # check to see if any ability was activated
        check_abilities(playing_list,ability_list,active_ability_list,seconds)

        # check to see if any ability is finished, if so revert her influence
        revert_abilities(active_ability_list,seconds)

        # move the players with all the checks that is required
        move_players(playing_list,player_list,ability_list)

        # update the board
        update_board(milliseconds,seconds,playing_list)
        get_in = create_ability(ability_list,get_in,seconds) 
    update_scores(scores,player_list)

# check to see if any of the players ha won the game 
def is_game_over(scores):
    for i in range(len(players_index)):
        if scores[i] >= 5 * len(players_index):
            return True
    return False

# get the winner player
def winner_color(players_index,scores):
     for i in range(len(scores)):
        if scores[i] >= 5 * len(players_index):
             return color_list[players_index[i]]

def main() :
    # graphics
    pygame.draw.rect(screen, WHITE, (900, 0, 5, 900))
    draw_menu()
    scores = [0,0,0,0,0]
    move_list = choose_players_moves()
    present_scores(scores)
    msg = "winning score is %s "%(5 * len(players_index))
    message_to_screen(msg,RED,SMALLFONT,960,50)
    # while game is not over continue running the rounds
    while not is_game_over(scores):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))
                run_round(move_list,scores)
                pygame.draw.rect(screen, BLACK, (905, 200, 200, 500))
                present_scores(scores)          
    pygame.draw.rect(screen, BLACK, (0, 0, 900, 900))
    message_to_screen("PLAYER WON",winner_color(players_index,scores),FONTMENU,350,350)
    pygame.time.wait(10000)

if __name__ == "__main__":
    main()