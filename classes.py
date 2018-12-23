import math, random, sys
import pygame
from pygame.locals import *
from settings import *

class Player:
    def __init__(self,playerRect,aRectR,aRectL,aRectN,screen):
        pygame.init()
        global moveLeft,moveRight,idleCheck,attack
        
        self.walkL=pygame.image.load("files/sprites/walkL.png").convert_alpha()
        self.walkR=pygame.image.load("files/sprites/walkR.png").convert_alpha()
        self.idle=pygame.image.load("files/sprites/idle.png").convert_alpha()

        self.attackR=pygame.image.load("files/sprites/attackR.png").convert_alpha()
        self.attackL=pygame.image.load("files/sprites/attackL.png").convert_alpha()
        self.attackU=pygame.image.load("files/sprites/attackUp.png").convert_alpha()
        self.attackD=pygame.image.load("files/sprites/attackDown.png").convert_alpha()
        self.currentAStatus = self.attackU     
        
        self.currentSprite=self.idle
        self.numImages = 4
        self.imageDelay = 0
        self.screen=screen

        #input coordinates and usefull variables//
        self.rect=playerRect
        self.stillCheck = True

        self.h=128
        self.w=57

        self.aH=96
        self.aW=182

        self.aCImage = 0
        self.aNumImages = 15
        self.aImageDelay = 0
        self.aRectR = aRectR
        self.aRectL = aRectL
        self.aRectN = aRectN

        self.cooldown = False

        self.aRect = self.aRectN
        
        self.aDirection = self.attackL
        
    def update(self):
        global cImage, attack

        #FOR THE PLAYER SPRITE/////////////////////////////
        if moveLeft == False and moveRight == False and cImage >= 1 and self.stillCheck != True:
            cImage=0
            self.stillCheck = True
        
        if cImage==3: #reset the counter when walk
            self.imageDelay+=1
            if self.imageDelay >= FPS-52:
                self.imageDelay = 0 
                cImage = 0
                
        elif cImage>=self.numImages-1 and idleCheck: #idle reset
            self.imageDelay+=1
            if self.imageDelay >= FPS-52:
                #print("idle reset")
                self.imageDelay = 0 
                cImage = 0
        
        elif (cImage>=self.numImages-1) and self.idleCheck == False: #smooth transition from walk to idle
            cImage=3 
        
        else: #walk anim
            self.imageDelay+=1
            if self.imageDelay >= FPS-52:
                self.imageDelay = 0 
                cImage+=1
                
        #FOR THE ATTACK SPRITE///////////////////////////
        if self.cooldown == True:
            self.aImageDelay+=1
            self.currentAStatus = self.attackD
            if self.aImageDelay >= 99:
                self.cooldown = False
                self.aImageDelay = 0
        else:
            self.currentAStatus = self.attackU

        if attack:
            if self.cooldown == True:
                attack = False
                print("Attack in cd")
                         
            else:
                if self.aCImage >= self.aNumImages-1:
                    self.aCImage=0
                    attack = False
                    self.aRect = self.aRectN
                    self.cooldown = True #start timer
                
                else:
                    self.aImageDelay+=1
                    if self.aImageDelay >= FPS-58:
                        self.aImageDelay = 0 
                        self.aCImage+=1
                
            
            
    def movement(self):
            if moveLeft:
                self.currentSprite=self.walkL
                self.stillCheck = False
                #print("Left")
      
            elif moveRight:
                self.currentSprite=self.walkR
                self.stillCheck = False
                #print("Right")

            if attack:
                if self.cooldown == False:
                    if moveLeft:
                        self.aRect = self.aRectL
                        self.aDirection = self.attackL
                    elif moveRight:
                        self.aRect = self.aRectR
                        self.aDirection = self.attackR

    def render(self):
        global cImage
        
        if moveRight or moveLeft:
            idleCheck = False
            self.numImages = 4
            self.screen.blit(self.currentSprite,self.rect,(cImage*self.w,0,self.w,self.h))
        else:
            self.numImages = 2
            self.currentSprite=self.idle
            self.screen.blit(self.currentSprite,self.rect,(cImage*self.w,0,self.w,self.h))

        if attack:
            self.screen.blit(self.aDirection,self.aRect,(self.aCImage*self.aW,0,self.aW,self.aH))
            #pygame.draw.rect(screen,RED,self.aRect)

class Rocks:
    def __init__(self,playerRect,rockRect,screen,WINDOWWIDTH,WINDOWHEIGHT,playermove,rMin,rMax):
        pygame.init()
        self.rockSprite=pygame.image.load("files/sprites/rock.png").convert_alpha()
        self.numImages = 4
        self.cImage=0
        self.imageDelay = 0
        self.screen=screen
        self.WINDOWWIDTH =WINDOWWIDTH
        self.WINDOWHEIGHT= WINDOWHEIGHT
        self.restart = False

        #rock properties
        self.rocks=[]
        self.rockMinSize = 59
        self.rockMaxSize = 60
        self.rockMinSpeed = rMin
        self.rockMaxSpeed = rMax
        self.rockAddRate = 50
        self.rockAddCounter = 0
        
        #input coordinates
        self.rect=rockRect
        self.playerRect=playerRect

        self.playermove = playermove
        self.jumpspeedDown = -1
        self.jumpspeedUp = 25

        #single sprite size (width, height)
        self.h=74
        self.w=82

    def add_rocks(self):
            self.rockAddCounter+=1
            if self.rockAddCounter == self.rockAddRate:
                self.rockAddCounter = 0 #####pygame.Rect(random.randint(100, 200 - baddieSize)#####
                self.rockSize = random.randint(self.rockMinSize, self.rockMaxSize)
                self.newRock = {'rect': pygame.Rect(random.randint(0, self.WINDOWWIDTH - self.rockSize), 0 - self.rockSize, self.rockSize, self.rockSize),
                            'speed': random.randint(self.rockMinSpeed, self.rockMaxSpeed),
                            'surface':pygame.transform.scale(self.rockSprite, (self.rockSize, self.rockSize)),
                            }
                self.rocks.append(self.newRock)
                #print(self.rocks)

    def colision(self):
        self.restart = False
        for b in self.rocks:
            if self.playerRect.colliderect(b['rect']):
                print('rock colide')
                self.restart = True

    def move(self):
        global moveRight, moveLeft,jump
        # Move the rocks down.
        for b in self.rocks:
           if jump:
               b['rect'].move_ip(0,b['speed']+5) 
           else:
               b['rect'].move_ip(0,b['speed'])

        # Delete rocks that have fallen past the bottom.
        for b in self.rocks[:]:
            if b['rect'].top > self.WINDOWHEIGHT:
                self.rocks.remove(b)

        if moveLeft:
            for b in self.rocks:
                b['rect'].move_ip(self.playermove,0)
            
        elif moveRight:      
            for b in self.rocks:
                b['rect'].move_ip(-1*self.playermove,0)

        global fall
        if jump: 
            if fall:
                self.jumpspeedUp=0
            if self.jumpspeedUp <= 0: #downforce
                self.jumpspeedDown+=1
                for b in self.rocks:                    
                    b['rect'].move_ip(0,-1*self.jumpspeedDown)
                
            elif self.jumpspeedDown == -1: #upforce
                self.jumpspeedUp -= 1
                for b in self.rocks:  
                    b['rect'].move_ip(0,self.jumpspeedUp)
            #print('down_', self.jumpspeedDown,' up_',self.jumpspeedUp,'fall_',fall)
            
                
        else:
            self.jumpspeedUp = 25
            self.jumpspeedDown = -1
        
                
        
    def update(self):
        if self.cImage==3:
            self.imageDelay+=1
            if self.imageDelay >= FPS-48:
                self.imageDelay = 0 
                self.cImage = 0
        
        elif (self.cImage>=self.numImages-1) and self.idleCheck == False:
            self.cImage=3
        
        else:
            self.imageDelay+=1
            if self.imageDelay >= FPS-48:
                self.imageDelay = 0 
                self.cImage+=1

    def render(self):
        for b in self.rocks:
            self.screen.blit(self.rockSprite,b['rect'],(self.cImage*self.w,0,self.w,self.h))



class Platforms_And_Gold: #THE MAIN SCORE COUNT IS LOCATED HERE
    def __init__(self,playerRect,rockRect,screen,WINDOWWIDTH,WINDOWHEIGHT,playermove):
        global moveLeft,moveRight,idleCheck,jump,SCORE
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.platSprite=pygame.image.load("files/sprites/platform.png").convert_alpha()
        self.goldSprite=pygame.image.load("files/sprites/gold.png").convert_alpha()

        self.goldSound = pygame.mixer.Sound('files/sounds/gold.wav')
        
        self.screen=screen
        self.WINDOWWIDTH =WINDOWWIDTH
        self.WINDOWHEIGHT= WINDOWHEIGHT
        self.numImages = 6
        self.cImage=0
        self.imageDelay = 0

        #plat properties
        self.plats=[]
        self.newPlat = 0

        self.playermove = playermove
        self.jumpspeedUp = 25
        self.jumpspeedDown = -1
        self.collide = True

        #coin properties
        self.golds = []
        self.newGold =[]
        self.score = 0
        
        #input coordinates
        self.rockRect = rockRect
        self.playerRect = playerRect
        self.platRect = pygame.Rect(300, self.WINDOWHEIGHT - 300, 261, 23)
        self.grounded = True
        self.lastPlat = 1

        #single sprite size (width, height)
        self.platH=23
        self.platW=261

        self.goldH=44
        self.goldW=44
        

    def new_plats_coins(self):
            self.newPlat = pygame.Rect(random.randint(-440,880),self.WINDOWHEIGHT - 250, 440, 50)
            self.newGold = self.newPlat
            self.newGold = [self.newPlat[0]+200,self.newPlat[1]-80,43,43]
            self.plats.append(self.newPlat)
            self.gold=pygame.Rect(self.newGold)
            self.gold.bottom = self.newPlat.top
            self.groundPlats = [pygame.Rect(-440,WINDOWHEIGHT-40,440,30),pygame.Rect(0,WINDOWHEIGHT-40,440,30),pygame.Rect(440,WINDOWHEIGHT-40,440,30),pygame.Rect(880,WINDOWHEIGHT-40,440,30)]

            self.goldSpawn = 0
            self.newGoldSpawn = 0
            self.isFalling = True

    def movement_input(self,bounce):
        global jump,fall
        if jump:
            print
        
        elif moveLeft:
            #print("leftplat")
            for b in self.plats:
                b.move_ip(self.playermove,0)
            for b in self.groundPlats:
                b.move_ip(self.playermove,0)
            self.gold.move_ip(self.playermove,0)
            
        elif moveRight:
            #print("rightplat")   
            for b in self.plats:
                b.move_ip(-1*self.playermove,0)
            for b in self.groundPlats:
                b.move_ip(-1*self.playermove,0)
            self.gold.move_ip(-1*self.playermove,0)

        if jump: #JUMP////////////////
            if self.jumpspeedDown == -1: #upforce...
                self.jumpspeedUp -= 1
                if moveRight:
                    for b in self.plats:
                        b.move_ip(-1*self.playermove,self.jumpspeedUp)
                    for b in self.groundPlats:
                        b.move_ip(-1*self.playermove,self.jumpspeedUp)
                    self.gold.move_ip(-1*self.playermove,self.jumpspeedUp)
                elif moveLeft:
                    for b in self.plats:
                        b.move_ip(self.playermove,self.jumpspeedUp)
                    for b in self.groundPlats:
                        b.move_ip(self.playermove,self.jumpspeedUp)
                    self.gold.move_ip(self.playermove,self.jumpspeedUp)
                else:
                    for b in self.plats:
                        b.move_ip(0,self.jumpspeedUp)
                    for b in self.groundPlats:
                        b.move_ip(0,self.jumpspeedUp)
                    self.gold.move_ip(0,self.jumpspeedUp)
                    
                for b in self.plats:
                    if self.playerRect.colliderect(b):
                        if b.bottom <= self.playerRect.top:
                            self.jumpspeedUp=25
                #print(self.jumpspeedUp,self.jumpspeedDown,jump)
                            
            if self.jumpspeedUp <= 0: #downforce...
                fall = True#for monster
                #print(fall)
                self.jumpspeedDown -= 1
                if moveRight:
                    for b in self.plats:
                        b.move_ip(-1*self.playermove,self.jumpspeedDown)
                    for b in self.groundPlats:
                        b.move_ip(-1*self.playermove,self.jumpspeedDown)
                    self.gold.move_ip(-1*self.playermove,self.jumpspeedDown)
                elif moveLeft:
                    for b in self.plats:
                        b.move_ip(self.playermove,self.jumpspeedDown)
                    for b in self.groundPlats:
                        b.move_ip(self.playermove,self.jumpspeedDown)
                    self.gold.move_ip(self.playermove,self.jumpspeedDown)
                else:                  
                    for b in self.plats:
                        b.move_ip(0,self.jumpspeedDown)
                    for b in self.groundPlats:
                        b.move_ip(0,self.jumpspeedDown)
                    self.gold.move_ip(0,self.jumpspeedDown)
                
                #print(self.playerRect.bottom,self.playerRect.top)
                for b in self.plats:
                    if self.playerRect.colliderect(b):
                        if b.top <= self.playerRect.bottom:
                            self.jumpspeedDown = -300
                            for a in self.plats: #make it stand on platform, too fast and collidirect cant keep up
                                a.top = self.playerRect.bottom-2
                                for c in self.groundPlats:
                                    c.top = a.bottom + 185
                            self.gold.bottom = a.top
                            self.grounded = True
                            
                for b in self.groundPlats:
                    if self.playerRect.colliderect(b):
                        if b.top <= self.playerRect.bottom:
                            self.jumpspeedDown = -300
                            
                            for c in self.groundPlats:
                                c.top = self.playerRect.bottom-2
                                for a in self.plats: #make it stand on platform, too fast and collidirect cant keep up
                                    a.bottom = c.top - 185
                                    self.gold.bottom = a.top
                            self.grounded = True
                            
                        
            if self.jumpspeedDown <= -300:
                self.jumpspeedUp = 25
                self.jumpspeedDown = -1
                jump = False
                fall = False

        '''for b in self.plats:#falling
                if self.playerRect.colliderect(b):
                    if b.top <= self.playerRect.bottom:
                        b.move_ip(0,-7)
                        for b in self.groundPlats:
                            b.move_ip(0,-7)
                        self.gold.move_ip(0,-7)'''
    def falling(self,restart):
        global jump,HP
        self.restart = restart

        #define the last platform it stood on so it doesnt go to the void
        for d in self.groundPlats:
            if self.playerRect.colliderect(d):
                self.lastPlat = 0
        for e in self.plats:
            if self.playerRect.colliderect(e):
                self.lastPlat = 1
        
        if jump != True:
            for a in self.plats:
                if ((self.playerRect.left > a.right or self.playerRect.right < a.left) and self.lastPlat == 1):
                    self.jumpspeedUp = 0
                    self.jumpspeedDown = -2
                    jump = True
                    self.isFalling = True
                    #print("falltop")
                else:
                    self.isFalling = False
                    

            if ((self.playerRect.right < self.groundPlats[0].left or self.playerRect.left > self.groundPlats[len(self.groundPlats)-1].right) and self.lastPlat == 0):
                self.jumpspeedUp = 0
                self.jumpspeedDown = -2
                jump = True
                self.isFalling = True
                #print("fallbot")

            else:
                self.isFalling = False

                
        if self.groundPlats[0].bottom <= 0: #RESTART IF HIT
            self.restart = True
        else:
            self.restart = False
            
    
    def update(self):
        if self.cImage==5: #make last sprite last longer
            self.imageDelay+=1
            if self.imageDelay >= FPS-54:
                self.imageDelay = 0 
                self.cImage = 0
        
        elif self.cImage>=self.numImages-1:
            self.cImage=5
        
        else:
            self.imageDelay+=1
            if self.imageDelay >= FPS-54:
                self.imageDelay = 0 
                self.cImage+=1

    def render(self):
        for b in self.groundPlats:
            self.screen.blit(self.platSprite,b)
        #pygame.draw.rect(screen,RED,self.gold)
        
        for b in self.plats:
            self.screen.blit(self.platSprite,b)
        self.screen.blit(self.goldSprite,self.gold,(self.cImage*self.goldW,0,self.goldW,self.goldH))

    def new_gold(self):
        for b in self.plats:
            self.gold = [random.randint(self.groundPlats[0].left, self.groundPlats[len(self.groundPlats)-1].right),b[1]-80,43,43]
            self.gold=pygame.Rect(self.gold)
            self.gold.bottom = b.top

                
            
    def gold_pickup(self):
        global SCORE
        if self.playerRect.colliderect(self.gold):
            pygame.mixer.Sound.play(self.goldSound)
            self.score += 1
            self.new_gold()
            
        




class Bat:
    def __init__(self,playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,jumpspeedDown,jumpspeedUp,playermove,attackRect):
        global fall
        self.playerRect = playerRect
        self.flyL=pygame.image.load("files/sprites/flyL.png").convert_alpha()
        self.flyR=pygame.image.load("files/sprites/flyR.png").convert_alpha()
        self.screen=screen
        self.WINDOWWIDTH =WINDOWWIDTH
        self.WINDOWHEIGHT= WINDOWHEIGHT
        self.numImages = 8
        self.cImage=0
        self.imageDelay = 0
        self.currentSprite = self.flyL
        self.rect = pygame.Rect(random.randint(-400,WINDOWWIDTH+400), random.randint(-800,-400), 65, 65)
        self.speed = 2
        self.direction = 0
        self.jumpspeedUp = jumpspeedUp
        self.jumpspeedDown = jumpspeedDown
        self.playermove = playermove
        
        self.attackRect = attackRect
        self.canMove = True
        self.mvCd = 0

        self.down = False
        self.up = False
        self.left = False
        self.right = False

        self.spawnDelay = 0
        self.bounce = False

        #single sprite size (width, height)
        #self.h=126
        #self.w=129

        self.h=149
        self.w=153


    def follow(self,restart,attackRect):
        global fall, jump
        self.restart = restart
        self.attackRect = attackRect

        if self.rect.colliderect(self.attackRect):
            print('bat stationary')
            self.canMove = False

        if self.canMove == True:
            self.mvCd =0
            if jump:
                if fall:
                    self.jumpspeedUp=0
                if self.jumpspeedUp <= 0: #downforce
                    self.jumpspeedDown+=1
                    self.rect.move_ip(0,-1*self.jumpspeedDown)
                    
                elif self.jumpspeedDown == -1: #upforce
                    self.jumpspeedUp -= 1
                    self.rect.move_ip(0,self.jumpspeedUp)
                #print('down_', self.jumpspeedDown,' up_',self.jumpspeedUp,'fall_',fall)
 
            else:
                self.jumpspeedUp = 25
                self.jumpspeedDown = -1
                
            if moveLeft:
                self.rect.move_ip(self.playermove,0)
            if moveRight:
                self.rect.move_ip(-1*self.playermove,0)

            if self.rect.bottom <= playerRect.bottom:#follow down
                    self.rect.move_ip(0,self.speed)
                    self.direction = 3
                    self.down = True
            else:
                self.down = False
                    
            if self.rect.top >= playerRect.top:#follow up
                    self.rect.move_ip(0,-self.speed)
                    self.direction = 2
                    self.up = True
            else:
                self.up = False
            
            if self.rect.left <= playerRect.left:#follow left
                self.rect.move_ip(self.speed,0)
                self.currentSprite = self.flyR
                self.direction = 1
                self.left = True
            else:
                self.left = False
                
            if self.rect.right >= playerRect.right:#follow right
                self.currentSprite = self.flyL
                self.rect.move_ip(-self.speed,0)
                self.direction = 0
                self.right = True
            else:
                self.right = False
                
            if (self.right == True and (self.up == True or self.down == True)) or (self.left == True and (self.up == True or self.down == True)):
                self.speed = 2
            else:
                self.speed = 4
                
        else: #IF CANT MOVE
            self.mvCd +=1
            if self.mvCd >= 120:
                self.canMove = True
            if self.canMove == True:
                self.mvCd =0
                
            if jump:
                if fall:
                    self.jumpspeedUp=0
                if self.jumpspeedUp <= 0: #downforce
                    self.jumpspeedDown+=1
                    self.rect.move_ip(0,-1*self.jumpspeedDown)                     
                elif self.jumpspeedDown == -1: #upforce
                    self.jumpspeedUp -= 1
                    self.rect.move_ip(0,self.jumpspeedUp)
            else:
                self.jumpspeedUp = 25
                self.jumpspeedDown = -1

            if moveLeft:
                self.rect.move_ip(self.playermove,0)
            if moveRight:
                self.rect.move_ip(-1*self.playermove,0)
                    
        if self.playerRect.colliderect(self.rect):
            self.restart = True
            print('colide on bat')
        else:
            self.restart = False
            
    def update(self):
        if self.cImage==3:
            self.imageDelay+=1
            if self.imageDelay >= FPS-55:
                self.imageDelay = 0 
                self.cImage = 0
        
        elif self.cImage>=self.numImages-1:
            self.cImage=7
        
        else:
            self.imageDelay+=1
            if self.imageDelay >= FPS-55:
                self.imageDelay = 0 
                self.cImage+=1

                
    def render(self):
        # reminder: pygame.Rect(WINDOWWIDTH-400, WINDOWHEIGHT -950, 130, 100)
        
        #pygame.draw.rect(screen,RED,self.rect)
        self.screen.blit(self.currentSprite,(self.rect.x-30,self.rect.y-30),(self.cImage*self.w,0,self.w,self.h))
        


class Slime:
    def __init__(self,playerRect,screen,WINDOWWIDTH,WINDOWHEIGHT,jumpspeedDown,jumpspeedUp,groundPlat,groundPlat2,playermove,attackRect):
        global fall
        self.playerRect = playerRect
        self.hopL=pygame.image.load("files/sprites/hopL.png").convert_alpha()
        self.hopR=pygame.image.load("files/sprites/hopR.png").convert_alpha()
        self.screen=screen
        self.WINDOWWIDTH =WINDOWWIDTH
        self.WINDOWHEIGHT= WINDOWHEIGHT
        self.numImages = 8
        self.cImage=0
        self.imageDelay = 0
        self.currentSprite = self.hopR
        self.spawn = random.randint(0,1)
        if self.spawn == 0:
            self.spawn = -30
        else:
            self.spawn = WINDOWWIDTH + 30
        self.rect = pygame.Rect(self.spawn, WINDOWHEIGHT - 250, 45, 45)
        if self.rect.x <= (WINDOWHEIGHT/2)+50 and self.rect.x <= (WINDOWHEIGHT/2)-50:
            self.rect.x = random.randint(groundPlat.left,groundPlat2.right)
            
        self.speed = 4
        self.direction = 0
        self.jumpspeedUp = jumpspeedUp
        self.jumpspeedDown = jumpspeedDown
        self.playermove = playermove
        self.ground = groundPlat
        
        self.attackRect = attackRect
        self.canMove = True
        self.mvCd = 0

        self.down = False
        self.up = False
        self.left = False
        self.right = False

        self.spawnDelay = 0

        #single sprite size (width, height)
        #self.h=126
        #self.w=129

        self.h=97
        self.w=118


    def follow(self,restart,attackRect):
        global fall
        self.restart = restart
        self.attackRect = attackRect

        if self.rect.colliderect(self.attackRect):
            print('slime stationary')
            self.canMove = False
            
        if self.canMove == True:
            
            if self.rect.top >= playerRect.bottom:#follow up
                self.up = True

            else:   
                if self.rect.left <= playerRect.left:#follow left
                    self.rect.move_ip(self.speed,0)
                    self.currentSprite = self.hopR
                    self.direction = 1
                    self.left = True
                else:
                    self.left = False
                    
                if self.rect.right >= playerRect.right:#follow right
                    self.currentSprite = self.hopL
                    self.rect.move_ip(-self.speed,0)
                    self.direction = 0
                    self.right = True
                else:
                    self.right = False
                    
            if moveLeft:
                self.rect.move_ip(self.playermove,0)
            if moveRight:
                self.rect.move_ip(-1*self.playermove,0)
        else:
            self.mvCd +=1
            if self.mvCd >= 120:
                self.canMove = True
                self.mvCd =0
                
            if moveLeft:
                self.rect.move_ip(self.playermove,0)
            if moveRight:
                self.rect.move_ip(-1*self.playermove,0)
                    
        if self.playerRect.colliderect(self.rect):
            self.restart = True
            print('colide on slime')
        else:
            self.restart = False
        

    def update(self):
        self.rect.bottom = self.ground.top
        
        if self.cImage==3:
            self.imageDelay+=1
            if self.imageDelay >= FPS-53:
                self.imageDelay = 0 
                self.cImage = 0
        
        elif self.cImage>=self.numImages-1:
            self.cImage=7
        
        else:
            self.imageDelay+=1
            if self.imageDelay >= FPS-53:
                self.imageDelay = 0 
                self.cImage+=1

                
    def render(self):
        # reminder: pygame.Rect(WINDOWWIDTH-400, WINDOWHEIGHT -950, 130, 100)
        
        #pygame.draw.rect(screen,RED,self.rect)
        self.screen.blit(self.currentSprite,(self.rect.x-30,self.rect.y-30),(self.cImage*self.w,0,self.w,self.h))
        
            

class movement:
    def __init__(self):
        global moveLeft,moveRight,idleCheck
        pygame.mixer.pre_init(44100,-16,2,1024) 
        pygame.init()
        self.jumpSound = pygame.mixer.Sound('files/sounds/jump.wav')
        self.explosion = pygame.mixer.Sound('files/sounds/explosion.wav')
        #playerMove = 5

        
    def move_input(self,cooldown):
        global moveLeft,moveRight,idleCheck,attack,jump
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:#Player Presses a Key
                if event.key == K_LEFT or event.key == K_a and moveRight == False:
                    moveLeft = True
               
                if event.key == K_RIGHT or event.key == K_d and moveLeft == False:
                    moveRight = True

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F4:
                    pygame.quit()
                    sys.exit()
                    
                if attack == False:
                    if event.key == K_x:
                        if moveRight or moveLeft:
                            if cooldown != True:
                                pygame.mixer.Sound.play(self.explosion)
                            attack = True
                        
                if jump == False:
                    if event.key == K_SPACE or event.key == K_UP:
                        pygame.mixer.Sound.play(self.jumpSound)
                        jump = True
                    
            if event.type == KEYUP: #Player Releases a Key
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                elif event.key == K_RIGHT or event.key == K_d:
                    moveRight = False       



class Background: #PARALAX
    def __init__(self,screen):
        self.bgImage0 = pygame.image.load("files/sprites/bgImage0.png").convert_alpha()
        self.bgImage1 = pygame.image.load("files/sprites/bgImage1.png").convert_alpha()
        self.bgDecor0 = pygame.image.load("files/sprites/bgDecor0.png").convert_alpha()
        self.screen = screen

        self.bgImage0Rect = pygame.Surface.get_rect(self.bgImage0)
        self.bgImage1Rect = pygame.Surface.get_rect(self.bgImage1)

        self.bgDecor0Rect = pygame.Surface.get_rect(self.bgDecor0)


        self.numImages = 12
        self.cImage=0
        self.imageDelay = 0

        self.h = 434
        self.w = 625

    def update(self):
        global moveLeft,moveRight

        self.bgDecor0Rect.move_ip(-1,0)
        
        #PARALAX
        if moveLeft:
            self.bgImage0Rect.move_ip(2,0)
            self.bgImage1Rect.move_ip(1,0)
            self.bgDecor0Rect.move_ip(1,0)
        if moveRight:
            self.bgImage0Rect.move_ip(-2,0)
            self.bgImage1Rect.move_ip(-1,0)
            self.bgDecor0Rect.move_ip(-1,0)

        #DECORATION DRAGON
        if self.cImage==3:
            self.imageDelay+=1
        if self.imageDelay >= FPS-48:
            self.imageDelay = 0 
            self.cImage = 0
        
        elif self.cImage>=self.numImages-1:
            self.cImage=7
        
        else:
            self.imageDelay+=1
            if self.imageDelay >= FPS-48:
                self.imageDelay = 0 
                self.cImage+=1
            
        
    def render(self):
        self.screen.blit(self.bgImage1,(self.bgImage1Rect.x-300,self.bgImage1Rect.y))
        self.screen.blit(self.bgDecor0,(self.bgDecor0Rect.x+1200,self.bgDecor0Rect.y+350),(self.cImage*self.w,0,self.w,self.h))
        self.screen.blit(self.bgImage0,(self.bgImage0Rect.x-500,self.bgImage0Rect.y))
