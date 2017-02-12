import statistics

import matplotlib.pyplot as plt
import numpy as np

# Flipper Positions
left_flip_x = [-200, -100, -200, -210, -200]
left_flip_y = [-10, -100, 10, 0, -10]
right_flip_x = [200, 100, 200, 210, 200]
right_flip_y = [-10, -100, 10, 0, -10]

# Set up plot
fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.35)
# plt.xlabel("Frequency")
# plt.ylabel("RMS")
ax.set_yticklabels([])
ax.set_xticklabels([])

RMS_LOWER_BOUND = 1000
RMS_UPPER_BOUND = 10000.0

FREQ_LOWER_BOUND = 0
FREQ_THRESHOLD = 300
FREQ_UPPER_BOUND = 1000

SKEW = 300

plt.subplot(311)
plt.axis([-300, 300, -200, 200])
line1, line2 = plt.plot(left_flip_x, left_flip_y, 'r-', right_flip_x, right_flip_y, 'b-', linewidth=4)

plt.subplot(312)
plt.axis([0, 200, 0, 5000])
rmsLine, rmed, rmean = plt.plot([], 'b-',[], [], 'm-',[], [], 'y-', linewidth=1)
lrms = plt.axhline(RMS_LOWER_BOUND,0,200,linewidth=1, color='k')

plt.subplot(313)
plt.axis([0, 200, 0, 1000])
freqLine, fmedl, fmeanl = plt.plot([], [], 'r-',[], [], 'm-',[], [], 'y-', linewidth=1)
lf = plt.axhline(FREQ_THRESHOLD,0,200,linewidth=1, color='k')


# axcolor = 'lightgoldenrodyellow'
# axfreq_threshold = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
# sfreq_threshold = Slider(axfreq_threshold, 'Freq Threshold', 0, 1000, valinit=FREQ_THRESHOLD)

# axrms_upper = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
# srms_upper = Slider(axrms_upper, 'RMS Upper Bound', 0, 20000, valinit=RMS_UPPER_BOUND)

# axrms_lower = plt.axes([0.25, 0.21, 0.65, 0.03], axisbg=axcolor)
# srms_lower = Slider(axrms_lower, 'RMS Lower Bound', 0, 5000, valinit=RMS_LOWER_BOUND)

# axskew = plt.axes([0.25, 0.25, 0.65, 0.03], axisbg=axcolor)
# sskew = Slider(axskew, 'Skew Factor', 1, 500, valinit=SKEW)

# text_thresh = ax.text(-90,230, ('Threshold:' + str(FREQ_THRESHOLD)) , style='italic')

# def update(val):
#    global FREQ_THRESHOLD
#    FREQ_THRESHOLD = sfreq_threshold.val
#    global RMS_UPPER_BOUND
#    RMS_UPPER_BOUND = srms_upper.val
#    global RMS_LOWER_BOUND
#    RMS_LOWER_BOUND = srms_lower.val
#    global SKEW
#    SKEW = sskew.val
# sfreq_threshold.on_changed(update)
# srms_upper.on_changed(update)
# srms_lower.on_changed(update)
# sskew.on_changed(update)

lrmsA = []

def plot(rmsA, freqA, countA, rMed, rMean, fmda, fmea):
    global lrms
    global lf

    RMS_LOWER_BOUND = max(1.2 * rMed[len(rMed)-1],800)
    FREQ_THRESHOLD = max(1.2 * fmda[len(fmda)-1],300)
    lrms.set_ydata([RMS_LOWER_BOUND,RMS_LOWER_BOUND])
    lf.set_ydata([FREQ_THRESHOLD,FREQ_THRESHOLD])

    rms = rmsA[len(rmsA)-1]
    freq = freqA[len(freqA)-1]

    if rms > 5000:
        rms = 5000
    if freq > 1000:
        freq = 1000

    title = 'RMS: ' + str(int(rms)) + ' --- Freq:' + str(int(freq))
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
        # This essentially change flipper movement to be binary
        move_y = 100
    else:
        move_y = -100

    flb = (rms + FREQ_LOWER_BOUND*SKEW)/SKEW
    fub = (rms + FREQ_UPPER_BOUND*SKEW)/SKEW
    fth = (rms + FREQ_THRESHOLD*SKEW)/SKEW

    if flb <= freq <= fth:
        # LEFT FLIPPER
        right_flip_y[1] = -100
        right_flip_x[1] = 100
        left_flip_y[1] = move_y
        #left_flip_x[1] = -100+move_x

    elif fth <= freq <= fub:
        # RIGHT FLIPPER
        left_flip_y[1] = -100
        left_flip_x[1] = -100
        right_flip_y[1] = move_y
        #right_flip_x[1] = 100-move_x
    else:
        pass  # NO MOVEMENT
    line1.set_xdata(left_flip_x)
    line1.set_ydata(left_flip_y)
    line2.set_xdata(right_flip_x)
    line2.set_ydata(right_flip_y)

    freqLine.set_ydata(freqA)
    freqLine.set_xdata(countA)
    rmsLine.set_ydata(rmsA)
    rmsLine.set_xdata(countA)
    rmed.set_ydata(rMed)
    rmed.set_xdata(countA)
    rmean.set_ydata(rMean)
    rmean.set_xdata(countA)
    fmedl.set_ydata(fmda)
    fmedl.set_xdata(countA)
    fmeanl.set_ydata(fmea)
    fmeanl.set_xdata(countA)

    fig.canvas.draw()
    plt.pause(0.00001)  # Note this correction
