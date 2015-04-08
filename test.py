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
