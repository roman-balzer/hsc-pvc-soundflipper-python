import statistics

import pyaudio
import audioop
import numpy as np
import wave
import only_plot as flip
#import RPi.GPIO as gpio

FORMAT = pyaudio.paInt16  # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 1024  # 1024bytes of data red from a buffer
RECORD_DURATION = 3000

CHUNK = SAMPLE_SIZE
WINDOW = np.blackman(CHUNK)

RMS_LOWER_BOUND = 1000
RMS_UPPER_BOUND = 10000.0

FREQ_LOWER_BOUND = 0
FREQ_THRESHOLD = 300
FREQ_UPPER_BOUND = 1000

# This Factor skews the Freq Threshold, since normally when
# doing a louder sound, this will result in an increase of the freq
SKEW = 300

## PIN VARS
PIN_LEFT = 11
PIN_RIGHT = 13
PWM_FREQ = 100

#SET UP GPIO PINS ON RASPBERRY
#gpio.setmode(gpio.BOARD)
#gpio.setup(PIN_LEFT,gpio.OUT)
#gpio.setup(PIN_RIGHT,gpio.OUT)


def draw_flipper(rms, freq, count):
    return
    if rms > 5000:
        rms = 5000
    if freq > 1000:
        freq = 1000

    flb = (rms + FREQ_LOWER_BOUND*SKEW)/SKEW
    fub = (rms + FREQ_UPPER_BOUND*SKEW)/SKEW
    fth = (rms + FREQ_THRESHOLD*SKEW)/SKEW

    if flb <= freq <= fth:
        # LEFT FLIPPER
        gpio.output(PIN_LEFT, True)
        gpio.output(PIN_RIGHT, False)

    elif fth <= freq <= fub:
        # RIGHT FLIPPER
        gpio.output(PIN_LEFT, False)
        gpio.output(PIN_RIGHT, True)
    else:
        gpio.output(PIN_LEFT, False)
        gpio.output(PIN_RIGHT, False)

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=SAMPLE_SIZE)

frames = []
count = 0
rmsA=[]
rmsMedianA=[]
rmsMeanA=[]
freqA=[]
countA=[]
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

    print("RMS: %f" % rms)
    print("FREQ: %f" % freq)

    if count < 100:
        rms +=1000

    if count >= 200:

        rmsA.pop(0)
        freqA.pop(0)
        rmsMedianA.pop(0)
        rmsMeanA.pop(0)
    else:
        countA.append(count)
    rmsA.append(rms)
    freqA.append(freq)
    rmsMedianA.append(statistics.median(rmsA))
    rmsMeanA.append(statistics.mean(rmsA))


    draw_flipper(rms, freq, count)
    flip.plot(rmsA, freqA, countA,rmsMedianA,rmsMeanA)

stream.stop_stream()
stream.close()
audio.terminate()
#gpio.cleanup()
