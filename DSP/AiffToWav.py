import glob
from scipy.io.wavfile import read, write
from scikits.audiolab import aiffread, wavwrite  # scipy.io.wavfile can't read 24-bit WAV
import aifc
import numpy as np
from numpy import pi, polymul
import os


def AifToWav(FolderName):
	"""
	Convert all .aiff files in FolderName to .wav and put it in 
	"""
	for file in glob.glob(FolderName + "/*.aiff"): # Wav Files
		x, fs, enc 	= aiffread(str(file))
		WavFileName = os.path.splitext(str(file))[0] + ".wav"
		wavwrite(x, WavFileName, fs, enc='pcm24')

		print WavFileName