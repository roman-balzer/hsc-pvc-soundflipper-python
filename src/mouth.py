import RPi.GPIO as GPIO
import configparser
import time
import network

# Get Config-Parameters
config = configparser.ConfigParser()
config.read('./src/config.ini')
configGPIO = config['gpio']

def mouth_happy_pressed(channel):
    print("Mouth-Happy-Pressed Callback")
    network.setMultiplicator(1.5)

def mouth_sad_pressed(channel):
    print('Edge detected on channel %s'%channel)
    print("Mouth-Sad-Pressed Callback")
    network.setMultiplicator(0.5)

def setup():
    print("Mouth setup")

    Mouth_Button_Happy = int(configGPIO['Mouth_Button_Happy'])
    Mouth_Button_Sad = int(configGPIO['Mouth_Button_Sad'])

    GPIO.setup(Mouth_Button_Happy, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Mouth_Button_Sad, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(Mouth_Button_Happy, GPIO.BOTH, callback=mouth_happy_pressed, bouncetime=200)
    GPIO.add_event_detect(Mouth_Button_Sad, GPIO.FALLING, callback=mouth_sad_pressed, bouncetime=200)
