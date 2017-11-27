"""=========================
Plot the audio signal
========================="""

# Copyright (c) Nov. 2017
# Chao Peng, Yufan Du, Peking University, Beijing, China
# All rights reserved.

import os
import matplotlib.pyplot as plt
import constant as CONST

# Draw a gap plot for each experiment
def everyGapPlot(data):
    highFreq, bandWidths = CONST.FREANDBAND[CONST.totalCounter]
    plt.title('Fre:%sHz, Ban:%sHz'%(highFreq, bandWidths), size=14)
    plt.xlabel('Experiment times', size=14)
    plt.ylabel('Gap (ms)', size=14)
    plt.plot(data, color='r', linestyle='--', marker='o')

    plt.savefig(os.path.join(CONST.fileAddress, "F%sB%s.png"%(highFreq, bandWidths)))

# Draw plots for all gap experiments
def totalGapPlot(data):
    plt.xlabel("Bandwidth (Hz)", size=14)
    plt.ylabel('Gap (ms)', size=14)
    plt.plot(data[0, 0:4], color='r', linestyle='--', marker='o', label='600 Hz')
    plt.plot(data[1, 0:6], color='y', linestyle='--', marker='o', label='2200 Hz')
    plt.plot(data[2, 0:6], color='g', linestyle='--', marker='o', label='4400 Hz')
    plt.legend()

    plt.savefig(os.path.join(CONST.fileAddress, "allGap.png"))