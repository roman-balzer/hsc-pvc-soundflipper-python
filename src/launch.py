import RPi.GPIO as GPIO
import configparser
import network

isNewGame = True

# Get Config-Parameters
config = configparser.ConfigParser()
config.read('config.ini')
configGPIO = config['gpio']

def setNewGameFalse():
    global isNewGame
    isNewGame = False

def launch_button_pressed():
    global isNewGame
     # check if new game or if ball just dropped from the ear
    if isNewGame:
        # if new game the points have to be set to zero
        network.startNewGame()
    # if ear there is nothing to do

def setup():
    global isNewGame
    isNewGame = True

    Launch_Button = int(configGPIO['Launch_Button'])
    # TODO: check if RISING is correct
    GPIO.add_event_detect(Launch_Button, GPIO.RISING, callback=launch_button_pressed, bouncetime=200)
