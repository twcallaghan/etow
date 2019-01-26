import os
import pygame
from pygame.locals import *

isRasPi=False

if os.uname()[1] == 'raspberrypi':
    print('Running on Raspberry Pi')
    isRasPi=True
else:
    print('Not running on Raspberry Pi')


# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screenWidth=640
screenHeight=480

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hello World')
pygame.mouse.set_visible(1)

done = False
clock = pygame.time.Clock()
numTicks=0

p1Mode=0
p1CountAll=0
p1Count1s=0
p1AvgRate=0
p1Rounds=0

p2Mode=0
p2CountAll=0
p2Count1s=0
p2AvgRate=0
p2Rounds=0

tickSpeed=30

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

    if key[K_z] and not key[K_x] and (p2Mode == 0):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=1
    elif not key[K_z] and key[K_x] and (p2Mode == 1):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=0

    if ((numTicks % tickSpeed) == 0):
        #p1AvgRate=float(p1CountAll)/float(numTicks)*float(tickSpeed)
        #p2AvgRate=float(p2CountAll)/float(numTicks)*float(tickSpeed)
        p1AvgRate=float(p1Count1s)
        p2AvgRate=float(p2Count1s)
        print("p1={0:.2f}  p2={1:.2f}".format(p1AvgRate,p2AvgRate))
        p1Count1s=0
        p2Count1s=0
        if (p1AvgRate > p2AvgRate):
            p1Rounds+=1
        elif (p2AvgRate > p1AvgRate):
            p2Rounds+=1

        if (p1Rounds >= 10):
            print('\nPlayer 1 wins!')
            done=True
        elif (p2Rounds >= 10):
            print('\nPlayer 2 wins!')
            done=True

    screen.fill(WHITE)

    p1Rate=int(round(p1AvgRate))
    for x in range(0,p1Rate):
        pygame.draw.rect(screen,BLACK,[screenWidth-100,screenHeight-50-(x*25),25,25])

    p2Rate=int(round(p2AvgRate))
    for x in range(0,p2Rate):
        pygame.draw.rect(screen,BLACK,[100,screenHeight-50-(x*25),25,25])

    for x in range(0,p1Rounds):
        pygame.draw.rect(screen,BLACK,[screenWidth/2+(x*25),50,25,25])

    for x in range(0,p2Rounds):
        pygame.draw.rect(screen,BLACK,[screenWidth/2-25-(x*25),50,25,25])

    pygame.display.flip()
