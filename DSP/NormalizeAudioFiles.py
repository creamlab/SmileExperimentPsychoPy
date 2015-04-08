#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from scipy.signal import lfilter
import numpy as np
from scikits.audiolab import wavread, wavwrite  # scipy.io.wavfile can't read 24-bit WAV
import glob
import os
from numpy import pi, polymul
from scipy.signal import bilinear
 
def Lin2db(Lin):
	return 20*np.log10(Lin)

def MaxWindowRms( a, WndSize):
 	"""
 	Return the root mean square of all the elements of *a*, flattened out.
 	"""
 	i = 0
 	RmsLevel = -1
 	while i + WndSize < len(a):
 		DataArray = a[i: i + WndSize]
 		NewRms = np.sqrt(np.mean(np.absolute(DataArray)**2))
		RmsLevel = max(RmsLevel, NewRms)

		i = WndSize + i
 	return RmsLevel



def rms_flat(a):  # from matplotlib.mlab
	"""
	Return the root mean square of all the elements of *a*, flattened out.
	"""
	return np.sqrt(np.mean(np.absolute(a)**2))

def A_weighting(fs):
    """Design of an A-weighting filter.

    b, a = A_weighting(fs) designs a digital A-weighting filter for
    sampling frequency `fs`. Usage: y = scipy.signal.lfilter(b, a, x).
    Warning: `fs` should normally be higher than 20 kHz. For example,
    fs = 48000 yields a class 1-compliant filter.

    References:
       [1] IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.

    """
    # Definition of analog A-weighting filter according to IEC/CD 1672.
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997
    
    NUMs = [(2*pi * f4)**2 * (10**(A1000/20)), 0, 0, 0, 0]
    DENs = polymul([1, 4*pi * f4, (2*pi * f4)**2],
                   [1, 4*pi * f1, (2*pi * f1)**2])
    DENs = polymul(polymul(DENs, [1, 2*pi * f3]),
                                 [1, 2*pi * f2])
    
    # Use the bilinear transformation to get the digital filter.
    # (Octave, MATLAB, and PyLab disagree about Fs vs 1/Fs)
    return bilinear(NUMs, DENs, fs)

def NormalizeAllSoundsInFolder(Path):
	WindowSize = 32000
	Old, New = [], []

	ListOfWeightedRms = []
	for file in glob.glob("experiment data/SoundsForExperiment/*.wav"): 
		x, fs, bits = wavread(str(file))
		b, a 		= A_weighting(fs)
		x 			= lfilter(b, a, x)
		ListOfWeightedRms.append(MaxWindowRms(x, WindowSize))

	WeightRmsRef = min(ListOfWeightedRms)

	Precision = 0.9 #Signal Multiplication factor
	for file in glob.glob("experiment data/SoundsForExperiment/*.wav"):
		x, y = [], []
		x, fs, bits = wavread(str(file))

		#For print
		print "Fichier en traitement : "+ str(str(file))
		b, a = A_weighting(fs)
		y 	= lfilter(b, a, x)
		Old.append(Lin2db(MaxWindowRms(y, WindowSize)))

		b, a 		= A_weighting(fs)
		y 	 		= lfilter(b, a, x)
		WeightedRms = MaxWindowRms(y, WindowSize)
		
		while WeightedRms  > WeightRmsRef :
			x 		= x * Precision
			b, a 	= A_weighting(fs)
			y 		= lfilter(b, a, x)
			WeightedRms = MaxWindowRms(y, WindowSize)

		wavwrite(x, str(file), fs=fs)

		#For print
		b, a = A_weighting(fs)
		y 	= lfilter(b, a, x)
		New.append(Lin2db(MaxWindowRms(y, WindowSize)))
		#New.append(Lin2db(rms_flat(y)))

	for i in range(0,len(Old)):
		print "Weighting before norm :" + str(Old[i]) + " Weighting after norm :"  + str(New[i])









