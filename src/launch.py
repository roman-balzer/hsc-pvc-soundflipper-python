import RPi.GPIO as GPIO
import network

## Represents the Launcher component on the Flipper. 
class Launcher:
    
    def __init__(self, networkHandler, configHandler):
        self.networkHander = networkHandler
        self.isNewGame = True
        config = configHandler.getGPIOConfig()
        Launch_Button = int(config['Launch_Button'])
        GPIO.setup(Launch_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(Launch_Button, GPIO.BOTH, callback=self.launch_button_pressed, bouncetime=200)

    def setIsNewGame(self, newGame):
        self.isNewGame = newGame

    def launch_button_pressed(self):
        # check if new game or if ball just dropped from the ear
        if self.isNewGame:
            # if new game the points have to be set to zero
            self.networkHandler.startNewGame()
        # if ear there is nothing to do
