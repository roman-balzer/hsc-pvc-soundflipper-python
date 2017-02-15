import time
import RPi.GPIO as GPIO
import subprocess
import random

## Represents the Ear component on the Flipper. 
# If the ball falls through the ear. It has to be detected.
# Also a random sound file should be played.
class Ear:

    ## Constructor of ear. 
    # Sets the GPIO pins (as in config file). 
    # Sets the parameter for the ultra sonic sensor as specified in config file.
    # Set random seed für random number generation to select an audio file randomly.
    # @param self The object pointer.
    # @param networkHandler The pointer to object of type networkHandler
    # @param configHandler The pointer to object of type configHandler
    def __init__(self, networkHandler, configHandler, launcher):
        self.networkHandler = networkHandler
        self.launcher = launcher
        config = configHandler.getGPIOConfig()
        configEar = configHandler.getEarConfig()

        self.Trigger_OutputPin = int(config['Trigger_OutputPin'])
        self.Echo_InputPin = int(config['Echo_InputPin'])
        self.sleeptime = float(configEar['Sleeptime'])
        self.maxDistance = int(configEar['Distance'])
        self.carrier_Signal_duration = float(configEar['Carrier_Signal_Duration'])

        random.seed()
        GPIO.setup(self.Trigger_OutputPin, GPIO.OUT)
        GPIO.setup(self.Echo_InputPin, GPIO.IN)
        GPIO.output(self.Trigger_OutputPin, False)
    
    ## If the ball in the ear is detected the isGame Flag is set to False.
    # So that the score is not change
    def onBallDetection(self):
        #self.launcher.setIsNewGame(False)
        print("Ball detekted")
        self.networkHandler.send(100)
        randomNumber = random.randrange(1,4)
        audioFilePath = "audio/" + str(randomNumber) + ".mp3"
        #subprocess.Popen(["mpg123", audioFilePath])

    def run(self):
        # Abstandsmessung wird mittels des 10us langen Triggersignals gestartet
        GPIO.output(self.Trigger_OutputPin, True)
        time.sleep(self.carrier_Signal_duration)
        GPIO.output(self.Trigger_OutputPin, False)

        # Hier wird die Stopuhr gestartet
        EinschaltZeit = time.time()
        while GPIO.input(self.Echo_InputPin) == 0:
            EinschaltZeit = time.time() # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird

        while GPIO.input(self.Echo_InputPin) == 1:
            AusschaltZeit = time.time() # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war

        # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
        Dauer = AusschaltZeit - EinschaltZeit
        # Mittels dieser kann nun der Abstand auf Basis der Schallgeschwindigkeit der Abstand berechnet werden
        Abstand = (Dauer * 34300) / 2

        # Überprüfung, ob der gemessene Wert innerhalb der zulässigen Entfernung liegt
        if Abstand < 2 or (round(Abstand) > 300):
            # Falls nicht wird eine Fehlermeldung ausgegeben
            print("Abstand außerhalb des Messbereich")
            print("------------------------------")
            self.onBallDetection()
        else:
            # Der Abstand wird auf zwei Stellen hinterm Komma formatiert
            Abstand = format((Dauer * 34300) / 2, '.2f')
            # Der berechnete Abstand wird auf der Konsole ausgegeben
            print(Abstand)
            print("------------------------------")
            if float(Abstand) <= self.maxDistance:
                self.onBallDetection()

        # Pause zwischen den einzelnen Messungen
        time.sleep(self.sleeptime)

