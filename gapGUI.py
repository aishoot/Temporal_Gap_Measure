"""========================================
Generate the GUI of the experiment
========================================"""

import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import constant as CONST
import audioPlot as aPlot
import noiseSignal as gNoise
import matplotlib.pyplot as plt


class GapDectionGUI:
    def __init__(self, mainWindow):
        curWidth = 700
        curHeight = 450
        mainWindow.title("Temporal Gap Detection")
        mainWindow.resizable(False, False)
        mainWindow.update()
        scnWidth, scnHeight = mainWindow.maxsize()  # Get screen width and height
        mainWindowX = (scnWidth-curWidth)/2
        mainWindowY = (scnHeight-curHeight)/2
        winSize = '%dx%d+%d+%d'%(curWidth, curHeight, mainWindowX, mainWindowY)
        mainWindow.geometry(winSize)

        highFreValue = tk.StringVar()
        highFreValue.set("600Hz")
        bandWidthValue = tk.StringVar()
        bandWidthValue.set("50Hz")
        judgeResult = tk.StringVar()
        name = tk.StringVar()

        # Define operation
        def buttonJudge(n):
            CONST.ClickNum = n
            #print(CONST.ClickNum, CONST.RandomNum)
            if CONST.ClickNum == CONST.RandomNum:  # Corret 2 times
                CONST.correctNum += 1
                if CONST.correctNum == 2:
                    judgeResult.set("Correct!")
                    CONST.flag[0][CONST.counter] = CONST.gapLength
                    CONST.flag[1][CONST.counter] = 1
                    CONST.counter += 1
                    CONST.gapLength = CONST.gapLength / 1.4  # Correct down
                    CONST.correctNum = 0
                else:
                    judgeResult.set("Correct!\nOnce again!")
            else:
                judgeResult.set("False!")
                CONST.flag[0][CONST.counter] = CONST.gapLength
                CONST.flag[1][CONST.counter] = 0
                CONST.correctNum = 0
                CONST.counter += 1
                CONST.gapLength = CONST.gapLength * 1.4  # False up

            if CONST.correctNum != 1:
                highFreq, bandWidths = CONST.FREANDBAND[CONST.totalCounter]
                symbol = (CONST.flag[1][CONST.counter-1] - CONST.flag[1][CONST.counter-2]) and (CONST.counter > 2)
                if symbol ==1:  # Determine whether it is a turning point
                    CONST.everyGap[CONST.turningNum] = CONST.flag[0][CONST.counter-1]
                    CONST.turningNum += 1
                if CONST.turningNum == 10:
                    saveData = CONST.flag[0:2, 1:CONST.counter]
                    averageGap = np.mean(CONST.everyGap[-6:])
                    messagebox.showinfo('END', "%s's average gap is %.2fms.\nNext batch of data."%(name.get(), averageGap))

                    print("Average Gap:%s."%averageGap)
                    pd.DataFrame(CONST.totalGap).to_csv(os.path.join(CONST.fileAddress, "%sAllGap.csv")%(CONST.totalCounter))
                    pd.DataFrame(saveData).to_csv(os.path.join(CONST.fileAddress, "F%sB%s.csv"%(highFreq, bandWidths)))
                    if highFreq == 600:
                        CONST.totalGap[0, CONST.totalCounter] = averageGap
                    elif highFreq == 2200:
                        CONST.totalGap[1, CONST.totalCounter - 4] = averageGap
                    elif highFreq == 4400:
                        CONST.totalGap[2, CONST.totalCounter - 10] = averageGap

                    CONST.totalCounter += 1
                    CONST.counter = 1
                    CONST.turningNum = 0
                    CONST.gapLength = 20
                    CONST.everyGap = np.zeros(10)
                    CONST.flag = np.zeros((3, 100))

            btnOne['state']   = 'disabled'
            btnTwo['state']   = 'disabled'
            btnThree['state'] = 'disabled'


        def funStart():
            nameStr = name.get()
            if nameStr!="":
                print(nameStr)
                nameString['state'] = 'readonly'
                if not os.path.exists(nameStr):
                    os.makedirs(nameStr)
                CONST.fileAddress = os.path.join(os.getcwd(), nameStr)
                btnStart['state'] = 'disabled'
            else:
                messagebox.showinfo('Warning', "\nPlease Input Your Name!")
                print("Your name is empty!")


        def funNext():
            if CONST.totalCounter >= 16:  # Complete the experiment
                judgeResult.set("")
                btnOne['state'] = 'disabled'
                btnTwo['state'] = 'disabled'
                btnThree['state'] = 'disabled'
                btnNext['state'] = 'disabled'
                messagebox.showinfo('Experiment END!', "\nClose the experiment window!")

                aPlot.totalGapPlot(CONST.totalGap)
                pd.DataFrame(CONST.totalGap).to_csv(os.path.join(CONST.fileAddress, "allGapValues.csv" ))
                print("Experiments is finished!")

            # Clear the results
            judgeResult.set("")
            btnOne['state'] = 'normal'
            btnTwo['state'] = 'normal'
            btnThree['state'] = 'normal'

            highFreq, bandWidths = CONST.FREANDBAND[CONST.totalCounter]
            highFreValue.set(str(highFreq) + "Hz")
            bandWidthValue.set(str(bandWidths) + "Hz")

            # Play the first sound
            #gNoise.playSound(CONST.fileAddress, highFreq, bandWidths, CONST.gapLength)
            print("Gap Length is:", CONST.gapLength)
            # Start playing sound
            gNoise.playAudio(highFreq, bandWidths, CONST.gapLength)
            print("Play Sound Finished!\n")

        # Three labels: highFrequency, bandwidth, judgeResult
        highFreTitle = tk.Label(mainWindow, text="HighFre")
        highFreTitle.place(relx=0.01, rely=0.01)
        highFre = tk.Label(mainWindow, textvariable=highFreValue, relief="ridge")
        highFre.place(relx=0.01, rely=0.05)
        bandWidthTitle = tk.Label(mainWindow, text="BandWidth")
        bandWidthTitle.place(relx=0.10, rely=0.01)
        bandWidth = tk.Label(mainWindow, textvariable=bandWidthValue, relief="ridge")
        bandWidth.place(relx=0.10, rely=0.05)
        nameTitle = tk.Label(mainWindow, text="Your Name")
        nameTitle.place(relx=0.85, rely=0.01)
        nameString = tk.Entry(mainWindow, text=name, width=9, textvariable=name)
        nameString.place(relx=0.85, rely=0.05)

        projectTitle = tk.Label(mainWindow, text="Temporal Gap Detection Experiment", fg='red', font=("Times New Roman", 18))
        projectTitle.place(relx=0.20, rely=0.25)

        btnOne  = tk.Button(mainWindow, text="Sound One", width=9, height=2,command=lambda:buttonJudge(1), font=("Times New Roman", 12))
        btnOne.place(relx=0.20, rely=0.45)
        btnTwo  = tk.Button(mainWindow, text="Sound Two", width=9, height=2,command=lambda:buttonJudge(2), font=("Times New Roman", 12))
        btnTwo.place(relx=0.41, rely=0.45)
        btnThree = tk.Button(mainWindow, text="Sound Three", width=9, height=2, command=lambda:buttonJudge(3), font=("Times New Roman", 12))
        btnThree.place(relx=0.62, rely=0.45)

        btnStart = tk.Button(mainWindow, text="Start", width=6, height=2, font=("Times New Roman", 12), command=funStart)
        btnStart.place(relx=0.25, rely=0.68)
        highFreTitle = tk.Label(mainWindow, textvariable=judgeResult)
        highFreTitle.place(relx=0.44, rely=0.72)
        btnNext = tk.Button(mainWindow, text="Next", width=6, height=2, font=("Times New Roman", 12), command=funNext)
        btnNext.place(relx=0.60, rely=0.68)

        textName = "* Yufan Du, Chao Peng\nNovember 2017\nAuditory Information Processing"
        inscribeName = tk.Label(mainWindow, text= textName, font=("Times New Roman", 10))
        inscribeName.place(relx=0.64, rely=0.86)