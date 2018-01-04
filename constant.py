"""=========================================================
# Copyright (c) Nov. 2017
# All rights reserved.
========================================================="""

import numpy as np

correctNum = 0
ClickNum = 0
RandomNum = 0

turningNum = 0
gapLength = 20
counter = 1
everyGap = np.zeros(10)
flag = np.zeros((3,100))

fileAddress = ""
totalCounter = 0
totalGap = np.zeros((3,6))
FREANDBAND = [(600, 50), (600, 100), (600, 200), (600, 400),
              (2200, 50), (2200, 100), (2200, 200), (2200, 400), (2200, 800), (2200, 1600),
              (4400, 50), (4400, 100), (4400, 200), (4400, 400), (4400, 800), (4400, 1600)]
