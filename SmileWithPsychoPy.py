from psychopy import visual, core, event, visual #import some libraries from PsychoPy
from ImageForSound import *
from Button import *
from Slider import *

class SmileExperiment:
 	def __init__(self):
		self.win 		= visual.Window(size=(1280, 800), pos=None, color=(255, 255, 255))

		self.mouse 		= event.Mouse(visible = True, newPos = False, win = self.win)
		self.trialClock = core.Clock()
		self.expClock 	= core.Clock()
		self.clickGap 	= .1 #seconds

		self.S1 = ImageForSound(	pos 		= ( -0.3, 0.7)
							, ImageName 		= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win 				= self.win
							, size 				= 0.3
							, SoundName 		= "experiment data/sounds/C1.wav"
							) 

		self.S2 = ImageForSound(	pos 		= (+0.3, 0.7)
							, ImageName 		= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win 				= self.win
							, size 				= 0.3
							, SoundName 		= "experiment data/sounds/C1.wav"
							) 


		self.ContinueButton	= Button( pos 		= (0, -0.5)
							, ImageName 		= "experiment data/pics/next.png"
							, ClickedImage	 	= "experiment data/pics/next_press.png"
							, win 				= self.win
							, size 				= 0.3
							) 

		self.Slider 		= Slider(pos = (0,0), height = 0.1, width = 1.3, size = 0.2, LeftText = "", RighText = "", win = self.win)


		self.s 			= Server().boot() #Audio Server
		self.s.start()


	# Mouse Functions
	def MouseClick(self):
		c, c_old 	= (0,0)
		while True :
			any_press 	= self.mouse.getPressed()
			c 			= self.trialClock.getTime()
			b1_press 	= any_press[0]	
			if b1_press and c - c_old > self.clickGap:
				c_old = c
				return self.mouse.getPos()

    # Display Functions
	def generateDisplay(self):
		self.S1.Draw()	
		self.S2.Draw()	
		self.ContinueButton.Draw()
		self.Slider.Draw()
		self.win.flip()

	def TextStimuli(self, Fname, duration):
		with open (Fname, "r") as myfile:
			IntroductionText = myfile.read().replace('\n', '')
		
		message = visual.TextStim(self.win, text = IntroductionText, color = (0, 0, 0), ) # Create a stimulus for a certain window
		message.draw() 	# Draw the stimulus to the window. We always draw at the back buffer of the window.
		self.win.flip() # Flip back buffer and front  buffer of the window.
		core.wait(duration) # Pause 5 s, so you get a chance to see it!

	def ISI(self,duration): #Inter Stimulus Interval
		self.win.flip()
		core.wait(duration)

	def ITI(self,duration): #Inter Trial Interval
		self.ISI(duration)

	# Main
	def RunExperiment(self):
		#Init
		ITItime = 0.5 #Inter Trial Interval
		self.TextStimuli(Fname = "Intro.txt", duration = 1.0)		


		self.ITI(ITItime)
		while True :

			self.generateDisplay()

			ClickPos = self.MouseClick()

			self.S1.Clicked(ClickPos, self.s)
			self.S2.Clicked(ClickPos, self.s)

			#time.sleep(0.1)
				
			if self.ContinueButton.Clicked(ClickPos):
				break

		self.ITI(ITItime)
				
		self.EndOfExperiment()

	# End
	def EndOfExperiment(self):
		self.TextStimuli(Fname = "Outro.txt", duration = 1.0)
		self.win.close() # Close the window
		core.quit() # Close PsychoPy
		self.s.stop()
		time.slepp(2)
		self.s.shutdown()

###
### End of experiment definition.

##Script : 
exp = SmileExperiment()
exp.RunExperiment()

