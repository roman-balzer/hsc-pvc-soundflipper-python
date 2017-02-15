import time
import RPi.GPIO as GPIO
import subprocess
import random

class Ear:
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

    def onBallDetection(self):
        self.launcher.setIsNewGame(False)
        self.networkHandler.send(100)
        randomNumber = random.randrange(1,4)
        audioFilePath = "audio/" + str(randomNumber) + ".mp3"
        subprocess.Popen(["mpg123", audioFilePath])

    def run(self):
        # distancesmessung wird mittels des 10us langen Triggersignals gestartet
        GPIO.output(self.Trigger_OutputPin, True)
        time.sleep(self.carrier_Signal_duration)
        GPIO.output(self.Trigger_OutputPin, False)

        # Hier wird die Stopuhr gestartet
        timeOn = time.time()
        while GPIO.input(self.Echo_InputPin) == 0:
            timeOn = time.time() # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird

        while GPIO.input(self.Echo_InputPin) == 1:
            timeOff = time.time() # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war

        # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
        duration = timeOff - timeOn
        # Mittels dieser kann nun der distance auf Basis der Schallgeschwindigkeit der distance berechnet werden
        distance = (duration * 34300) / 2

        # Überprüfung, ob der gemessene Wert innerhalb der zulässigen Entfernung liegt
        if distance < 2 or (round(distance) > 300):
            # Es wird davon ausgegangen, dass wenn der gemessene Wert außerhalb des Bereichs liegt, dass dann ein Ball
            # in das Ohr gefallen ist.
            #print("distance außerhalb des Messbereich")
            #print("------------------------------")
            self.onBallDetection()
        else:
            # Der distance wird auf zwei Stellen hinterm Komma formatiert
            distance = format((duration * 34300) / 2, '.2f')
            #print("Der distance beträgt:%s"%distance)
            #print("------------------------------")
            if float(distance) <= self.maxDistance:
                self.onBallDetection()

        # Pause zwischen den einzelnen Messungen
        time.sleep(self.sleeptime)

