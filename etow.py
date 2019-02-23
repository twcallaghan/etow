import sys
import os
import pygame
from pygame.locals import *

isRasPi=False

if os.uname()[1] == 'raspberrypi':
    print('Running on Raspberry Pi')
    isRasPi=True
else:
    print('Not running on Raspberry Pi')

p2IsBot=True
p2Speed=8

# preferred display modes
wantedDisplays=[(1920,1080),(1366,768)]

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screenWidth=0
screenHeight=0
screenBitDepth=8

pygame.init()

# can we get the mode we want
for testMode in wantedDisplays:
    if pygame.display.mode_ok(testMode,pygame.FULLSCREEN,screenBitDepth):
        print("can do {0}".format(testMode))
        screenWidth=testMode[0]
        screenHeight=testMode[1]
        break

if (screenWidth == 0):
    print("Display not capable of {0}, exiting".format(wantedDisplays))
    sys.exit(1)

playerPowerWidthCell=screenWidth/30
playerPowerHeightCell=screenHeight/30
screenWidthMiddle=screenWidth/2
screenHeightMiddle=screenHeight/2
knotWidthHeight=screenWidth/10
knotWidthHeightHalf=knotWidthHeight/2
knotMoveDistance=screenWidth/30
topBuffer=50
ropeThickness=knotWidthHeight/2
ropeThicknessHalf=ropeThickness/2

gameFontSize=50
#gameFont=pygame.font.Font('./digital_counter_7.ttf',gameFontSize)
gameFont=pygame.font.SysFont("monospace", gameFontSize)

screen = pygame.display.set_mode((screenWidth, screenHeight),pygame.FULLSCREEN,screenBitDepth)
pygame.display.set_caption('Hello World')
pygame.mouse.set_visible(1)

done = False
clock = pygame.time.Clock()
numTicks=0

numSeconds=0
p1Mode=0
p1CountAll=0
p1Count1s=0
p1Rounds=0
p2Mode=0
p2CountAll=0
p2Count1s=0
p2Rounds=0
p1Speeds={}
p2Speeds={}
for x in range(1,11):
    p1Speeds[x]=0
    p2Speeds[x]=0


tickSpeed=60

while not done:
    clock.tick(tickSpeed)
    numTicks+=1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            #sys.exit()

    key = pygame.key.get_pressed()

    if key[K_ESCAPE]:
        print('\nGame Shuting Down!')
        done=True

    if key[K_LEFT] and not key[K_RIGHT] and (p1Mode == 0):
        p1CountAll+=1
        p1Count1s+=1
        p1Mode=1
    elif not key[K_LEFT] and key[K_RIGHT] and (p1Mode == 1):
        p1CountAll+=1
        p1Count1s+=1
        p1Mode=0

    if (p2IsBot):
        p2Count1s=p2Speed
    elif key[K_z] and not key[K_x] and (p2Mode == 0):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=1
    elif not key[K_z] and key[K_x] and (p2Mode == 1):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=0

    if ((numTicks % tickSpeed) == 0):
        print("p1={0}  p2={1}".format(p1Count1s,p2Count1s))
        for x in range(10,1,-1):
            p1Speeds[x]=p1Speeds[x-1]
            p2Speeds[x]=p2Speeds[x-1]
        p1Speeds[1]=p1Count1s
        p2Speeds[1]=p2Count1s
        if (p1Count1s > p2Count1s):
            p1Rounds+=1
        elif (p2Count1s > p1Count1s):
            p2Rounds+=1
        p1Count1s=0
        p2Count1s=0

        if ((p1Rounds-p2Rounds) >= 10):
            print('\nPlayer 1 wins!')
            done=True
        elif ((p2Rounds-p1Rounds) >= 10):
            print('\nPlayer 2 wins!')
            done=True

        numSeconds+=1

    screen.fill(WHITE)

    text=gameFont.render(str(p2Rounds),True,BLUE)
    textRect=text.get_rect()
    textRect.centerx=screen.get_rect().centerx
    textRect.centery=screen.get_rect().centery
    screen.blit(text,textRect)
    #pygame.display.update()

    # player right power meter
    for y in range(1,11):
        for x in range(0,p1Speeds[y]):
            pygame.draw.rect(screen,RED,[screenWidthMiddle+10+((y-1)*playerPowerWidthCell),screenHeight-50-(x*playerPowerHeightCell),playerPowerWidthCell,playerPowerHeightCell])

    # player left power meter
    for y in range(1,11):
        for x in range(0,p2Speeds[y]):
            pygame.draw.rect(screen,BLUE,[screenWidthMiddle-10-((y)*playerPowerWidthCell),screenHeight-50-(x*playerPowerHeightCell),playerPowerWidthCell,playerPowerHeightCell])

    knot = p1Rounds - p2Rounds
    thisColor=BLACK
    if (p1Rounds > p2Rounds):
        thisColor=RED
    elif (p2Rounds > p1Rounds):
        thisColor=BLUE
    else:
        thisColor=BLACK
    pygame.draw.rect(screen,thisColor,[screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance),topBuffer,knotWidthHeight,knotWidthHeight])
    pygame.draw.rect(screen,RED,[screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance)+knotWidthHeight,topBuffer+knotWidthHeightHalf-ropeThicknessHalf,screenWidth,ropeThickness])
    pygame.draw.rect(screen,BLUE,[0,topBuffer+knotWidthHeightHalf-ropeThicknessHalf,screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance),ropeThickness])

    pygame.display.flip()

print("Total presses          | p1={0}  p2={1}".format(p1CountAll,p2CountAll))
print("Avg presses per second | p1={0}  p2={1}".format(p1CountAll/numSeconds,p2CountAll/numSeconds))

