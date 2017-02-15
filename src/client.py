import RPi.GPIO as GPIO
import threading
from network import NetworkHandler
from ear import Ear
from launch import Launcher
from voice import Voice
from mouth import Mouth
from config import ConfigHandler

GPIO.setmode(GPIO.BCM)

config = ConfigHandler()
network = NetworkHandler(config)
launcher = Launcher(network, config)
mouth = Mouth(network, config)
voice = Voice(config)


## Encapsulates the Ear component in  own thread.
# Because the Ear uses polling to check the value of the ultra sonic sensor. 
class EarThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ear = Ear(network, config, launcher)
        print('initialized ear-thread')
    
    def run(self):
        print('startet ear-thread')
        while True:
            self.ear.run()
        print('Finished ear-thread')
try:
    #start the ear thread
    background = EarThread()
    background.start()
    #the voice component acts as the main Programm
    voice.run()
    background.join()

# clean up after termination of the programm
except KeyboardInterrupt: 
    GPIO.cleanup()
    voice.cleanup()

