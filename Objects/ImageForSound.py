from psychopy import visual, core, event, visual #import some libraries from PsychoPy
from pyo import *
from Button import Button 

class ImageForSound(Button):
	
	def __init__(self, pos = (0,0), ImageName = "", ClickedImage = "", win = None, size = 1,  SoundName = "" ):
		
		Button.__init__(self
						, pos 			= pos
						, ImageName 	= ImageName
						, ClickedImage 	= ClickedImage
						, win 			= win
						, size 			= size
						)
		
		self.sound = SoundName


	def Clicked(self, ClickPos, s):
		if super(ImageForSound, self).Clicked(ClickPos):
			sf 	  	= SfPlayer(self.sound, speed = 1, loop=False)
			trig 	= TrigRand(sf['trig'])
			a 		= sf.mix(2).out()
			

			while trig.get() == 0:
				continue
			return True

		else:

			return False

	#Setters :
	def SetSound(self, Fname):
		self.sound = Fname