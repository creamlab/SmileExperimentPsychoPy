from psychopy import visual, core, event, visual #import some libraries from PsychoPy

class Button(object):
	def __init__(self, pos = (0,0), ImageName = "", ClickedImage = "", win = None , size = 1):
		self.pos 				= pos 
		self.Image  			= ImageName
		self.ClickedImage  		= ClickedImage
		self.win 				= win
		self.size				= size

		self.ImgContainer 		= visual.ImageStim(self.win, image = self.Image, mask = None, units = '', pos = self.pos)
		self.ImgContainer.setSize(self.size)


	def Clicked(self, ClickPos):
		if self.ImgContainer.contains( ClickPos ):
			#self.ImgContainer = visual.ImageStim(self.win, image = self.ClickedImage, mask = None, units = '', pos = self.pos)
			#self.ImgContainer.setSize(self.size)
			#self.ImgContainer.draw(self.win)
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

