import os
import time
#import RPi.GPIO as GPIO
from gpiozero import Button

#offButton = 4
offButton = Button(4)


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(offButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#offValue = 1
while 1:
    
    #offValue = GPIO.input(offButton)
    if offButton.is_pressed: 
    #if offValue == 0:
        #print("pressed")
        time.sleep(2)
        #offValue = GPIO.input(offButton)
        if offButton.is_pressed:
        #if offValue == 0:
            #print("shutdown")
            os.system("shutdown now -h")
            time.sleep(1)