import os

isRasPi=False

if os.uname()[1] == 'raspberrypi':
    print('Running on Raspberry Pi')
    isRasPi=True
else:
    print('Not running on Raspberry Pi')

