import pyaudio
import audioop
import numpy as np
import wave
import RPi.GPIO as gpio


# SETUP VARIABLES

## READ AUDIO VARS
FORMAT = pyaudio.paInt16  # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 10240  # 1024bytes of data red from a buffer
RECORD_DURATION = 300
WAVE_OUTPUT_FILENAME = "file.wav"

CHUNK = SAMPLE_SIZE;
WINDOW = np.blackman(CHUNK)

## FLIPPER MOVEMENT VARS
RMS_LOWER_BOUND = 1000
RMS_UPPER_BOUND = 10000.0

FREQ_LOWER_BOUND = 0
FREQ_THRESHOLD = 300
FREQ_UPPER_BOUND = 1000

## PIN VARS
PIN_LEFT = 11
PIN_RIGHT = 13
PWM_FREQ = 100

#SET UP GPIO PINS ON RASPBERRY
gpio.setmode(gpio.BOARD)
gpio.setup(PIN_LEFT,gpio.OUT)
gpio.setup(PIN_RIGHT,gpio.OUT)

FLIP_LEFT = gpio.PWM(PIN_LEFT,PWM_FREQ)
FLIP_RIGHT = gpio.PWM(PIN_RIGHT,PWM_FREQ)
FLIP_LEFT.start(0)
FLIP_RIGHT.start(0)


def flipper_movement(rms, freq):
    if RMS_LOWER_BOUND <= rms:
        percentage_in_bounds = ((rms - RMS_LOWER_BOUND) / (RMS_UPPER_BOUND - RMS_LOWER_BOUND))
    else:
        percentage_in_bounds = 0

    if FREQ_LOWER_BOUND <= freq <= FREQ_THRESHOLD:
        # LEFT FLIPPER
        FLIP_LEFT.ChangeDutyCycle(percentage_in_bounds)
        FLIP_RIGHT.ChangeDutyCycle(0)
        print("LEFT")
    elif FREQ_THRESHOLD <= freq <= FREQ_UPPER_BOUND:
        # RIGHT FLIPPER
        print("RIGHT")
        FLIP_RIGHT.ChangeDutyCycle(percentage_in_bounds)
        FLIP_LEFT.ChangeDutyCycle(0)
    else:
        pass  # NO MOVEMENT


audio = pyaudio.PyAudio()


# START RECORDING
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=SAMPLE_SIZE)
frames = []

# LOOP
for i in range(0, int(RATE / SAMPLE_SIZE * RECORD_DURATION)):
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

    flipper_movement(rms, freq)

# PROGRAM END
stream.stop_stream()
stream.close()
audio.terminate()
gpio.cleanup()
