from psychopy import visual, core, event, visual, logging #import some libraries from PsychoPy
from Objects.ImageForSound import *
from Objects import Button
import glob
import csv
from random import shuffle
import codecs

class SmileExperiment:
 	def __init__(self):
		self.win 		= visual.Window(size=(1280, 800), pos=None, color=(255, 255, 255))

		self.mouse 		= event.Mouse(visible = True, newPos = False, win = self.win)
		self.trialClock = core.Clock()
		self.expClock 	= core.Clock()
		self.clickGap 	= .1 #seconds
		
		self.ratingScale = None
		
		self.S1 = ImageForSound(	pos 		= ( - 0.3, 0.6)
							, ImageName 		= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							) 

		self.S2 = ImageForSound(	pos 		= ( + 0.3, 0.6)
							, ImageName 		= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win 				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							)

		self.ratingScale = None

		#for i in range (1,10):

		self.TxtSonA	= visual.TextStim(self.win, text = "Son A : ", pos = ( -0.5, 0.6), color = 'black')
		self.TxtSonB  	= visual.TextStim(self.win, text = "Son B : ", pos = ( +0.1, 0.6), color = 'black')

		PasSouriant = "Pas du tout souriante"
		TresSouriant = "Tres souriante"
		
		self.PasSouriante  		= visual.TextStim(self.win, text = PasSouriant, pos = ( -0.75, -0.4), color = 'black')
		self.TresSouriante  	= visual.TextStim(self.win, text = TresSouriant, pos = ( 0.7, -0.4), color = 'black')
		self.PasSouriante.height 	= 0.06
		self.TresSouriante.height 	= 0.06

		self.s			= Server().boot() #Audio Server
		self.s.start()

		#For Writing Results
		TotalFiles = len(glob.glob('participant data/*.csv'))
		self.ResultsName = "participant data/Results_"+ str(TotalFiles) +".csv"
		self.fieldnames  = ['File_A', 'File_B', 'Note', 'DecisionTime','A is neutral', 'B is neutral', 'Gain', 'freq', 'Cue']
		with open(self.ResultsName, 'w') as csvfile:
			writer		= csv.DictWriter(csvfile, fieldnames = self.fieldnames)
			writer.writeheader()

	# Mouse Functions
	def MouseClick(self):
		c, c_old 	= (0,0)
		while True :
			any_press 	= self.mouse.getPressed()
			c 			= self.trialClock.getTime()
			b1_press 	= any_press[0]
			time.sleep(0.01) # For controlling the process from taking too much CPU 
			if b1_press and c - c_old > self.clickGap:
				c_old = c
				return self.mouse.getPos()

    # Display Functions
	def generateDisplay(self):
		self.S1.Draw()	
		self.S2.Draw()
		self.TxtSonA.autoDraw = True
		self.TxtSonB.autoDraw = True
		self.PasSouriante.autoDraw  = True
		self.TresSouriante.autoDraw = True
		self.win.flip()

	def TextStimuliUntillKey(self, Fname):
		with codecs.open (Fname, "r", "utf-8") as myfile:
			IntroductionText = myfile.read()

		message = visual.TextStim(self.win, text = IntroductionText, color = 'black') # Create a stimulus for a certain window
		message.height = 0.05
		message.draw() 	# Draw the stimulus to the window. We always draw at the back buffer of the window.
		self.win.flip() # Flip back buffer and front  buffer of the window.

		while True:
			if len(event.getKeys()) > 0: break
			event.clearEvents()
			core.wait(0.2)

	def TextStimuli(self, Fname, duration):
		with codecs.open (Fname, "r", "utf-8") as myfile:
			IntroductionText = myfile.read()
		
		
		message = visual.TextStim(self.win, text = IntroductionText, color = 'black') # Create a stimulus for a certain window		
		message.draw() 	# Draw the stimulus to the window. We always draw at the back buffer of the window.
		
		self.win.flip() # Flip back buffer and front  buffer of the window.
		core.wait(duration) # Pause 5 s, so you get a chance to see it!
		
	def ISI(self,duration): #Inter Stimulus Interval
		self.win.flip()
		core.wait(duration)

	def ITI(self,duration): #Inter Trial Interval
		self.ISI(duration)

	# End
	def EndOfExperiment(self):
		self.TextStimuli(Fname = "Text/Outro.txt", duration = 8.0)
		self.win.close() # Close the window
		core.quit() # Close PsychoPy
		self.s.stop()
		time.slepp(2)
		self.s.shutdown()


	# ----- Main Experiment -------
	def RunExperiment(self):
		#Init
		ITItime = 0.5 #Inter Trial Interval
		self.TextStimuliUntillKey(Fname = "Text/Intro.txt")

		self.ITI(ITItime)

		self.generateDisplay()
		ListOfFiles = []

		for file in glob.glob("experiment data/sounds/*.wav"): # Wav Files
			SplitPath = os.path.split(file) # Separate path in list 
			SoundName = SplitPath[-1] # Get the last item of list in order to have the audio file name
			ListOfFiles.append(SoundName)

		shuffle(ListOfFiles) # Random File Example order

		Paths = ["experiment data/sounds/", "experiment data/Modified Sounds/"]
		for FName in ListOfFiles:
			shuffle(Paths) # Random A and B
			self.S1.SetSound(Paths[0] + FName)
			self.S2.SetSound(Paths[1] + FName)
						
			self.ratingScale = visual.RatingScale(self.win
								, scale			= 'Par rapport a la voix A, la voix B est ...'
								, low 			= -10
								, high 			= 10
								, textColor		= 'black'
								, lineColor		= 'black'
								, size 			= 1.5
							)

			while self.ratingScale.noResponse:
				self.ratingScale.draw()
				self.win.flip()

				ClickPos = self.MouseClick()
				self.S1.Clicked(ClickPos, self.s)
				self.S2.Clicked(ClickPos, self.s)

			rating 			= self.ratingScale.getRating()
			decisionTime 	= self.ratingScale.getRT()
			choiceHistory 	= self.ratingScale.getHistory()


			with open(self.ResultsName, 'a') as csvfile :
				writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
				writer.writerow({ 'File_A': Paths[0] + FName
								, 'File_B': Paths[1] + FName
								, 'Note'  : rating
								, 'DecisionTime' : decisionTime
								, 'A is neutral' : ("Modified" not in Paths[0])
								, 'B is neutral' : ("Modified" not in Paths[1])
								, 'Gain'  : 3
								, 'freq'  : 2500
								, 'Cue'	  : 1.12
								})

		self.ITI(ITItime)
		self.EndOfExperiment()
###
### End of experiment definition.

##Script : 
exp = SmileExperiment()
exp.RunExperiment()

