import RPi.GPIO as GPIO
import threading
import network
import ear
#import launch
#import voice
#import mouth

network.setup()
#launch.setup()
#voice.setup()
#mouth.setup()

#the ear component runs in its own thread 
class EarThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ear.setup()
        print('initialized ear-thread')

    def run(self):
        print('startet ear-thread')
        while True:
            ear.run()
        print('Finished ear-thread')
try:
    #start the ear thread
    background = EarThread()
    background.start()

    #the voice component acts as the main Programm
    #there goes the function call of voice component
    #voice.run()

    background.join()

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt: 
    GPIO.cleanup()
    voice.cleanup()

