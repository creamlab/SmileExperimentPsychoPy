from psychopy import visual, core, event, visual #import some libraries from PsychoPy

class Slider(object):

	def __init__(self, pos = (0,0), height = 0.2, width = 0.2,  size = 1, LeftText = "", RighText = "", win = None):
		self.pos 		= pos 
		self.size 		= size 
		self.width 		= width
		self.height 	= height
		self.fillPos 	= self.width / 2
		self.win 		= win
		self.rect 		= visual.Rect(self.win,
                			height = self.height, width = self.width, pos = self.pos,
                			fillColor='black'
            			)

		self.arrow_r 	= 'experiment data/pics/arrow_r.png'
		self.arrow_l 	= 'experiment data/pics/arrow_l.png'
		self.arrow_h 	= 30
		self.arrow_w 	= 30

		ImgContainerL 	= None
		ImgContainerR 	= None

	def Draw(self):
		
		self.rect.draw()
		
		Left_pos		  	= (self.pos[0] - self.width/2, self.pos[1]) 
		self.ImgContainerL 	= visual.ImageStim(self.win, image = self.arrow_l, mask = None, units = '', pos = Left_pos )
		
		Right_pos		  	= (self.pos[0] + self.width/2, self.pos[1]) 
		self.ImgContainerR 	= visual.ImageStim(self.win, image = self.arrow_r, mask = None, units = '', pos = Right_pos )

		self.ImgContainerL.setSize(self.size)
		self.ImgContainerR.setSize(self.size)
		
		self.ImgContainerL.draw(self.win)
		self.ImgContainerR.draw(self.win)
		#self.rect.fillColorSpace()

	def Clicked(self, ClickPos):
		if self.ImgContainer.contains( ClickPos ):
			return True
		else :
			return False

	#Setters : 	
	def SetImgName(self, pos):
		self.pos = pos

	def SetClickedImageName(self, size):
		self.size = size

	def SetWidth(self, width):
		self.width = width

	def SetHeight(self, height):
		self.height = height

	def SetFillPos(self, fillPos):
		self.fillPos = fillPos
		