import pygame
import sys
import random
import time
from pygame.locals import *
from pygame.constants import *
from settings import *
from classes import *

class Game: #CLASS GAME LOCATED HERE FOR EASY ACCESS
    def __init__(self):
        #game initialization
        pygame.mixer.pre_init(44100,-16,2,1024) 
        pygame.init() 
        self.clock = pygame.time.Clock()

        #some sounds n stuff
        backgroundMusic = pygame.mixer.music.load('files/sounds/celesteBG.mp3')
        self.hit = pygame.mixer.Sound('files/sounds/hit.wav')
        self.over = pygame.mixer.Sound('files/sounds/over.wav')
        
        self.scorePlaceholder = pygame.image.load("files/sprites/score.png").convert_alpha()
        self.startBG = pygame.image.load("files/sprites/startBG.jpg")

        #define interface (User Interface) sprites
        self.UI0 = pygame.image.load("files/sprites/0.png").convert_alpha()
        self.UI1 = pygame.image.load("files/sprites/1.png").convert_alpha()
        self.UI2 = pygame.image.load("files/sprites/2.png").convert_alpha()
        self.UI3 = pygame.image.load("files/sprites/3.png").convert_alpha()
        
        self.UIRect = pygame.Surface.get_rect(self.UI0)
        self.currentUI = self.UI3
        #self.filter = pygame.image.load("files/sprites/filter.png").convert_alpha()
        self.scorePhRect = pygame.Surface.get_rect(self.scorePlaceholder)
        self.highScore = 0

        self.addMonster = self.addMonster = random.randint(0,20000)
        self.addBat = 0
        self.addSlime = 0

    def music(self):
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def wait_key_press(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Pressing ESC quits.
                        self.quit_game()
                    return

    
    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, 1, WHITE)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
   
    def quit_game(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        screen.blit(self.startBG,(0,0))
        self.draw_text('Welcome to: Down on The Pit', font, screen, 0 + 30, (WINDOWHEIGHT / 3))
        self.draw_text('HIGHSCORE: ' + str(self.highScore), font, screen, 0 + 30, 0+30)
        self.draw_text('Press anything to continue.', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 100)
        self.draw_text('Esc to Exit.', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 150)

        self.draw_text('> X - To cast Fire (beware of cooldown)', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 400)
        self.draw_text('> L/R Arrows or A/D - To move', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 300)
        self.draw_text('> Space or Up Arrow - To jump', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 350)
        pygame.display.update()
        self.wait_key_press()
        
    def info_screen(self):
        screen.blit(self.startBG,(0,0))
        self.draw_text('As time progresses the game becomes harder!', font, screen, 0 + 30, (WINDOWHEIGHT / 3))
        self.draw_text('HIGHSCORE: ' + str(self.highScore), font, screen, 0 + 30, 0+30)
        self.draw_text('You are stranded in a pit, all you have left to do', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 100)
        self.draw_text('is gather the gold pieces!', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 150)
        self.draw_text('Good Luck!', font, screen, 0 + 30, (WINDOWHEIGHT / 3) + 200)
        
        pygame.display.update()
        self.wait_key_press()
        
    def hp_UI(self,HP): #update hp UI if hp goes down
        self.HP = HP
        self.UIRect.right = WINDOWWIDTH-2
        self.UIRect.top = 0+2

        if self.HP == 3:
            self.currentUI = self.UI3
        elif self.HP == 2:
            self.currentUI = self.UI2
        elif self.HP == 1:
            self.currentUI = self.UI1
        elif self.HP == 0:
            self.currentUI = self.UI0

    def add_monsters(self,addMonsterMaxRate): #"faint" chance a new monster will appear
        self.addMonsterMaxRate = addMonsterMaxRate
        self.addMonster = random.randint(0,self.addMonsterMaxRate)
        if self.addMonster <= 100:
            #Bat = 0  MAX = 3 BATS
            #Slime = 1  MAX = 2 SLIMES
            self.addMonster = random.randint(0,2)
            if self.addMonster == 0:
                self.addBat += 1
            else:
                self.addSlime +=1
                
    def end(self,Score):
        self.score = Score
        if self.score >= self.highScore:
            self.highScore = self.score
        self.score = 0
        self.start_screen()
        self.info_screen()
        
        
        

    def updates(self,score):
        #screen.blit(self.filter, [0, 0])
        screen.blit(self.scorePlaceholder, [0, 0])
        self.draw_text(str(score), font, screen, self.scorePhRect.right, self.scorePhRect.center[1]-16)
        screen.blit(self.currentUI, self.UIRect)
        
        self.clock.tick(FPS)
        pygame.display.flip()
        screen.fill(BG)
        

restart = True
game = Game()
game.start_screen()
game.info_screen()
game.music()

while True:
    if restart:
        pygame.mixer.Sound.play(game.hit)
        player = Player(playerRect,attackRectR,attackRectL,attackRectNone,screen)
        rock = Rocks(playerRect,rockRect,screen,WINDOWWIDTH,WINDOWHEIGHT,playermove,rMin,rMax)
        plat = Platforms_And_Gold(playerRect,rockRect,screen,WINDOWWIDTH,WINDOWHEIGHT,playermove)
        plat.score = score

        move = movement()

        ####init game
        plat.new_plats_coins()

        bat1 = Bat(playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,plat.jumpspeedDown,plat.jumpspeedUp,playermove,player.aRect)
        bat2 = Bat(playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,plat.jumpspeedDown,plat.jumpspeedUp,playermove,player.aRect)
        bat3 = Bat(playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,plat.jumpspeedDown,plat.jumpspeedUp,playermove,player.aRect)
    
        slime1 = Slime(playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,plat.jumpspeedDown,plat.jumpspeedUp,plat.groundPlats[0],plat.groundPlats[len(plat.groundPlats)-1],playermove,player.aRect)
        slime2 = Slime(playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,plat.jumpspeedDown,plat.jumpspeedUp,plat.groundPlats[0],plat.groundPlats[len(plat.groundPlats)-1],playermove,player.aRect)

        bg = Background(screen)
        HP -= 1
        restart = False

        bat1.restart = restart
        bat2.restart = restart
        bat3.restart = restart

        slime1.restart = restart
        slime2.restart = restart

    #pygame.draw.rect(screen,RED,playerRect)
    bg.update()
    bg.render()
    
    move.move_input(player.cooldown)

    player.movement()
    player.update()
    player.render()
        
    game.add_monsters(addMonsterMaxRate)
    
    bat1.follow(HP,player.aRect)
    bat1.update()
    bat1.render()
    if game.addBat >= 1:
        bat2.follow(HP,player.aRect)
        bat2.update()
        bat2.render()
    if game.addBat >= 2:
        bat3.follow(HP,player.aRect)
        bat3.update()
        bat3.render()

    slime1.follow(HP,player.aRect)
    slime1.update()
    slime1.render()
    if game.addSlime >= 1:
        slime2.follow(HP,player.aRect)
        slime2.update()
        slime2.render()
    
    rock.add_rocks()
    rock.move()
    rock.colision()
    rock.update()
    rock.render()

    plat.movement_input(bat1.bounce)
    plat.falling(restart)
    plat.gold_pickup()
    plat.update()
    plat.render()
    score = plat.score
    
    #bat1.playerRect = player.rect
    #slime1.playerRect = player.rect
    #rock.playerRect = player.rect

    if player.cooldown == True: #draw the cooldown icon
        countdown += 1
        if countdown >= 10:
            str_countdown = str(countdown)[0]
        else:
            str_countdown = '0'
        screen.blit(player.currentAStatus, [0+2, WINDOWHEIGHT-60])
        game.draw_text('0.'+str_countdown, font, screen, 0+2, WINDOWHEIGHT-60)
    else:
        countdown = 0
        screen.blit(player.currentAStatus, [0+2, WINDOWHEIGHT-60])


    #END GAME CHECK/////////////////////
    if HP <= 2:
        if plat.score == 15 or plat.score == 30 or plat.score == 50 or plat.score == 100 or plat.score == 200:
            HP += 1
    if HP <= 0:
        pygame.mixer.Sound.play(game.over)
        print('YOU LOOSE')
        HP = 3
        game.end(plat.score)
        plat.score = 0
        score = plat.score
        restart = True
        game.addBat = 0
        game.addSlime = 0
        #pygame.mixer.Sound.play(self.deathSound)
        #quit FUNC
    
    game.hp_UI(HP)
    game.updates(plat.score)
    
    restart = plat.restart
    if bat1.restart:
        restart = bat1.restart
    elif bat2.restart:
        restart = bat2.restart
    elif bat3.restart:
        restart = bat3.restart
    elif slime1.restart:
        restart = slime1.restart
    elif slime2.restart:
        restart = slime2.restart
    elif rock.restart:
        restart = rock.restart           
