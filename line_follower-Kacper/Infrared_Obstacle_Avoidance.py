import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

# initialise bot
Ab = AlphaBot()

# setup neccessary pins
DR = 16
DL = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

# start by going forward
Ab.forward()
# keep track of last state
last_state = ""
try:
    # main loop
    while True:
        # reset PWM, because turning changes it
        Ab.setPWMB(90)
        Ab.setPWMA(90)
        # get info if sensors see the wall
        DR_status = not(GPIO.input(DR))
        DL_status = not(GPIO.input(DL))

        # if both see the wall go forward
        if ((DL_status == True) and (DR_status == True)):
            Ab.forward()
            print("forward")
            last_state = "f"
        # if right one doesn't see it go right
        elif ((DL_status == True) and (DR_status == False)):
            Ab.right()
            print("right")
            last_state = "r"
        # if left one doesn't see it go left
        elif ((DL_status == False) and (DR_status == True)):
            Ab.left()
            print("left")
            last_state = "l"
        # if it doesn't see anything go left if it wasn't going right
        else:
            if (last_state == "l" or last_state == "f"):
                Ab.left()
                print("left stupid")
                last_state = "l"

except KeyboardInterrupt:
	GPIO.cleanup();
