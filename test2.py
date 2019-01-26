import RPi.GPIO as GPIO

def button_callback1(channel):
    print("Button 1 was pushed!")

def button_callback2(channel):
    print("Button 2 was pushed!")

# ignore warnings
GPIO.setwarnings(False)

# use physical pin numbering
GPIO.setmode(GPIO.BOARD)

# set pin 0 to be an input in and set the initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup event on pin 10 rising edge
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback1,bouncetime=100)

# Setup event on pin 12 rising edge
GPIO.add_event_detect(12,GPIO.RISING,callback=button_callback2,bouncetime=100)

# Run until user hits the enter key
message=input("Press enter to quit\n\n")

# clean up
GPIO.cleanup()

