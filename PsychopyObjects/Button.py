from psychopy import visual, core, event, visual #import some libraries from PsychoPy

class Button(object):
	def __init__(self, pos = (0,0), Image = "", ClickedImage = "", win = None , size = 1):
		self.pos 				= pos 
		self.Image  			= Image
		self.ClickedImage  		= ClickedImage
		self.win 				= win
		self.size				= size

		self.ImgContainer 		= visual.ImageStim(self.win, image = self.Image, mask = None, units = '', pos = self.pos)
		self.ImgContainer.setSize(self.size)


	def Clicked(self, ClickPos):
		if self.ImgContainer.contains( ClickPos ):
			return True
		else :
			return False

	#Setters :
	def SetImgName(self, Fname):
		self.PlayImage = Fname

	def SetClickedImageName(self, Fname):
		self.StopImage = Fname

	def SetPos(self, pos):
		self.pos = pos

