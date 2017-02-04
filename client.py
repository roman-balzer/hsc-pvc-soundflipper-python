import threading
import network
import ear
import voice

network.setup()
ear.setup()
voice.setup()

try: 
    while True:
        ear.run()
       # voice.run()

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()

