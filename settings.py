import pygame
import sys
from pygame.locals import *
from console import *

pygame.init()
#window/pygame related
WINDOWWIDTH = 1250
WINDOWHEIGHT = 900
size = (WINDOWWIDTH, WINDOWHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption ("Down on The Pit")

font = pygame.font.SysFont(None, 48)

#colors
TEXTCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1216   # 38
HEIGHT = 800  # 25
FPS = 60
TITLE = "!(a3xA)Game"
BG = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#movements
moveRight = False
moveLeft = False
jump = True
idleCheck = True
cImage = 0
countdown = 0
str_countdown = str(countdown)[0]
attack = False
fall = False

#difficulty set
if difficulty == 'good': #Easy
    playermove = 3
    addMonsterMaxRate = 10000
    rMin = 8
    rMax = 15
        
elif difficulty == 'bad': #Hard
    playermove = 8
    addMonsterMaxRate = 100000
    rMin = 2
    rMax = 8
    
elif difficulty == 'well': #Normal
    playermove = 5
    addMonsterMaxRate = 50000
    rMin = 5
    rMax = 10
        

#rects
playerRect = pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT -400, 54, 130)
attackRectR = pygame.Rect((WINDOWWIDTH/2) + 63, WINDOWHEIGHT -380, 128, 74)
attackRectL = pygame.Rect((WINDOWWIDTH/2) - 185, WINDOWHEIGHT -380, 128, 74)
attackRectNone = pygame.Rect((WINDOWWIDTH/2) - 185, WINDOWHEIGHT +500, 54, 128)
rockRect = pygame.Rect(WINDOWWIDTH-400, WINDOWHEIGHT -400, 54, 128)

x = 0 #used to time jump
score = 0
HP = 4

#sound


#sounds
#gameOverSound = pygame.mixer.Sound('gameover.wav')
#pygame.mixer.music.load('background.mid')
