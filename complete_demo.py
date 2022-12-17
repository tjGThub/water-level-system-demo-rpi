# 4 video(1 is company logo video which is used during idle) &
# 3 button(1 emergency stop,one start button & *one shutdown button)
# *shutdown button is done in another python script

import RPi.GPIO as GPIO
import vlc
import time

import subprocess
from subprocess import Popen


gButton = 13
rButton = 12

motor = 18

sensor1 = 21
led1 = 20

sensor2 = 26
led2 = 19

def setVid1():
    player1.set_media(video1)
    player2.set_media(video1)
    #print('Done setting video 1')

def setVid2():
    player1.set_media(video2)
    player2.set_media(video2)
    #print('Done setting video 2')
    
def setVid3():
    player1.set_media(video3)
    player2.set_media(video3)
    #print('Done setting video 3')
    
def setVid4():
    player1.set_media(video4)
    player2.set_media(video4)
    #print('Done setting video 4')

#NOT USED
#Need to change the sleep time according to how long is the video
def runVid():
    player1.play()
    #print('play player1')
    time.sleep(1)
    player2.stop()
    #print('stop player2')
    time.sleep(3)
    player2.play()
    #print('play player2')
    time.sleep(1)
    player1.stop()
    #print('stop player1')
    time.sleep(3)

#Need to first put a black screen at the background so that we wont 
# see the desktop during video transitions.    
def runVid2():
    player1.play()
    if player1.get_state() == vlc.State.Ended:
        player1.stop()

def stopVid():
    player1.stop()
    player2.stop()

def gpioInit() :
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(rButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(gButton,GPIO.RISING,callback=gButtonCallback)
    #GPIO.add_event_detect(rButton,GPIO.RISING,callback=rButtonCallback)
    
    GPIO.setup(motor,GPIO.OUT)
    
    GPIO.setup(sensor1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led1,GPIO.OUT)
    
    GPIO.setup(sensor2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led2,GPIO.OUT)

def gpioOff() :
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(motor, GPIO.LOW)
    
def gButtonCallback(channel):
    #print("gbutton pushed")
    global gValue
    gValue == 0
    
def rButtonCallback(channel):
    #print("rbutton pushed")
    global rValue
    rValue == 0

##################### PUT YOUR VIDEO LINK HERE ###################
vid1 = ("/home/test/Desktop/vid.mp4")
vid2 = ("/home/test/Desktop/vid1.mp4")
vid3 = ("/home/test/Desktop/vid2.mp4")
vid4 = ("/home/test/Desktop/vid2.mp4")
##################################################################

gpioInit()
#Put black screen on background so we dont see the desktop when switch video.
subprocess.call("feh -F /home/test/Desktop/black.jpeg &", shell=True)

player1 = vlc.MediaPlayer()
player2 = vlc.MediaPlayer()

video1 = vlc.Media(vid1)
video2 = vlc.Media(vid2)
video3 = vlc.Media(vid3)
video4 = vlc.Media(vid4)

player1.toggle_fullscreen()

gValue = 1
rValue = 1
setVid1()

while 1:
    #Run company logo video 1
    if rValue == 0:
        setVid1()
    runVid2()
    
    gValue = GPIO.input(gButton)
    rValue = GPIO.input(rButton)
    #If green button pressed
    if gValue == 0:
        #Stop company logo video
        stopVid()
        
        while 1:
            #If red button pressed then stop video and gpios
            rValue = GPIO.input(rButton)
            if rValue == 0:
                gpioOff()
                stopVid()
                break
                
            value1 = GPIO.input(sensor1)
            value2 = GPIO.input(sensor2)
            
            #Stage 1 video 2
            if value1 == 0 and value2 == 0:
                GPIO.output(led1, GPIO.LOW)
                GPIO.output(led2, GPIO.LOW)
                GPIO.output(motor,GPIO.HIGH)
                setVid2()
                while value1 == 0:
                    runVid2()
                    
                    rValue = GPIO.input(rButton)
                    if rValue == 0:
                        gpioOff()
                        stopVid()
                        break
                        
                    value1 = GPIO.input(sensor1)
                    if value1 == 1:
                        stopVid()
                        break
            #Stage 2 video 3
            elif value1 == 1 and value2 == 0:
                GPIO.output(led1, GPIO.HIGH)
                GPIO.output(led2, GPIO.LOW)
                setVid3()
                while value1 == 1 and value2 == 0:
                    runVid2()
                    
                    rValue = GPIO.input(rButton)
                    if rValue == 0:
                        gpioOff()
                        stopVid()
                        break

                    value1 = GPIO.input(sensor1)
                    value2 = GPIO.input(sensor2)
                    if value1 == 0 and value2 == 1:
                        stopVid()
                        break
            #Stage 3 video 4
            elif value1 == 1 and value2 == 1:
                GPIO.output(led1, GPIO.HIGH)
                GPIO.output(led2, GPIO.HIGH)
                setVid4()
                while value2 == 1:
                    runVid2()
                    #Let water pump run for 5s when at level 2 before shutting off water pump
                    time.sleep(5)
                    GPIO.output(motor,GPIO.LOW)
                
                    rValue = GPIO.input(rButton)
                    if rValue == 0:
                        gpioOff()
                        stopVid()
                        break
                        
                    value2 = GPIO.input(sensor2)
                    if value2 == 0:
                        stopVid()
                        break
            
            if rValue == 0:
                break
 
GPIO.cleanup()
stopVid()