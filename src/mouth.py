import RPi.GPIO as GPIO
import time
import network

## Represents the Mouth component on the Flipper. Has two contact plates.
class Mouth:

    ## Initializes the Mouth component.
    # Sets the GPIO pins (as in config file) and add callback function if pull-up detected.
    # @param self The object pointer.
    # @param networkHandler The pointer to object of type networkHandler
    # @param configHandler The pointer to object of type configHandler
    def __init__(self, networkHandler, configHandler):
        print("Mouth setup")
        self.networkHandler = networkHandler
        config = configHandler.getGPIOConfig()
        Mouth_Button_Happy = int(config['Mouth_Button_Happy'])
        Mouth_Button_Sad = int(config['Mouth_Button_Sad'])

        GPIO.setup(Mouth_Button_Happy, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Mouth_Button_Sad, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(Mouth_Button_Happy, GPIO.BOTH, callback=self.mouth_happy_pressed, bouncetime=200)
        GPIO.add_event_detect(Mouth_Button_Sad, GPIO.BOTH, callback=self.mouth_sad_pressed, bouncetime=200)

    ## Callback function when the Flipper is happy. 
    # That means if the Flipper is in up position.
    # Sets the score muliplicator to 1.5. 
    # @param channel The GPIO channel on which the pull-up event is detected
    def mouth_happy_pressed(self, channel):
        print("Mouth-Happy-Pressed Callback")
        self.networkHandler.setMultiplicator(1.5)
    
    ## Callback function when the Flipper is sad. 
    # That means if the Flipper is in down position.
    # Sets the score muliplicator to 1.5.  
    # @param channel The GPIO channel on which the pull-up event is detected
    def mouth_sad_pressed(self, channel):
        print("Mouth-Sad-Pressed Callback")
        self.networkHandler.setMultiplicator(0.5)

