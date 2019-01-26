import RPi.GPIO as GPIO

# ignore warnings
GPIO.setwarnings(False)

# use physical pin numbering
GPIO.setmode(GPIO.BOARD)

# set pin 0 to be an input in and set the initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if (GPIO.input(10) == GPIO.HIGH):
        print("Button was pushed!")

# clean up
GPIO.cleanup()

