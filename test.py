<<<<<<< HEAD
from pylab import plot, show, title, xlabel, ylabel, subplot, savefig, grid, specgram, suptitle, yscale
from scipy import fft, arange, ifft, io
from numpy import sin, linspace, pi, cos, sin, random, array
#import numpy as np
#from scipy.io.wavfile import read, write
from matplotlib import pyplot

def plotCosAndSin():
	X = linspace(-pi, pi, 256, endpoint=True)
	C, S = cos(X), sin(X)
	plot(X, C)
	plot(X, S)
	show()

def Normalize(data):
	Max = max(data)
   	data = [x / Max for x in data]
   	return data

def WhiteNoiseGenerator(Duration, Fs):
	#t    = linspace(0, Duration, Duration * Fs, endpoint=True)
	data = []
	data = random.normal(0, 0.5, Duration*Fs)
	data = Normalize(data)
	return data

def Ramp(freq, Duration, Fs):
	Data = []
	Ramp = []
	DureeRamp = float(1)/freq
	Ramp = linspace(0, DureeRamp , DureeRamp*Fs, endpoint=True)
 	while len(Data) < Duration*Fs:
		Data.extend(Ramp)	
	Data = Data[0:Duration*Fs]	
	Data = Normalize(Data)
	return Data

def Triangle(freq, Duration, Fs):
	Data, Ramp = [], []
	DureeRamp = float(1)/freq
	UpRamp 	 = linspace(0, DureeRamp , (DureeRamp*Fs/2))
 	DownRamp = linspace(DureeRamp, 0 , (DureeRamp*Fs/2))
	
 	Ramp.extend(UpRamp)
	Ramp.extend(DownRamp)

 	while len(Data) < Duration*Fs:
		Data.extend(Ramp)	

	Data = Data[0:Duration*Fs]	
	Data = Normalize(Data)
	return Data

def Sin(freq, Duration, Fs):
	t    = linspace(0, Duration , Duration * Fs, endpoint=True)
	data = sin(2*pi*freq*t)
	return data

def Cos(freq, Duration, Fs):
	t    = linspace(0, Duration , Duration * Fs, endpoint=True)
	data = cos(2*pi*freq*t)
	return data

def SquareWave(freq, Duration, Fs):
	t    = linspace(0, Duration, Duration * Fs, endpoint=True)
	Data = []
	SamplesPerPeriod = Fs/ freq 
	for i in range(0, len(t)):
		if (i % SamplesPerPeriod) < SamplesPerPeriod/2 :
			Data.append(1.0)
		else :
			Data.append(0.0)
	return Data

def PlotPSForWavFile(name, Duration):
	"""
	Plot Power Spectrum of wave File
	"""
	rate, data = io.wavfile.read(name)
	#Data = data[0:Duration*rate]
	plotPS(data, rate)


def plotPS(data, Fs):
	"""
	Plot Power Spectrum of data
	"""
	y 	 = data
	timp = len(y)/Fs
	t 	 = linspace(0,timp,len(y))

	pyplot.subplot(2,1,1)
	pyplot.plot(t,y)
	pyplot.xlabel('Time')
	pyplot.ylabel('Amplitude')
	pyplot.subplot(2,1,2)

	n 	= len(y)
	k 	= arange(n)
	T 	= n/Fs
	frq = k/T # two sides frequency range
	frq = frq[range(n/2)] # one side frequency range
 	Y 	= fft(y)/n # fft computing and normalization
 	Y 	= Y[range(n/2)]
 	
	pyplot.xscale('log')
	pyplot.plot(frq, abs(Y),'r') # plotting the spectrum
	pyplot.xlabel('Freq (Hz)')
	pyplot.ylabel('|Y(f)|')

	show()

def PlotSpecGram(FileName):	
	rate, data = io.wavfile.read(FileName)
	Pxx, freqs, bins, im = specgram(data, NFFT=512, Fs=rate, noverlap=10)
	xlabel('Time (s)')
	ylabel('|Y(freq)|')
	suptitle('Spectrogram', fontsize=15)
	grid()
	show()

def PlotSpecGram(rate, data):	
	Pxx, freqs, bins, im = specgram(data, NFFT=512, Fs=rate, noverlap=10)
	xlabel('Time (s)')
	ylabel('|Y(freq)|')
	suptitle('Spectrogram', fontsize=15)
	yscale('symlog')
	grid()
	show()

def ComputeLoudness(Data, BufferSize, Fs): 
	# TODO :  not finished!
	Y 			= []
	Loudness 	= []
	for i in range(0, len(Data)/BufferSize):
		pos = i*BufferSize
		if len(Data) < (pos + BufferSize):
			EndChunk = len(Data)
		else :
			EndChunk = pos + BufferSize

		y 		= Data[pos : EndChunk ]
		n 		= len(y)
		k 		= arange(n)
		T 		= n/Fs
		frq 	= k/T # two sides frequency range
		frq 	= frq[range(n/2)] # one side frequency range
	 	Y 	 	= fft(y)/n # fft computing and normalization
	 	Y 		= Y[range(n/2)]
	 	Loudness.append(sum(abs(Y)))
	return Loudness

def BellFilter(FileName, Q, f, gain):
	rate, data = io.wavfile.read(FileName)
	Data = data[0:Duration*rate]


print 'hello'
=======
#! /usr/bin/env python_32
"""measure your JND in orientation using a staircase method"""

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import time, numpy, random

try:#try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:#if not there then use a default set
    expInfo = {'observer':'jwp', 'refOrientation':0}
expInfo['dateStr']= data.getDateStr() #add the current time
#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='simple JND Exp', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo)#save params to file for next time
else:
    core.quit()#the user hit cancel so exit

#make a text file to save data
fileName = expInfo['observer'] + expInfo['dateStr']
dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
dataFile.write('targetSide,oriIncrement,correct\n')

#create the staircase handler
staircase = data.StairHandler(startVal = 20.0,
                          stepType = 'db', stepSizes=[8,4,4,2,2,1,1],
                          nUp=1, nDown=3,  #will home in on the 80% threshold
                          nTrials=1)

#create window and stimuli
win = visual.Window([800,600],allowGUI=True, monitor='testMonitor', units='deg')
foil = visual.GratingStim(win, sf=1, size=4, mask='gauss', ori=expInfo['refOrientation'])
target = visual.GratingStim(win, sf=1, size=4, mask='gauss', ori=expInfo['refOrientation'])
fixation = visual.GratingStim(win, color=-1, colorSpace='rgb', tex=None, mask='circle',size=0.2)
#and some handy clocks to keep track of time
globalClock = core.Clock()
trialClock = core.Clock()

#display instructions and wait
message1 = visual.TextStim(win, pos=[0,+3],text='Hit a key when ready.')
message2 = visual.TextStim(win, pos=[0,-3],
    text="Then press left or right to identify the %.1f deg probe." %expInfo['refOrientation'])
message1.draw()
message2.draw()
fixation.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()

for thisIncrement in staircase: #will step through the staircase
    #set location of stimuli
    targetSide= random.choice([-1,1]) #will be either +1(right) or -1(left)
    foil.setPos([-5*targetSide, 0])
    target.setPos([5*targetSide, 0]) #in other location

    #set orientation of probe
    foil.setOri(expInfo['refOrientation'] + thisIncrement)

    #draw all stimuli
    foil.draw()
    target.draw()
    fixation.draw()
    win.flip()

    core.wait(0.5) #wait 500ms; but use a loop of x frames for more accurate timing in fullscreen
                              # eg, to get 30 frames: for f in xrange(30): win.flip()
    #blank screen
    fixation.draw()
    win.flip()

    #get response
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='left':
                if targetSide==-1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey=='right':
                if targetSide== 1: thisResp = 1#correct
                else: thisResp = -1             #incorrect
            elif thisKey in ['q', 'escape']:
                core.quit() #abort experiment
        event.clearEvents() #must clear other (eg mouse) events - they clog the buffer

    #add the data to the staircase so it can calculate the next level
    staircase.addData(thisResp)
    dataFile.write('%i,%.3f,%i\n' %(targetSide, thisIncrement, thisResp))
    core.wait(1)

#staircase has ended
dataFile.close()
staircase.saveAsPickle(fileName) #special python binary file to save all the info

#give some output to user in the command line in the output window
print 'reversals:'
print staircase.reversalIntensities
print 'mean of final 6 reversals = %.3f' %(numpy.average(staircase.reversalIntensities[-6:]))

#give some on screen feedback
feedback1 = visual.TextStim(win, pos=[0,+3],
    text='mean of final 6 reversals = %.3f' %
(numpy.average(staircase.reversalIntensities[-6:])))
feedback1.draw()
fixation.draw()
win.flip()
event.waitKeys() #wait for participant to respond

win.close()
core.quit()
>>>>>>> 06dda0bedf03862f882569797c8c53e4e08a7072
