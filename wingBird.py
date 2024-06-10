import random
import sys
import pygame
from pygame.locals import *


FPS = 60
SCREENWIDTH = 1280
SCREENHIGHT = 720
PLAYERHEIGHT = 100
PLAYERWIDTH = 100
BASEHEIGHT = 100
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
GROUNDY = SCREENHIGHT*0.86
GAME_SPRITES ={}
GAME_SOUNDS = {}
PLAYER = ["characters/blue_bird.png","characters/yellow_hat.png","characters/brown_bird.png","characters/blue_helmet.png","characters/white_bird.png","characters/yellow_quack.png"]
BACKGROUND ="images/bg.jpg"
PIPE ="images/pipe.png"


def welcome():
    playerx = int(SCREENWIDTH/6)
    playery = int((SCREENHIGHT - PLAYERHEIGHT)/2)
    basex =0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key ==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(pygame.transform.scale(GAME_SPRITES['player'],(PLAYERWIDTH,PLAYERHEIGHT)),(playerx,playery))#pygame.transform.scale(GAME_SPRITES['player'],(PLAYERWIDTH,PLAYERHEIGHT))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'],(-30,0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    playerx =int(SCREENWIDTH/6)
    playery =int((SCREENHIGHT - PLAYERHEIGHT)/2)
    basex = 0
    pipe1= randomPipe()
    pipe2 = randomPipe()
    pipe3 = randomPipe()
    upperPipes =[
        {'x':SCREENWIDTH+150,'y':pipe1[0]['y']},
        {'x':SCREENWIDTH+150+(SCREENWIDTH/2),'y':pipe2[0]['y']}
    ]
    lowerPipes =[
        {'x':SCREENWIDTH+150,'y':pipe1[1]['y']},
        {'x':SCREENWIDTH+150+(SCREENWIDTH/2),'y':pipe2[1]['y']}
    ]

    pipeVelocityX=-6

    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY = 1
    playerFlappy = -9 #speed of bird when we press arrow key
    playerFlapped = False #when space is pressed becomes true
    SCORE=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or (event.key==K_SPACE or event.key == K_UP):
                if playery>0:
                    playerVelY=playerFlappy
                    playerFlapped= True
                    GAME_SOUNDS['wing'].play()
        crashTest = collision(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            SCREEN.blit(GAME_SPRITES['gameover'],(0,0))
            pygame.display.update()
            return SCORE
        playerMidPosition = playerx+PLAYERWIDTH/2
        for pipe in upperPipes:
            pipeMidPosition = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPosition<= playerMidPosition<pipeMidPosition+8:
                SCORE+=1
                print("Score:",SCORE)
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY+= playerAccY

        if playerFlapped:
            playerFlapped = False

        playery = playery + min(playerVelY, GROUNDY-playery-PLAYERHEIGHT)


        #motion of pipes
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelocityX
            lowerPipe['x']+=pipeVelocityX

        if 0<upperPipes[0]['x']<8:
            newpipe = randomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
   
        #deeting pipes 
        if upperPipes[0]['x']<= -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(pygame.transform.scale(GAME_SPRITES['player'],(PLAYERWIDTH,PLAYERHEIGHT)),(playerx,playery))
        
        digits = [int(x) for x in list(str(SCORE))]
        width = 0
        for digit in digits:
            width += 50 #GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = 30

        for digit in digits:
            SCREEN.blit(pygame.transform.scale(GAME_SPRITES['numbers'][digit],(50,50)),(Xoffset,SCREENHIGHT*0.05))
            Xoffset += 50
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

def collision(playerx,playery,upperPipes,lowerPipes):
    if playery+PLAYERHEIGHT >= GROUNDY or playery<=0:
        GAME_SOUNDS['hit'].play()
        print("1err")
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery+25 < pipeHeight + pipe['y'] and pipe['x']<=playerx+PLAYERWIDTH <= pipe['x']+GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            print("2err",playerx - pipe['x']+PLAYERWIDTH)
            return True

    for pipe in lowerPipes:
        if (playery + PLAYERHEIGHT-25 > pipe['y']) and pipe['x']<=playerx+PLAYERWIDTH <= pipe['x']+ GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            print("3err")
            return True

    return False
    
 


def randomPipe():
    height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHIGHT/3.6
    y2 = offset + random.randrange(0,int(SCREENHIGHT-BASEHEIGHT-(1.2*offset)))
    x = SCREENWIDTH+10
    y1 = height -y2 +offset
    pipe = [
        {'x':x,'y':-y1},{'x':x,'y':y2}
    ]
    return pipe


def exit(score):
    playerx = int(SCREENWIDTH/6)
    playery = int((SCREENHIGHT - PLAYERHEIGHT)/2)
    basex =0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key ==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(pygame.transform.scale(GAME_SPRITES['player'],(PLAYERWIDTH,PLAYERHEIGHT)),(playerx,playery))#pygame.transform.scale(GAME_SPRITES['player'],(PLAYERWIDTH,PLAYERHEIGHT))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['gameover'],(0,0))
                digits = [int(x) for x in list(str(score))]
                width = 0
                for digit in digits:
                    width += 100 #GAME_SPRITES['numbers'][digit].get_width()
                Xoffset = (SCREENWIDTH-100)/2

                for digit in digits:
                    SCREEN.blit(pygame.transform.scale(GAME_SPRITES['numbers'][digit],(100,100)),(Xoffset,SCREENHIGHT*0.05))
                    Xoffset += 100
                pygame.display.update()
                FPSCLOCK.tick(FPS)





if __name__=="__main__":
    #starting the game (initializing)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("WingBird by Ayushman Tomar")
    GAME_SPRITES['numbers']=(pygame.image.load('images/0.png').convert_alpha(),
                             pygame.image.load('images/1.png').convert_alpha(),
                             pygame.image.load('images/2.png').convert_alpha(),
                             pygame.image.load('images/3.png').convert_alpha(),
                             pygame.image.load('images/4.png').convert_alpha(),
                             pygame.image.load('images/5.png').convert_alpha(),
                             pygame.image.load('images/6.png').convert_alpha(),
                             pygame.image.load('images/7.png').convert_alpha(),
                             pygame.image.load('images/8.png').convert_alpha(),
                             pygame.image.load('images/9.png').convert_alpha(),
    )
    GAME_SPRITES['message']= pygame.image.load('images/message.png').convert_alpha()
    GAME_SPRITES['base']= pygame.image.load('images/base.jpg').convert_alpha()
    GAME_SPRITES['gameover']=pygame.image.load('images/game_over.png')
    GAME_SPRITES['pipe']= (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha(),
    )
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER[random.randint(0,5)]).convert_alpha()
    
    GAME_SOUNDS['die'] = pygame.mixer.Sound('sounds/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('sounds/wing.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('sounds/point.wav')
    while True:
        welcome()
        score = mainGame()
        print(score)
        exit(score)


