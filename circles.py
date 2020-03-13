import pygame
import game_def
import circle_def
import random
import math
import sys

CURRENT_LEVEL = 1

def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        GAME.high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", GAME.high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
 
    return high_score
 
 
def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")

def draw_player(x,y):    
    pygame.draw.circle(win, BLUE, (PLAYER.x,PLAYER.y), PLAYER.size, PLAYER.size)
    if (PLAYER.shield_one > 0):
        pygame.draw.circle(win, MAGENTA, (PLAYER.x,PLAYER.y), PLAYER.size + 5, PLAYER.shield_one)
    if (PLAYER.shield_two > 0):
        i = 0
        while i < PLAYER.shield_two:
            if i == 0:
                pygame.draw.circle(win, L_YELLOW, (PLAYER.x + PLAYER.size,PLAYER.y + PLAYER.size), int(PLAYER.size / 4), 1)
            elif i == 1:
                pygame.draw.circle(win, L_YELLOW, (PLAYER.x - PLAYER.size,PLAYER.y + PLAYER.size), int(PLAYER.size / 4), 1)
            elif i == 2:
                pygame.draw.circle(win, L_YELLOW, (PLAYER.x + PLAYER.size,PLAYER.y - PLAYER.size), int(PLAYER.size / 4), 1)
            elif i == 3:
                pygame.draw.circle(win, L_YELLOW, (PLAYER.x - PLAYER.size,PLAYER.y - PLAYER.size), int(PLAYER.size / 4), 1)
            i += 1

def distance(x1,y1,x2,y2):
    dist = ((x1 - x2)**2 + (y1-y2)**2)**.5
    return dist

def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def show_score():
    
    coin_string = "Coin:  " + str(PLAYER.gold)		
    tSurface, tRect = text_objects(coin_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (700, 440)
    win.blit(tSurface, tRect)
    
    speed_string = "Speed: " + str(PLAYER.speed)		
    tSurface, tRect = text_objects(speed_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (700, 480)
    win.blit(tSurface, tRect)
    
    hscore_string = "High:  " + str(GAME.high_score)		
    tSurface, tRect = text_objects(hscore_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (700, 520)
    win.blit(tSurface, tRect)
    
    score_string = "Score: " + str(PLAYER.size)		
    tSurface, tRect = text_objects(score_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (700, 560)
    win.blit(tSurface, tRect)
    pygame.display.update()
    
def show_level():
    level_string = "Level: " + str(GAME.level)
    tSurface, tRect = text_objects(level_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (700, 400)
    win.blit(tSurface, tRect)
    pygame.display.update()

def show_pause():    
    pause_string = "PAUSED"
    tSurface, tRect = text_objects(pause_string, pygame.font.SysFont('Comic Sans MS', 24, bold=True), L_GREY)		
    tRect.center = (400, 300)
    win.blit(tSurface, tRect)
    pygame.display.update()

    
    
def move_circles():
    # first the player
    if PLAYER.direction == WEST:
        if PLAYER.x > PLAYER.size:
            PLAYER.x -= 1 * PLAYER.speed
    if PLAYER.direction == EAST:
        if PLAYER.x <= display_width - PLAYER.size:
            PLAYER.x += 1 * PLAYER.speed
    if PLAYER.direction == SOUTH:
        if PLAYER.y <= display_height - PLAYER.size:
            PLAYER.y += 1 * PLAYER.speed
    if PLAYER.direction == NORTH:
        if PLAYER.y >= PLAYER.size:
            PLAYER.y -= 1 * PLAYER.speed
    if PLAYER.direction == NE:
        if PLAYER.x <= display_width - PLAYER.size and PLAYER.y >= PLAYER.size:
            PLAYER.x += 1 * PLAYER.speed
            PLAYER.y -= 1 * PLAYER.speed
    if PLAYER.direction == NW:
        if PLAYER.x > PLAYER.size and PLAYER.y >= PLAYER.size:
            PLAYER.x -= 1 * PLAYER.speed
            PLAYER.y -= 1 * PLAYER.speed
    if PLAYER.direction == SE:
        if PLAYER.x <= display_width - PLAYER.size and PLAYER.y <= display_height - PLAYER.size:
            PLAYER.x += 1 * PLAYER.speed
            PLAYER.y += 1 * PLAYER.speed
    if PLAYER.direction == SW:
        if PLAYER.x > PLAYER.size and PLAYER.y <= display_height - PLAYER.size:
            PLAYER.x -= 1 * PLAYER.speed
            PLAYER.y += 1 * PLAYER.speed
    
    # now loop through the enemies
    i = 0
    for obj in CIRCLES:	
        if CIRCLES[i].direction == WEST:
            if CIRCLES[i].x <= CIRCLES[i].size:
                CIRCLES[i].direction = random.randint(NORTH, SOUTH)
                continue
            if random.randint(1,100) < 3:
                CIRCLES[i].direction = random.randint(1,4)
                continue
            CIRCLES[i].x -= 1 * CIRCLES[i].speed
        if CIRCLES[i].direction == EAST:
            if CIRCLES[i].x >= display_width - CIRCLES[i].size:
                CIRCLES[i].direction = random.randint(NORTH, SOUTH)
                continue
            if random.randint(1,100) < 3:
                CIRCLES[i].direction = random.randint(1,4)
                continue
            CIRCLES[i].x += 1 * CIRCLES[i].speed
        if CIRCLES[i].direction == SOUTH:
            if CIRCLES[i].y >= display_height - CIRCLES[i].size:
                CIRCLES[i].direction = random.randint(EAST, WEST)
                continue
            if random.randint(1,100) < 3:
                CIRCLES[i].direction = random.randint(1,4)
                continue
            CIRCLES[i].y += 1 * CIRCLES[i].speed
        if CIRCLES[i].direction == NORTH:
            if CIRCLES[i].y <= CIRCLES[i].size:
                CIRCLES[i].direction = random.randint(EAST, WEST)
                continue
            if random.randint(1,100) < 3:
                CIRCLES[i].direction = random.randint(1,4)
                continue
            CIRCLES[i].y -= 1 * CIRCLES[i].speed
        if CIRCLES[i].direction == NE:
            if CIRCLES[i].x <= display_width - CIRCLES[i].size and CIRCLES[i].y >= CIRCLES[i].size:
                CIRCLES[i].x += 1 * CIRCLES[i].speed
                CIRCLES[i].y -= 1 * CIRCLES[i].speed
            else:
                CIRCLES[i].direction = random.randint(1,8)
        if CIRCLES[i].direction == NW:
            if CIRCLES[i].x > CIRCLES[i].size and CIRCLES[i].y >= CIRCLES[i].size:
                CIRCLES[i].x -= 1 * CIRCLES[i].speed
                CIRCLES[i].y -= 1 * CIRCLES[i].speed
            else:
                CIRCLES[i].direction = random.randint(1,8)
        if CIRCLES[i].direction == SE:
            if CIRCLES[i].x <= display_width - CIRCLES[i].size and CIRCLES[i].y <= display_height - CIRCLES[i].size:
                CIRCLES[i].x += 1 * CIRCLES[i].speed
                CIRCLES[i].y += 1 * CIRCLES[i].speed
            else:
                CIRCLES[i].direction = random.randint(1,8)
        if CIRCLES[i].direction == SW:
            if CIRCLES[i].x > CIRCLES[i].size and CIRCLES[i].y <= display_height - CIRCLES[i].size:
                CIRCLES[i].x -= 1 * CIRCLES[i].speed
                CIRCLES[i].y += 1 * CIRCLES[i].speed
            else:
                CIRCLES[i].direction = random.randint(1,8)
        i += 1
    
def check_collision():
    i = 0
    x = 0
    
    for obj in CIRCLES:
        if distance(PLAYER.x, PLAYER.y, CIRCLES[i].x, CIRCLES[i].y) < PLAYER.size + CIRCLES[i].size:
            if CIRCLES[i].alignment == GOOD:
                PLAYER.size += CIRCLES[i].size
                grow_effect.play()
                if PLAYER.size > GAME.high_score:
                    GAME.high_score = PLAYER.size
                    save_high_score(PLAYER.size)
                CIRCLES.pop(i)
            elif CIRCLES[i].alignment == SPD_BOOST:
                PLAYER.speed += 1
                CIRCLES.pop(i)
                speed_effect.play()
            elif CIRCLES[i].alignment == COIN:
                PLAYER.gold += CIRCLES[i].size
                CIRCLES.pop(i)
                coin_effect.play()
            elif CIRCLES[i].alignment == SHIELD_ONE:
                PLAYER.shield_one += CIRCLES[i].size
                CIRCLES.pop(i)
                shield_one_effect.play()
            elif CIRCLES[i].alignment == SHIELD_TWO:
                PLAYER.shield_two += CIRCLES[i].size
                if PLAYER.shield_two > 4:
                    PLAYER.shield_two = 4
                CIRCLES.pop(i)
                shield_two_effect.play()
            elif CIRCLES[i].alignment == BAD:
                if (PLAYER.shield_one > 0):
                    PLAYER.shield_one -= 1
                elif (PLAYER.shield_two > 0):
                    PLAYER.shield_two -= 1
                else:
                    PLAYER.size -= CIRCLES[i].size
                shrink_effect.play()
                CIRCLES.pop(i)
                if PLAYER.size < 1:
                    print("You died!")
                    pygame.quit()
                    quit()
        
        for obj2 in CIRCLES:
            try:
                if distance(CIRCLES[i].x, CIRCLES[i].y, CIRCLES[x].x, CIRCLES[x].y) < CIRCLES[i].size + CIRCLES[x].size:                
                    if CIRCLES[i].alignment == BAD and CIRCLES[x].alignment == BAD and i != x:
                        CIRCLES[i].size += CIRCLES[x].size 
                        if CIRCLES[i].size > CIRCLES[x].size:
                            del CIRCLES[x]   
                        elif CIRCLES[x].size >= CIRCLES[i].size:
                            del CIRCLES[i]  
                
            except:
                print ("Error, out of range in CIRCLES array "+ str(i) + " " + str(x))                    
        x += 1
        i += 1
                
        
        
        
        

def new_circle(): 
    circle_type = random.randint(1,100)
    
    if circle_type < 35:
        CIRCLES.append(circle_def.Player(random.randint(10,800), random.randint(10,600), GAME.level * random.randint(2,15), random.randint(1,8), GAME.level * random.randint(2,7), 1, 0))
    else:
        type = random.randint(1,7)
        
        if (type > 5): #shield one
            CIRCLES.append(circle_def.Player(random.randint(10,800), random.randint(10,600), random.randint(1,2), random.randint(1,8), GAME.level * random.randint(2,7), type, 0))
        else:
            CIRCLES.append(circle_def.Player(random.randint(10,800), random.randint(10,600), GAME.level * random.randint(2,15), random.randint(1,8), GAME.level * random.randint(2,7), type, 0))
        
    

def draw_other_circles():            
    i = 0
    for obj in CIRCLES:		
        if CIRCLES[i].alignment == BAD:
            pygame.draw.circle(win, RED, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        elif CIRCLES[i].alignment == GOOD:
            pygame.draw.circle(win, GREEN, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        elif CIRCLES[i].alignment == SPD_BOOST:
            pygame.draw.circle(win, WHITE, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        elif CIRCLES[i].alignment == COIN:
            pygame.draw.circle(win, YELLOW, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        elif CIRCLES[i].alignment == SHIELD_ONE:
            pygame.draw.circle(win, MAGENTA, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        elif CIRCLES[i].alignment == SHIELD_TWO:
            pygame.draw.circle(win, L_YELLOW, (CIRCLES[i].x,CIRCLES[i].y), CIRCLES[i].size, CIRCLES[i].size)
        i += 1
    
    
    
def main_loop():
    time = 0
    level_time = 0    
    music_paused = True
    pygame.mixer.music.pause()
    PAUSED = False
    high_score = get_high_score()
	  
    while GAME.state == PLAYING:
        
        pygame.time.delay(100)
		
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()						
				
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP4]:
            PLAYER.direction = WEST            
        if keys[pygame.K_KP6]:
            PLAYER.direction = EAST
        if keys[pygame.K_KP8]:
            PLAYER.direction = NORTH
        if keys[pygame.K_KP2]:
            PLAYER.direction = SOUTH
        if keys[pygame.K_KP9]:
            PLAYER.direction = NE
        if keys[pygame.K_KP7]:
            PLAYER.direction = NW
        if keys[pygame.K_KP3]:
            PLAYER.direction = SE
        if keys[pygame.K_KP1]:
            PLAYER.direction = SW
            
        if keys[pygame.K_p]:
            if PAUSED == False:
                pygame.mixer.music.pause()
                music_paused = True
                PAUSED = True
                show_pause() 
                continue
            else:
                PAUSED = False
                pygame.mixer.music.unpause()
                music_paused = False
        if keys[pygame.K_m]:
            if music_paused == False:
                pygame.mixer.music.pause()
                music_paused = True                
            elif music_paused == True:
                pygame.mixer.music.unpause()
                music_paused = False
        if keys[pygame.K_F1]:
            PLAYER.speed = 5
            PLAYER.size = 10
            PLAYER.x = 10
            PLAYER.y = 10
            CIRCLES = []
            a = 10
            while a > 0:
                new_circle()
                a -= 1
        
        if PAUSED == True:
            continue
        
        win.fill(BLACK) #clear screen.
        move_circles()
        draw_player(PLAYER.x, PLAYER.y)
        draw_other_circles()                
        
        time += 1        
        level_time += 1
        
        if level_time > (LEVEL_TIMER * 10):
            level_time = 0
            GAME.level += 1
            print ("Level up!")
        
        if time > (TIMER * 10):
            time = 0
            new_circle()
       
            #print("Circles! memory usage: " + str(sys.getsizeof(CIRCLES)) + " bytes")
            
        check_collision()        
        show_score()
        show_level()
        pygame.display.update()        
        
    
    
#colors
BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
BLUE = (0,0,255)
L_ORANGE = (255, 153, 51)
L_GREY = (191, 191, 191)
D_ORANGE = (204, 82, 0)
D_GREY = (38, 38, 38)
YELLOW = (255, 204, 0)
GREEN = (0, 255, 0)
MAGENTA = (203, 52, 153) #first shield
L_YELLOW = (255, 255, 153) #second shield

#circle types
BAD = 1
PLYR = 2
GOOD = 3
SPD_BOOST = 4
COIN = 5
SHIELD_ONE = 6
SHIELD_TWO = 7

#directions
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4
NE = 5
NW = 6
SE = 7
SW = 8

#circle timer, sets time in seconds in between new enemies
TIMER = 2

#level timer
LEVEL_TIMER = 45

#game states
PLAYING = 0
PAUSED = 1
START_SCREEN = 2


#display variables
display_width = 800
display_height = 600

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load('background.mp3')

#pygame.mixer.music.play(-1)

#initialize main window and do layout
win = pygame.display.set_mode((display_width, display_height))
win.fill(BLACK)
pygame.display.set_caption("Circles!")

speed_effect = pygame.mixer.Sound("speed_up.wav")
shrink_effect = pygame.mixer.Sound("shrink.wav")
grow_effect = pygame.mixer.Sound("grow.wav")
level_effect = pygame.mixer.Sound("level.wav")
coin_effect = pygame.mixer.Sound("coin.wav")
shield_one_effect = pygame.mixer.Sound("shield_one.wav")
shield_two_effect = pygame.mixer.Sound("shield_two.wav")


GAME = game_def.Game(1,PLAYING,0)
PLAYER = circle_def.Player(10, 10, 10, SOUTH, 5, PLYR, 0)

CIRCLES = []

a = 10
while a > 0:
    new_circle()
    a -= 1

main_loop()