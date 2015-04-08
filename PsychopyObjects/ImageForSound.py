from psychopy import visual, core, event, visual #import some libraries from PsychoPy
from pyo import *
from Button import Button 

class ImageForSound(Button):
	
	def __init__(self, pos = (0,0), Image = "", ClickedImage = "", win = None, size = 1,  SoundName = "" ):
		
		Button.__init__(self
						, pos 			= pos
						, Image 		= Image
						, ClickedImage 	= ClickedImage
						, win 			= win
						, size 			= size
						)
		
		self.sound 	= SoundName
		self.sf = None


	def Clicked(self, ClickPos, s):
		if super(ImageForSound, self).Clicked(ClickPos):

			self.sf = SfPlayer(self.sound, speed = 1, loop=False)
			trig 	= TrigRand(self.sf['trig'])
			a = self.sf.mix(2).out()

			#Change image
			self.ImgContainer.autoDraw = False
			self.ImgContainer 		= visual.ImageStim(self.win, image = self.ClickedImage, mask = None, units = '', pos = self.pos)

			self.ImgContainer.draw()
			self.win.flip()

			#Wait untill sound is played
		
		
			while trig.get() == 0:
				continue

			self.ImgContainer = visual.ImageStim(self.win, image = self.Image, mask = None, units = '', pos = self.pos)
			self.ImgContainer.setSize(self.size)
			self.ImgContainer.draw()
			self.win.flip()
			self.ImgContainer.autoDraw = True
				

	#Setters :
	def SetSound(self, Fname):
		self.sound = Fname
