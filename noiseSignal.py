"""========================================
Generate and play band-limited signal
========================================"""

# Copyright (c) Nov. 2017
# All rights reserved.

import os
import wave
import random
import pyaudio
import numpy as np
import sounddevice as sd
import constant as CONST
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real


def band_limited_noise(highFreq, bandWidth, timeLength, samplerate=44100):
    minFreq = highFreq - bandWidth
    timeLength = timeLength / 1000
    samples = int(timeLength*samplerate)
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=minFreq, freqs<=highFreq))[0]
    f[idx] = 1
    return fftnoise(f)


# Generate the band-limited noise (ms)
def genNoise(bandWidth, highFreq, audioLength, samplerate=44100):
    x = band_limited_noise(bandWidth, highFreq, audioLength, samplerate)
    # Amplitude normalization
    #audioFile = np.int16(MaxMinNorma(x) * (10**3))
    audioFile = MaxMinNorma(x)
    return audioFile


# Add gap to the audio-(ms)
def addGap(waveFile, gapLength, gapOrigin=400, samplerate=44100):
    copyData = waveFile.copy()
    originPoint    = int(gapOrigin * samplerate/1000)
    gapLengthPoint = int(gapLength * samplerate/1000)
    copyData[originPoint:(originPoint + gapLengthPoint + 1)] = 0
    #return np.int16(waveFile)
    return copyData


def syntheticAudio(highFreq, bandWidth, gapLength, audioLength=800, gapOrigin=400, samplerate=44100):
    lengthOf200ms = int(200 * samplerate/1000)
    gapZeros = np.zeros(lengthOf200ms)
    noneGapData = noise3(highFreq, bandWidth)
    #noneGapData = band_limited_noise(highFreq, bandWidth, timeLength = 800, samplerate=44100)
    gapData = addGap(noneGapData, gapLength, gapOrigin, samplerate)

    # Random splicing
    CONST.RandomNum = random.randint(1, 3)
    print("Correct number is:", CONST.RandomNum)
    if CONST.RandomNum == 1:
        synAudioData = np.concatenate((gapData, gapZeros, noneGapData, gapZeros, noneGapData), axis=0)
    elif CONST.RandomNum == 2:
        synAudioData = np.concatenate((noneGapData, gapZeros, gapData, gapZeros, noneGapData), axis=0)
    else:
        synAudioData = np.concatenate((noneGapData, gapZeros, noneGapData, gapZeros, gapData), axis=0)

    return noneGapData, gapData, synAudioData


# Save audio files, "fileName":"test.wave"
def saveAudio(waveFile, fileAddress, nchannels=1, sampwidth=2, framerate=44100):
    f = wave.open(fileAddress, "wb")
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)
    # Convert data to binary file
    f.writeframes(waveFile.tostring())
    f.close()


def playSound(fileAddress, highFreq, bandWidth, gapLength):
    noneGapData, gapData, synAudioData = syntheticAudio(highFreq, bandWidth, gapLength)
    synAudioAdd = os.path.join(fileAddress, "F%sB%sG%.2fSyn.wav"%(highFreq, bandWidth, CONST.gapLength))
    saveAudio(noneGapData, os.path.join(fileAddress, "F%sB%sG%.2fNoneGap.wav"%(highFreq, bandWidth, CONST.gapLength)))
    saveAudio(gapData, os.path.join(fileAddress, "F%sB%sG%.2fGap.wav"%(highFreq, bandWidth, CONST.gapLength)))
    saveAudio(synAudioData, synAudioAdd)

    wf = wave.open(synAudioAdd, 'rb')
    chunk = wf.getnframes()
    p = pyaudio.PyAudio()

    # Turn on the sound output stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # Write audio to the sound card to play
    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    # Stop stream and close PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Play Sound Finished!")


def noise(highFreq, bandwidth, soundLength=800, fs=44100):
    minFreq = highFreq - bandwidth
    soundLength /= 1000
    s_array = np.arange(fs * soundLength)
    myarray = np.zeros_like(s_array)

    for fre in np.arange(minFreq, highFreq + 1, 1):
        phi = np.random.random() * 2 * np.pi
        s_array2 = np.sin(2 * np.pi * fre * s_array / fs + phi)
        myarray = myarray + s_array2
    myarray2 = myarray / np.max(myarray)
    return myarray2


def noise2(highFreq, bandwidth, soundLength=800, fs=44100):
    minFreq = highFreq - bandwidth
    soundLength /= 1000
    gauData = np.random.randn(1, int(fs * soundLength))[0]
    data2 = butter_bandpass_filter(gauData, lowcut=minFreq, highcut=highFreq, fs=44100, order=4)
    data3 = data2 / np.max(data2)
    return data3


def noise3(highFreq, bandwidth, soundLength=800, fs=44100):
    minFreq = highFreq - bandwidth
    fs = 44100  # Hz
    f = (highFreq + minFreq)/2  # Hz
    soundLength = soundLength/1000
    myarray1 = np.arange(fs * soundLength)
    myarray = np.sin(2 * np.pi * f * myarray1 / fs)

    return myarray


def playAudio(highFreq, bandWidth, gapLength, samplerate=44100):
    noneGapData, gapData, synAudioData = syntheticAudio(highFreq, bandWidth, gapLength)
    synAudioAdd = os.path.join(fileAddress, "F%sB%sG%.2fSyn.wav"%(highFreq, bandWidth, CONST.gapLength))
    #saveAudio(noneGapData, os.path.join(fileAddress, "F%sB%sG%.2fNoneGap.wav"%(highFreq, bandWidth, CONST.gapLength)))
    #saveAudio(gapData, os.path.join(fileAddress, "F%sB%sG%.2fGap.wav"%(highFreq, bandWidth, CONST.gapLength)))
    #saveAudio(synAudioData, synAudioAdd)
    sd.play(synAudioData, samplerate)


def genSound(highFreq, bandWidth, soundLength, fs = 44100):
    minFreq = highFreq - bandWidth
    soundLength /= soundLength
    s_array = np.arange(fs * soundLength)
    myarray = np.zeros_like(s_array)

    for fre in np.arange(minFreq, highFreq+1, 1):
        s_array = np.sin(2 * np.pi * fre / fs * s_array)
        myarray += s_array

    myarray = myarray/myarray.shape[0]
