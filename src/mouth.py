import RPi.GPIO as GPIO
import time
import network

class Mouth:
    def __init__(self, networkHandler, configHandler):
        print("Mouth setup")
        self.networkHandler = networkHandler
        config = configHandler.getGPIOConfig()
        Mouth_Button_Happy = int(config['Mouth_Button_Happy'])
        Mouth_Button_Sad = int(config['Mouth_Button_Sad'])

        GPIO.setup(Mouth_Button_Happy, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Mouth_Button_Sad, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(Mouth_Button_Happy, GPIO.BOTH, callback=mouth_happy_pressed, bouncetime=200)
        GPIO.add_event_detect(Mouth_Button_Sad, GPIO.BOTH, callback=mouth_sad_pressed, bouncetime=200)

    def mouth_happy_pressed(channel):
        print("Mouth-Happy-Pressed Callback")
        self.networkHandler.setMultiplicator(1.5)

    def mouth_sad_pressed(channel):
        print('Edge detected on channel %s'%channel)
        print("Mouth-Sad-Pressed Callback")
        self.networkHandler.setMultiplicator(0.5)

