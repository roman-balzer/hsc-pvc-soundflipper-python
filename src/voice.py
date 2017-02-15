import statistics
import pyaudio
import audioop
import numpy as np
import wave
import RPi.GPIO as gpio


class Voice:
    def __init__(self, configHandler):
        configVoiceParams = configHandler.getVoiceConfig()
        configGPIOParams = configHandler.getGPIOConfig()

        self.FORMAT = pyaudio.paInt16  # We use 16bit format per sample
        self.CHANNELS = int(configVoiceParams['Channels'])
        self.RATE = int(configVoiceParams['Rate'])
        self.SAMPLE_SIZE = int(configVoiceParams['Sample_Size'])  # 1024bytes of data red from a buffer
        self.CHUNK = self.SAMPLE_SIZE
        self.WINDOW = np.blackman(self.CHUNK)

        self.RMS_LOWER_BOUND = int(configVoiceParams['Rms_Lower_Bound'])
        self.RMS_ADAPTION_FACTOR = float(configVoiceParams['Rms_Adaption_Factor'])
        self.RMS_MIN_VALUE = float(configVoiceParams['Rms_Min_Value'])
        self.MEDIAM_SAMPLE_SIZE = int(configVoiceParams['Median_Sample_Size'])

        self.FREQ_LOWER_BOUND = int(configVoiceParams['Freq_Lower_Bound'])
        self.FREQ_THRESHOLD = int(configVoiceParams['Freq_Threshold'])
        self.FREQ_UPPER_BOUND = int(configVoiceParams['Freq_Upper_Bound'])

        # This Factor skews the Freq Threshold, since normally when
        # doing a louder sound, this will result in an increase of the freq
        self.SKEW = int(configVoiceParams['Skew'])

        ## PIN VARS
        self.PIN_LEFT = int(configGPIOParams['Flipper_Left_OutputPin'])
        self.PIN_RIGHT = int(configGPIOParams['Flipper_Right_OutputPin'])

        #SET UP GPIO PINS ON RASPBERRY
        gpio.setmode(gpio.BCM)
        gpio.setup(self.PIN_LEFT,gpio.OUT)
        gpio.setup(self.PIN_RIGHT,gpio.OUT)

    def draw_flipper(self, rms, freq):
        if rms > 5000:
            rms = 5000
        if freq > 1000:
            freq = 1000

        flb = (rms + self.FREQ_LOWER_BOUND*self.SKEW)/self.SKEW
        fub = (rms + self.FREQ_UPPER_BOUND*self.SKEW)/self.SKEW
        fth = (rms + self.FREQ_THRESHOLD*self.SKEW)/self.SKEW

        if rms > self.RMS_LOWER_BOUND:
            if flb <= freq <= fth:
                gpio.output(self.PIN_LEFT, True)
                gpio.output(self.PIN_RIGHT, False)

            elif fth <= freq <= fub:
                gpio.output(self.PIN_LEFT, False)
                gpio.output(self.PIN_RIGHT, True)
            else:
                gpio.output(self.PIN_LEFT, False)
                gpio.output(self.PIN_RIGHT, False)
                pass  # NO MOVEMENT
        else:
            gpio.output(self.PIN_LEFT, False)
            gpio.output(self.PIN_RIGHT, False)


    def run(self):
        # start Recording
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.SAMPLE_SIZE)
        count = 0
        frames = []
        rms_list = []
        while True:
            count += 1
            data = stream.read(self.SAMPLE_SIZE)
            frames.append(data)

            rms = audioop.rms(data, 2)

            indata = np.array(wave.struct.unpack("%dh" % self.CHUNK, data)) * self.WINDOW
            fftData = abs(np.fft.rfft(indata)) ** 2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData) - 1:
                y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                freq = (which + x1) * self.RATE / self.SAMPLE_SIZE
            else:
                freq = which *  self.RATE / self.SAMPLE_SIZE

            # Create a List to calculate the median of the rms
            if count > self.MEDIAM_SAMPLE_SIZE:
                rms_list.pop(0)
            rms_list.append(rms)

            # Adjust the Volume Threshold based on the last RMS values
            self.RMS_LOWER_BOUND = max(self.RMS_ADAPTION_FACTOR * statistics.median(rms_list), self.RMS_MIN_VALUE)
            self.draw_flipper(rms, freq)

    def cleanup(self):
        stream.stop_stream()
        stream.close()
        audio.terminate()
        # @TODO: Dont forget to gpio.cleanup()
