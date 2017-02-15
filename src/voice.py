import statistics
import configparser
import pyaudio
import audioop
import numpy as np
import wave
import RPi.GPIO as gpio

# Get Config-Parameters
config = configparser.ConfigParser()
config.read('./src/config.ini')
configParameters = config['voice']
configGPIO = config['gpio']

FORMAT = pyaudio.paInt16  # We use 16bit format per sample
CHANNELS = int(configParameters['Channels'])
RATE = int(configParameters['Rate'])
SAMPLE_SIZE = int(configParameters['Sample_Size'])  # 1024bytes of data red from a buffer
CHUNK = SAMPLE_SIZE
WINDOW = np.blackman(CHUNK)

RMS_LOWER_BOUND = int(configParameters['Rms_Lower_Bound'])
RMS_ADAPTION_FACTOR = float(configParameters['Rms_Adaption_Factor'])
MEDIAM_SAMPLE_SIZE = int(configParameters['Median_Sample_Size'])

FREQ_LOWER_BOUND = int(configParameters['Freq_Lower_Bound'])
FREQ_THRESHOLD = int(configParameters['Freq_Threshold'])
FREQ_UPPER_BOUND = int(configParameters['Freq_Upper_Bound'])

# This Factor skews the Freq Threshold, since normally when
# doing a louder sound, this will result in an increase of the freq
SKEW = int(configParameters['Skew'])

## PIN VARS
PIN_LEFT = int(configGPIO['Flipper_Left_OutputPin'])
PIN_RIGHT = int(configGPIO['Flipper_Right_OutputPin'])

def setup():
    #SET UP GPIO PINS ON RASPBERRY
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_LEFT,gpio.OUT)
    gpio.setup(PIN_RIGHT,gpio.OUT)

def draw_flipper(rms, freq):
    if rms > 5000:
        rms = 5000
    if freq > 1000:
        freq = 1000

    flb = (rms + FREQ_LOWER_BOUND*SKEW)/SKEW
    fub = (rms + FREQ_UPPER_BOUND*SKEW)/SKEW
    fth = (rms + FREQ_THRESHOLD*SKEW)/SKEW

    if rms > RMS_LOWER_BOUND:
        if flb <= freq <= fth:
            gpio.output(PIN_LEFT, True)
            gpio.output(PIN_RIGHT, False)

        elif fth <= freq <= fub:
            gpio.output(PIN_LEFT, False)
            gpio.output(PIN_RIGHT, True)
        else:
            gpio.output(PIN_LEFT, False)
            gpio.output(PIN_RIGHT, False)
            pass  # NO MOVEMENT
    else:
        gpio.output(PIN_LEFT, False)
        gpio.output(PIN_RIGHT, False)


def run():
    # start Recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=SAMPLE_SIZE)
    count = 0
    frames = []
    rms_list = []
    while True:
        count += 1
        data = stream.read(SAMPLE_SIZE)
        frames.append(data)

        rms = audioop.rms(data, 2)

        indata = np.array(wave.struct.unpack("%dh" % CHUNK, data)) * WINDOW
        fftData = abs(np.fft.rfft(indata)) ** 2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            freq = (which + x1) * RATE / SAMPLE_SIZE
        else:
            freq = which * RATE / SAMPLE_SIZE

        # Create a List to calculate the median of the rms
        if count > MEDIAM_SAMPLE_SIZE:
            rms_list.pop(0)
        rms_list.append(rms)

        # Adjust the Volume Threshold based on the last RMS values
        RMS_LOWER_BOUND = RMS_ADAPTION_FACTOR * statistics.median(rms_list)
        draw_flipper(rms, freq)

def cleanup():
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # @TODO: Dont forget to gpio.cleanup()
