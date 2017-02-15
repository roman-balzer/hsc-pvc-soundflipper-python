import RPi.GPIO as GPIO
import network

## Represents the Launcher component on the Flipper. 
class Launcher:
    ## Initializes the Launcher component.
    # Sets the GPIO pins (as in config file) and add callback function if pull-up detected.
    # @param self The object pointer.
    # @param networkHandler The pointer to object of type networkHandler
    # @param configHandler The pointer to object of type configHandler
    def __init__(self, networkHandler, configHandler):
        self.networkHander = networkHandler
        self.isNewGame = True
        config = configHandler.getGPIOConfig()
        Launch_Button = int(config['Launch_Button'])
        GPIO.setup(Launch_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(Launch_Button, GPIO.BOTH, callback=self.launch_button_pressed, bouncetime=200)
    
    ## Sets the member variable isNewGame. 
    # Specifies if the ball in the Launcher has been fallen through the flipper or the ear.
    # If the ball falls through the ear no new game starts. 
    # @param self The object pointer.
    # @param newGame Boolean 
    def setIsNewGame(self, newGame):
        self.isNewGame = newGame

    ## Callback function if pull-up event is detected on lauch button
    # @param self The object pointer.
    def launch_button_pressed(self):
        # check if new game or if ball just dropped from the ear
        if self.isNewGame:
            # if new game the points have to be set to zero
            self.networkHandler.startNewGame()
        # if ear there is nothing to do
