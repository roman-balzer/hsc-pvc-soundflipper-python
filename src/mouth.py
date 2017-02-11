import RPi.GPIO as GPIO
import configparser
import network

# Get Config-Parameters
config = configparser.ConfigParser()
config.read('config.ini')
configGPIO = config['gpio']

def mouth_happy_pressed():
    network.setMultiplicator(10);

def mouth_sad_pressed():
    network.setMultiplicator(0.5);

def setup():
    Mouth_Button_Happy = int(configGPIO['Mouth_Button_Happy'])
    Mouth_Button_Sad = int(configGPIO['Mouth_Button_Sad'])
    # TODO: check if RISING is correct
    GPIO.add_event_detect(Mouth_Button_Happy, GPIO.RISING, callback=mouth_happy_pressed, bouncetime=200)
    GPIO.add_event_detect(Mouth_Button_Sad, GPIO.RISING, callback=mouth_sad_pressed, bouncetime=200)
