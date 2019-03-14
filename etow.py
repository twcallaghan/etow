import sys
import os
import time
import pygame
from pygame.locals import *

isRasPi=False
p2IsBot=True
p2Speed=8
roundsToWin=10

lbTaps='./lbtaps.txt'
lbAvg='./lbavg.txt'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screenWidth=0
screenHeight=0
screenBitDepth=8

#gameFont='./assets/digital_counter_7.ttf'
gameFont='freesansbold.ttf'
gameFont050=None
gameFont075=None
gameFont100=None
gameFont250=None
gameFont500=None

allDone=False

p1CountAll=0
p1Count1s=0
p1Mode=0
p2CountAll=0
p2Count1s=0
p2Mode=0

p1b1=False
p1b2=False
p2b1=False
p2b2=False

clock=None

tickSpeed=30


def clear_buttons():
    global p1b1
    global p1b2
    global p2b1
    global p2b2
    p1b1=False
    p1b2=False
    p2b1=False
    p2b2=False


def screen_title():
    global allDone
    done=False
    colorValue=0
    clear_buttons()
    while not done and not allDone:
        clock.tick(tickSpeed)
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                done=True
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_F8)):
                done=True
                allDone=True

        if (p1b1 or p1b2 or p2b1 or p2b2):
            done=True

        text=gameFont100.render('Electronic',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,150))
        screen.blit(text,thisTextRect)
        text=gameFont100.render('Tug',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,350))
        screen.blit(text,thisTextRect)
        text=gameFont100.render('Of',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,550))
        screen.blit(text,thisTextRect)
        text=gameFont100.render('War',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,750))
        screen.blit(text,thisTextRect)
        text=gameFont050.render('Hit Any Button',False,(colorValue,colorValue,colorValue))
        thisTextRect=text.get_rect(center=(screenWidthMiddle,950))
        screen.blit(text,thisTextRect)

        colorValue += 16
        if (colorValue > 255):
            colorValue=0

        pygame.display.flip()

    pygame.event.pump()


def screen_rules():
    global allDone
    numSeconds=10
    clear_buttons()

    # instructions
    done=False
    colorValue=0
    while not done and not allDone:
        clock.tick(tickSpeed)
        screen.fill(WHITE)
        text=gameFont100.render('Press alternating buttons quickly.',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,250))
        screen.blit(text,thisTextRect)
        text=gameFont100.render('Defeat your opponent.',False,BLACK)
        thisTextRect=text.get_rect(center=(screenWidthMiddle,450))
        screen.blit(text,thisTextRect)
        text=gameFont050.render('Press all 4 buttons to continue.',False,(colorValue,colorValue,colorValue))
        thisTextRect=text.get_rect(center=(screenWidthMiddle,850))
        screen.blit(text,thisTextRect)

        if (p1b1):
            text=gameFont050.render('4',False,RED)
            thisTextRect=text.get_rect(center=(screenWidthMiddle+600,950))
            screen.blit(text,thisTextRect)

        if (p1b2):
            text=gameFont050.render('3',False,RED)
            thisTextRect=text.get_rect(center=(screenWidthMiddle+400,950))
            screen.blit(text,thisTextRect)

        if (p2b1):
            text=gameFont050.render('2',False,BLUE)
            thisTextRect=text.get_rect(center=(screenWidthMiddle-400,950))
            screen.blit(text,thisTextRect)

        if (p2b2):
            text=gameFont050.render('1',False,BLUE)
            thisTextRect=text.get_rect(center=(screenWidthMiddle-600,950))
            screen.blit(text,thisTextRect)


        colorValue += 16
        if (colorValue > 255):
            colorValue=0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                done=True
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_F8)):
                done=True
                allDone=True

        if (p1b1 and p1b2 and p2b1 and p2b2):
            done=True

    # countdown
    done=False
    numTicks=0
    while not done and not allDone:
        clock.tick(tickSpeed)
        numTicks += 1
        if ((numTicks % tickSpeed) == 0):
            numSeconds -= 1
            screen.fill(WHITE)
            text=gameFont100.render('Game starts in...',False,BLACK)
            thisTextRect=text.get_rect(center=(screenWidthMiddle,350))
            screen.blit(text,thisTextRect)
            text=gameFont500.render(str(numSeconds),False,BLACK)
            thisTextRect=text.get_rect(center=(screenWidthMiddle,650))
            screen.blit(text,thisTextRect)
            pygame.display.flip()
        if (numSeconds == 0):
            done=True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                done=True
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_F8)):
                done=True
                allDone=True

    pygame.event.pump()


def screen_game():
    global p1Mode
    global p1CountAll
    global p1Count1s
    global p2Mode
    global p2CountAll
    global p2Count1s
    global allDone

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
    p1FinalRounds=0
    p1FinalTaps=0
    p2FinalRounds=0
    p2FinalTaps=0
    p1FinalAvg=0
    p2FinalAvg=0
    lastRoundMargin=0
    lastRoundVictor='unknown'
    advantageColor=0
    advantageIncrement=int(255/tickSpeed)

    p1Speeds={}
    p2Speeds={}
    for x in range(1,11):
        p1Speeds[x]=0
        p2Speeds[x]=0

    winner=''
    done=False
    while not done and not allDone:
        clock.tick(tickSpeed)
        numTicks+=1

        if (p2IsBot):
            p2Count1s=p2Speed

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                done=True
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_F8)):
                done=True
                allDone=True

            if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT) and (p1Mode == 0)):
                p1CountAll+=1
                p1Count1s+=1
                p1Mode=1
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT) and (p1Mode == 1)):
                p1CountAll+=1
                p1Count1s+=1
                p1Mode=0

            if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_z) and (p2Mode == 0)):
                p2CountAll+=1
                p2Count1s+=1
                p2Mode=1
            elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_x) and (p2Mode == 1)):
                p2CountAll+=1
                p2Count1s+=1
                p2Mode=0

        if ((numTicks % tickSpeed) == 0):
            advantageColor=255
            #print("p1={0}  p2={1}".format(p1Count1s,p2Count1s))
            for x in range(10,1,-1):
                p1Speeds[x]=p1Speeds[x-1]
                p2Speeds[x]=p2Speeds[x-1]
            p1Speeds[1]=p1Count1s
            p2Speeds[1]=p2Count1s
            if (p2IsBot):
                p2CountAll+=p2Speed
            if (p1Count1s > p2Count1s):
                p1Rounds+=1
                lastRoundMargin=p1Count1s-p2Count1s
                lastRoundVictor='right'
                #if not ((p1Rounds-p2Rounds) >= roundsToWin):
                #    player1Sound.play()
            elif (p2Count1s > p1Count1s):
                p2Rounds+=1
                lastRoundMargin=p2Count1s-p1Count1s
                lastRoundVictor='left'
                #if not ((p2Rounds-p1Rounds) >= roundsToWin):
                #    player2Sound.play()
            else:
                lastRoundMargin=0
                lastRoundVictor='unknown'
            p1Count1s=0
            p2Count1s=0

            if ((p1Rounds-p2Rounds) >= roundsToWin):
                #victorySound.play()
                done=True
                winner='Red'
            elif ((p2Rounds-p1Rounds) >= roundsToWin):
                #victorySound.play()
                done=True
                winner='Blue'

            if (winner != ''):
                # capture final statistics
                p1FinalRounds=p1Rounds
                p1FinalTaps=p1CountAll
                p2FinalRounds=p2Rounds
                p2FinalTaps=p2CountAll
                thisSeconds=numSeconds
                if (thisSeconds==0):
                    thisSeconds=1
                p1FinalAvg=p1CountAll/thisSeconds
                p2FinalAvg=p2CountAll/thisSeconds

            numSeconds+=1

        screen.fill(WHITE)

        if (lastRoundVictor=='left'):
            advantageColor -= advantageIncrement
            pygame.draw.rect(screen,(advantageColor,advantageColor,255),[50,300,screenWidthMiddle-50-50,100])
            text=gameFont075.render('+'+str(lastRoundMargin)+' advantage',False,WHITE)
            thisTextRect=text.get_rect(center=(screenWidthMiddle/2,350))
            screen.blit(text,thisTextRect)
        elif (lastRoundVictor=='right'):
            advantageColor -= advantageIncrement
            pygame.draw.rect(screen,(255,advantageColor,advantageColor),[screenWidthMiddle+50,300,screenWidthMiddle-50-50,100])
            text=gameFont075.render('+'+str(lastRoundMargin)+' advantage',False,WHITE)
            thisTextRect=text.get_rect(center=(screenWidth-(screenWidthMiddle/2),350))
            screen.blit(text,thisTextRect)

        # right player rounds
        text=gameFont050.render('Rnds',False,BLACK)
        screen.blit(text,(screenWidth-300,screenHeight-300))
        text=gameFont050.render(str(p1Rounds),False,BLACK)
        screen.blit(text,(screenWidth-150,screenHeight-300))
        # right player taps
        text=gameFont050.render('Taps',False,BLACK)
        screen.blit(text,(screenWidth-300,screenHeight-200))
        text=gameFont050.render(str(p1CountAll),False,BLACK)
        screen.blit(text,(screenWidth-150,screenHeight-200))
        # right player avg
        text=gameFont050.render('Avg',False,BLACK)
        screen.blit(text,(screenWidth-300,screenHeight-100))
        thisSeconds=numSeconds
        if (thisSeconds==0):
            thisSeconds=1
        text=gameFont050.render("{0:0.2f}".format(p1CountAll/thisSeconds),False,BLACK)
        screen.blit(text,(screenWidth-150,screenHeight-100))
        # left player rounds
        text=gameFont050.render('Rnds',False,BLACK)
        screen.blit(text,(50,screenHeight-300))
        text=gameFont050.render(str(p2Rounds),False,BLACK)
        screen.blit(text,(200,screenHeight-300))
        # left player taps
        text=gameFont050.render('Taps',False,BLACK)
        screen.blit(text,(50,screenHeight-200))
        text=gameFont050.render(str(p2CountAll),False,BLACK)
        screen.blit(text,(200,screenHeight-200))
        # left player avg
        text=gameFont050.render('Avg',False,BLACK)
        screen.blit(text,(50,screenHeight-100))
        thisSeconds=numSeconds
        if (thisSeconds==0):
            thisSeconds=1
        text=gameFont050.render("{0:0.2f}".format(p2CountAll/thisSeconds),False,BLACK)
        screen.blit(text,(200,screenHeight-100))

        # player right power meter
        for y in range(1,11):
            for x in range(0,p1Speeds[y]):
                pygame.draw.rect(screen,RED,[screenWidthMiddle+10+((y-1)*playerPowerWidthCell)+playerPowerCellBuffer,screenHeight-50-(x*playerPowerHeightCell)+playerPowerCellBuffer,playerPowerWidthCell-playerPowerCellBuffer,playerPowerHeightCell-playerPowerCellBuffer])

        # player left power meter
        for y in range(1,11):
            for x in range(0,p2Speeds[y]):
                pygame.draw.rect(screen,BLUE,[screenWidthMiddle-10-((y)*playerPowerWidthCell)+playerPowerCellBuffer,screenHeight-50-(x*playerPowerHeightCell)+playerPowerCellBuffer,playerPowerWidthCell-playerPowerCellBuffer,playerPowerHeightCell-playerPowerCellBuffer])

        knot = p1Rounds - p2Rounds
        thisColor=BLACK
        if (p1Rounds > p2Rounds):
            thisColor=RED
        elif (p2Rounds > p1Rounds):
            thisColor=BLUE
        else:
            thisColor=BLACK
        # knot
        pygame.draw.rect(screen,thisColor,[screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance),topBuffer,knotWidthHeight,knotWidthHeight])
        # right rope
        pygame.draw.rect(screen,RED,[screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance)+knotWidthHeight,topBuffer+knotWidthHeightHalf-ropeThicknessHalf,screenWidth,ropeThickness])
        # left rope
        pygame.draw.rect(screen,BLUE,[0,topBuffer+knotWidthHeightHalf-ropeThicknessHalf,screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance),ropeThickness])
        # left victory
        text=gameFont050.render('win',False,BLACK)
        thisTextRect=text.get_rect(center=(250,25))
        screen.blit(text,thisTextRect)
        # right victory
        text=gameFont050.render('win',False,BLACK)
        thisTextRect=text.get_rect(center=(1675,25))
        screen.blit(text,thisTextRect)

        # rounds until victory
        if (winner == ''):
            text=gameFont100.render(str(roundsToWin-abs(p1Rounds-p2Rounds)),False,BLACK)
            thisTextRect=text.get_rect(center=(screenWidthMiddle-knotWidthHeightHalf+(knot*knotMoveDistance)+(knotWidthHeight/2),topBuffer+(knotWidthHeight/2)))
            screen.blit(text,thisTextRect)

        pygame.display.flip()

    if not (winner == ''):
        clear_buttons()
        done=False
        numTicks=0

        p1FinalRounds=p1Rounds
        p1FinalTaps=p1CountAll
        p2FinalRounds=p2Rounds
        p2FinalTaps=p2CountAll
        thisSeconds=numSeconds
        if (thisSeconds==0):
            thisSeconds=1
        p1FinalAvg=p1CountAll/thisSeconds
        p2FinalAvg=p2CountAll/thisSeconds

        listTaps=[]
        listAvg=[]
        lbTaps='./lbtaps.txt'
        lbAvg='./lbavg.txt'
        with open(lbTaps) as f:
            tempTaps=f.read().splitlines()
        for thisTaps in tempTaps:
            listTaps.append(int(thisTaps))
        with open(lbTaps) as f:
            tempAvg=f.read().splitlines()
        for thisAvg in tempAvg:
            listAvg.append(float(thisAvg))
        listTaps.append(int(p1FinalTaps))
        listTaps.append(int(p2FinalTaps))
        listAvg.append(float(p1FinalAvg))
        listAvg.append(float(p2FinalAvg))
        listTaps=sorted(listTaps,reverse=True)
        listAvg=sorted(listAvg,reverse=True)

        with open(lbTaps,'w') as f:
            for item in listTaps:
                f.write("{0}\n".format(item))

        with open(lbAvg,'w') as f:
            for item in listAvg:
                f.write("{0:0.2f}\n".format(item))

        p1TapsLB=1
        p2TapsLB=1
        p1AvgLB=1
        p2AvgLB=1

        thisPosition=1
        for thisTaps in listTaps:
            if p1FinalTaps >= thisTaps:
                p1TapsLB=thisPosition
                break
            thisPosition += 1

        thisPosition=1
        for thisTaps in listTaps:
            if p2FinalTaps >= thisTaps:
                p2TapsLB=thisPosition
                break
            thisPosition += 1

        thisPosition=1
        for thisAvg in listAvg:
            if p1FinalAvg >= thisAvg:
                p1AvgLB=thisPosition
                break
            thisPosition += 1

        thisPosition=1
        for thisAvg in listAvg:
            if p2FinalAvg >= thisAvg:
                p2AvgLB=thisPosition
                break
            thisPosition += 1

        TapsLBSize=len(listTaps)
        AvgLBSize=len(listAvg)

        while not done and not allDone:
            clock.tick(tickSpeed)
            numTicks+=1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    done=True
                elif ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_F8)):
                    done=True
                    allDone=True

            if (p1b1 and p1b2 and p2b1 and p2b2):
                done=True

            screen.fill(WHITE)

            if (winner=='Blue'):
                pygame.draw.rect(screen,BLUE,[50,100,screenWidthMiddle-50-50,600])
                text=gameFont100.render('winner',False,WHITE)
                thisTextRect=text.get_rect(center=(screenWidthMiddle/2,400))
                screen.blit(text,thisTextRect)
            elif (winner=='Red'):
                pygame.draw.rect(screen,RED,[screenWidthMiddle+50,100,screenWidthMiddle-50-50,600])
                text=gameFont100.render('winner',False,WHITE)
                thisTextRect=text.get_rect(center=(screenWidth-(screenWidthMiddle/2),400))
                screen.blit(text,thisTextRect)

            # right player rounds
            text=gameFont050.render('Rnds',False,BLACK)
            screen.blit(text,(screenWidth-300,screenHeight-300))
            text=gameFont050.render(str(p1FinalRounds),False,BLACK)
            screen.blit(text,(screenWidth-150,screenHeight-300))
            # right player taps
            text=gameFont050.render('Taps',False,BLACK)
            screen.blit(text,(screenWidth-300,screenHeight-200))
            text=gameFont050.render(str(p1FinalTaps),False,BLACK)
            screen.blit(text,(screenWidth-150,screenHeight-200))
            # right player taps rank
            #text=gameFont050.render('Taps',False,BLACK)
            #screen.blit(text,(screenWidth-300,screenHeight-200))
            text=gameFont050.render(str(p1TapsLB)+' of '+str(TapsLBSize),False,BLACK)
            screen.blit(text,(screenWidth-550,screenHeight-200))
            # right player avg
            text=gameFont050.render('Avg',False,BLACK)
            screen.blit(text,(screenWidth-300,screenHeight-100))
            text=gameFont050.render("{0:0.2f}".format(p1FinalAvg),False,BLACK)
            screen.blit(text,(screenWidth-150,screenHeight-100))
            # right player avg rank
            #text=gameFont050.render('Avg',False,BLACK)
            #screen.blit(text,(screenWidth-300,screenHeight-100))
            text=gameFont050.render(str(p1AvgLB)+' of '+str(AvgLBSize),False,BLACK)
            screen.blit(text,(screenWidth-550,screenHeight-100))
            # left player rounds
            text=gameFont050.render('Rnds',False,BLACK)
            screen.blit(text,(50,screenHeight-300))
            text=gameFont050.render(str(p2FinalRounds),False,BLACK)
            screen.blit(text,(200,screenHeight-300))
            # left player taps
            text=gameFont050.render('Taps',False,BLACK)
            screen.blit(text,(50,screenHeight-200))
            text=gameFont050.render(str(p2FinalTaps),False,BLACK)
            screen.blit(text,(200,screenHeight-200))
            # left player taps rank
            #text=gameFont050.render('Taps',False,BLACK)
            #screen.blit(text,(50,screenHeight-200))
            text=gameFont050.render(str(p2TapsLB)+' of '+str(TapsLBSize),False,BLACK)
            screen.blit(text,(400,screenHeight-200))
            # left player avg
            text=gameFont050.render('Avg',False,BLACK)
            screen.blit(text,(50,screenHeight-100))
            text=gameFont050.render("{0:0.2f}".format(p2FinalAvg),False,BLACK)
            screen.blit(text,(200,screenHeight-100))
            # left player avg rank
            #text=gameFont050.render('Avg',False,BLACK)
            #screen.blit(text,(50,screenHeight-100))
            text=gameFont050.render(str(p2AvgLB)+' of '+str(AvgLBSize),False,BLACK)
            screen.blit(text,(400,screenHeight-100))

            pygame.display.flip()


def button_callback1(channel):
    global p1CountAll
    global p1Count1s
    global p1Mode
    global p1b1
    p1b1=True
    if (p1Mode == 0):
        p1CountAll+=1
        p1Count1s+=1
        p1Mode=1

def button_callback2(channel):
    global p1CountAll
    global p1Count1s
    global p1Mode
    global p1b2
    p1b2=True
    if (p1Mode == 1):
        p1CountAll+=1
        p1Count1s+=1
        p1Mode=0

def button_callback3(channel):
    global p2CountAll
    global p2Count1s
    global p2Mode
    global p2b1
    p2b1=True
    if (p2Mode == 0):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=1

def button_callback4(channel):
    global p2CountAll
    global p2Count1s
    global p2Mode
    global p2b2
    p2b2=True
    if (p2Mode == 1):
        p2CountAll+=1
        p2Count1s+=1
        p2Mode=0

def main():
    global screenWidth
    global screenHeight
    global playerPowerWidthCell
    global playerPowerHeightCell
    global playerPowerCellBuffer
    global screenWidthMiddle
    global screenHeightMiddle
    global knotWidthHeight
    global knotWidthHeightHalf
    global knotMoveDistance
    global topBuffer
    global ropeThickness
    global ropeThicknessHalf
    global screen
    global gameFont050
    global gameFont075
    global gameFont100
    global gameFont250
    global gameFont500
    global clock
    global isRasPi

    #pygame.mixer.pre_init(22050, -16, 1, 256)
    #pygame.mixer.init()
    pygame.init()

    # preload sound fx
    #victorySound = pygame.mixer.Sound('./assets/winner.wav')
    #player1Sound = pygame.mixer.Sound('./assets/player1.wav')
    #player2Sound = pygame.mixer.Sound('./assets/player2.wav')

    if os.uname()[1] == 'raspberrypi':
        print('Running on Raspberry Pi')
        isRasPi=True
        import RPi.GPIO as GPIO
        # ignore warnings
        GPIO.setwarnings(False)
        # use physical pin numbering
        GPIO.setmode(GPIO.BOARD)
        # set pin 0 to be an input in and set the initial value to be pulled low (off)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Setup event on pin rising edges
        GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback1,bouncetime=100)
        GPIO.add_event_detect(12,GPIO.RISING,callback=button_callback2,bouncetime=100)
        GPIO.add_event_detect(16,GPIO.RISING,callback=button_callback3,bouncetime=100)
        GPIO.add_event_detect(18,GPIO.RISING,callback=button_callback4,bouncetime=100)
    else:
        print('Not running on Raspberry Pi')

    # preferred display modes
    wantedDisplays=[(1920,1080),(1366,768)]

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

    playerPowerWidthCell=int(screenWidth/35)
    playerPowerHeightCell=int(screenHeight/60)
    playerPowerCellBuffer=2
    screenWidthMiddle=int(screenWidth/2)
    screenHeightMiddle=int(screenHeight/2)
    knotWidthHeight=int(screenWidth/10)
    knotWidthHeightHalf=int(knotWidthHeight/2)
    knotMoveDistance=int(screenWidth/((roundsToWin*2)+10))
    topBuffer=50
    ropeThickness=int(knotWidthHeight/2)
    ropeThicknessHalf=int(ropeThickness/2)

    screen = pygame.display.set_mode((screenWidth, screenHeight),pygame.FULLSCREEN,screenBitDepth)
    #pygame.display.set_caption('Hello World')
    pygame.mouse.set_visible(0)

    gameFont050=pygame.font.Font(gameFont,50)
    gameFont075=pygame.font.Font(gameFont,75)
    gameFont100=pygame.font.Font(gameFont,100)
    gameFont250=pygame.font.Font(gameFont,250)
    gameFont500=pygame.font.Font(gameFont,500)

    clock=pygame.time.Clock()

    while not allDone:
        screen_title()
        screen_rules()
        screen_game()

    if (isRasPi):
        # clean up
        GPIO.cleanup()


if __name__ == "__main__":
    main()


