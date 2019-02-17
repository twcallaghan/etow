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
        for x in range(1,10):
            p1Speeds[x]=p1Speeds[x+1]
            p2Speeds[x]=p2Speeds[x+1]
        p1Speeds[10]=p1Count1s
        p2Speeds[10]=p2Count1s
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

    for y in range(1,11):
        for x in range(0,p1Speeds[y]):
            pygame.draw.rect(screen,RED,[screenWidth-100-((10-y)*10),screenHeight-50-(x*10),10,10])

    for y in range(1,11):
        for x in range(0,p2Speeds[y]):
            pygame.draw.rect(screen,BLUE,[100+(y*10),screenHeight-50-(x*10),10,10])

    knot = p1Rounds - p2Rounds
    if (p1Rounds > p2Rounds):
        pygame.draw.rect(screen,RED,[(screenWidth/2)-25+(knot*25),50,50,50])
    elif (p2Rounds > p1Rounds):
        pygame.draw.rect(screen,BLUE,[(screenWidth/2)-25+(knot*25),50,50,50])
    else:
        pygame.draw.rect(screen,BLACK,[(screenWidth/2)-25+(knot*25),50,50,50])
    pygame.draw.rect(screen,RED,[(screenWidth/2)-25+(knot*25)+50,70,1000,10])
    pygame.draw.rect(screen,BLUE,[0,70,(screenWidth/2)-25+(knot*25),10])

    pygame.display.flip()

print("Total presses          | p1={0}  p2={1}".format(p1CountAll,p2CountAll))
print("Avg presses per second | p1={0}  p2={1}".format(p1CountAll/numSeconds,p2CountAll/numSeconds))

