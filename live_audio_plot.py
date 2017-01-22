import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
import wave
from matplotlib.widgets import Slider, Button

FORMAT = pyaudio.paInt16  # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 10240  # 1024bytes of data red from a buffer
RECORD_DURATION = 300
WAVE_OUTPUT_FILENAME = "file.wav"

CHUNK = SAMPLE_SIZE;
WINDOW = np.blackman(CHUNK)

RMS_LOWER_BOUND = 1000
RMS_UPPER_BOUND = 10000.0

FREQ_LOWER_BOUND = 0
FREQ_THRESHOLD = 300

FREQ_UPPER_BOUND = 1000

# This Factor skews the Freq Threshold, since normally when
# doing a louder sound, this will result in an increase of the freq
SKEW = 300

# Flipper Positions
left_flip_x = [-200, -100, -200, -210, -200]
left_flip_y = [-10, -100, 10, 0, -10]
right_flip_x = [200, 100, 200, 210, 200]
right_flip_y = [-10, -100, 10, 0, -10]

# Set up plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
#plt.xlabel("Frequency")
#plt.ylabel("RMS")
plt.axis([-300, 300, -200, 200])
ax.set_yticklabels([])
ax.set_xticklabels([])

line1, line2 = plt.plot(left_flip_x, left_flip_y, 'r-', right_flip_x, right_flip_y, 'b-', linewidth=4)

axcolor = 'lightgoldenrodyellow'
axfreq_threshold = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
sfreq_threshold = Slider(axfreq_threshold, 'Freq Threshold', 0, 1000, valinit=FREQ_THRESHOLD)

axrms_upper = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
srms_upper = Slider(axrms_upper, 'RMS Upper Bound', 0, 20000, valinit=RMS_UPPER_BOUND)

axrms_lower = plt.axes([0.25, 0.21, 0.65, 0.03], axisbg=axcolor)
srms_lower = Slider(axrms_lower, 'RMS Lower Bound', 0, 5000, valinit=RMS_LOWER_BOUND)

axskew = plt.axes([0.25, 0.25, 0.65, 0.03], axisbg=axcolor)
sskew = Slider(axskew, 'Skew Factor', 1, 500, valinit=SKEW)

text_thresh = ax.text(-90,230, ('Threshold:' + str(FREQ_THRESHOLD)) , style='italic')

def update(val):
    global FREQ_THRESHOLD
    FREQ_THRESHOLD = sfreq_threshold.val
    global RMS_UPPER_BOUND
    RMS_UPPER_BOUND = srms_upper.val
    global RMS_LOWER_BOUND
    RMS_LOWER_BOUND = srms_lower.val
    global SKEW
    SKEW = sskew.val
sfreq_threshold.on_changed(update)
srms_upper.on_changed(update)
srms_lower.on_changed(update)
sskew.on_changed(update)


def draw_flipper(rms, freq):
    title = 'RMS: ' + str(int(rms)) + ' --- Freq:' + str(int(freq))
    print(title)
    plt.title(title)

    move_x = 0
    if RMS_LOWER_BOUND <= rms:
        percentage_in_bounds = ((rms - RMS_LOWER_BOUND) / (RMS_UPPER_BOUND - RMS_LOWER_BOUND))
        calc_val = (percentage_in_bounds * 200) - 100
        move_y = max(min(100, calc_val), -100)
        if percentage_in_bounds > 0.5:
            move_x = (1 - min(1, percentage_in_bounds)) * 80
        else:
            move_x = percentage_in_bounds * 80
    else:
        move_y = -100

    flb = (rms + FREQ_LOWER_BOUND*SKEW)/SKEW
    fub = (rms + FREQ_UPPER_BOUND*SKEW)/SKEW
    fth = (rms + FREQ_THRESHOLD*SKEW)/SKEW
    text_thresh.set_text("Threshold: " +str(fth))
    print fth

    if flb <= freq <= fth:
        # LEFT FLIPPER
        right_flip_y[1] = -100
        right_flip_x[1] = 100
        left_flip_y[1] = move_y
        left_flip_x[1] = -100+move_x
    elif fth <= freq <= fub:
        # RIGHT FLIPPER
        left_flip_y[1] = -100
        left_flip_x[1] = -100
        right_flip_y[1] = move_y
        right_flip_x[1] = 100-move_x
    else:
        pass  # NO MOVEMENT

    line1.set_xdata(left_flip_x)
    line1.set_ydata(left_flip_y)
    line2.set_xdata(right_flip_x)
    line2.set_ydata(right_flip_y)

    fig.canvas.draw()
    plt.pause(0.00001)  # Note this correction


audio = pyaudio.PyAudio()


# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=SAMPLE_SIZE)

frames = []
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

    draw_flipper(rms, freq)

stream.stop_stream()
stream.close()
audio.terminate()
