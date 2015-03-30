from pyo import *
from scipy.io.wavfile import read, write
import glob
import os
from scipy import io
from numpy import linspace

def playFileWithEq( boo, fr, Q):
	s = Server().boot()
	s.start()

	FName = "experiment data/Sounds For Stimuli/C1.wav"
	sf 	  = SfPlayer(FName, speed = 1, loop=False)
	trig  = TrigRand(sf['trig'])

	eq    = EQ(sf, freq=fr, q=Q, boost=boo, type=0)

	eq = eq.mix(2)
	eq.out()

	while trig.get() == 0:
		continue
	s.stop()

def PeakFilterWavFiles( boo, fr, Q):
	#Eq parameters
	# fr : float or PyoObject, optional. Cutoff or center frequency of the filter. Defaults to 1000.
	# Gain, expressed in dB, to add or remove at the center frequency. Default to -3.
	# Q of the filter, defined as freq/bandwidth. float or PyoObject, optional

	s = Server(duplex=0, audio="offline").boot()

	# output folder
	recpath = os.path.join(os.path.expanduser("~"), "Desktop/Cream/Experiments/SmileExperimentPsychoPy/experiment data", "SoundsForExperiment")
	if not os.path.isdir(recpath):
		os.mkdir(recpath)


	#Input folder
	for file in glob.glob("experiment data/Sounds For Stimuli/*.wav"): # Wav Files
		SplitPath = os.path.split(file) # Separate path in list 
		s.boot()
		name = SplitPath[-1] # Get the last item of list in order to have the audio file name

		duration = sndinfo(file)[1]
		s.recordOptions(dur = duration + 0.1, filename = os.path.join(recpath, str(boo) + "_" + name), fileformat=0, sampletype=0)
		
		FName = str(file)
		sf 	  = SfPlayer(FName, speed = 1, loop = False)
		eq    = EQ(sf, freq=fr, q=Q, boost=boo, type=0)
		eq = eq.mix(2)
		eq.out()

		s.start()
		s.shutdown()

def RisingPeakFilterInWavFiles(Start, Stop, fr, Q):
	#Start and stop boost in db
	#fr : Frquency
	#Q of the filter, defined as freq/bandwidth. Should be between 1 and 500. Defaults to 1.
	#The more the Q, the less bandwith

	s = Server(duplex=0, audio="offline").boot()

	# output folder
	recpath = os.getcwd()+"/experiment data/Rising Eq Sounds"
	if not os.path.isdir(recpath):
		os.mkdir(recpath)

	#Input folder
	os.chdir("experiment data/Sounds For Stimuli")
	for file in glob.glob("*.wav"): # Wav Files
		s.boot()
		name = str(file)

		duration = sndinfo(file)[1] + 0.1
		s.recordOptions(dur = duration, filename=os.path.join(recpath, "Rising" + str(file)), fileformat = 0, sampletype = 0)
		
		#Shape Ramp
		boo = - LFO( freq = 1 / (2 * float(duration) ) , sharp = 1, type = 1)
		

		#boo = Fader(0.3, 0.5, duration, 1)
		Delta = abs(Start - Stop)
		boo = (Delta * boo) + Start
		
		sf = SfPlayer(file, speed = 1, loop=False)
		eq = EQ(sf, freq = fr, q = Q, boost = boo, type = 0)
		a  = eq.mix(2).out()

		s.start()
		s.shutdown()

def GeneratePinkNoiseFile():
	s = Server(duplex=0, audio="offline").boot()

	# output folder
	recpath = os.path.join(os.path.expanduser("~"), os.getcwd()+"/experiment data", "Sounds For Stimuli")
	if not os.path.isdir(recpath):
		os.mkdir(recpath)

	s.boot()
	duration = 10
	name = "Pn.wav"
	s.recordOptions(dur = duration + 0.1, filename=os.path.join(recpath, name), fileformat=0, sampletype=0)
	a = PinkNoise(.1).mix(2).out()
	s.start()
	s.shutdown()


#GeneratePinkNoiseFile()

ListOfboosts = [ -15 ,-10 , -5, 0, 5, 10, 15]
fr    = 3000
Q 	  = 0.4
for boost in ListOfboosts:
	PeakFilterWavFiles(boost, fr, Q)

#playFileWithEq(boo, fr, Q)
#RisingPeakFilterInWavFiles(Start = -5, Stop = 10, fr = 3000, Q = 2)