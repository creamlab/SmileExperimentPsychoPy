# coding=utf-8

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

		self.S1 = ImageForSound(	pos 		= ( 0.3, 0.6 )
							, Image 			= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							) 

		self.S2 = ImageForSound(	pos 		= ( + 0.3, 0.3)
							, Image 			= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win 				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							)

		self.ratingScale = visual.RatingScale(self.win
							, scale			= ''
							, low 			= 1.
							, high 			= 10.
							, textColor		= 'white'
							, lineColor		= 'black'
							, size 			= 1.5
							, markerColor	= 'black'
							, showValue		= False
							, stretch		= 1.0
							, acceptText	= 'Valider'
							, precision		= 100
							, tickHeight	= 0
							)

		#Arrows
		self.ArrowR		= visual.ImageStim(self.win, image = "experiment data/pics/arrow_r.png", mask = None, units = '', pos = ( 0.45, -0.4))
		self.ArrowL 	= visual.ImageStim(self.win, image = "experiment data/pics/arrow_l.png", mask = None, units = '', pos = ( -0.47, -0.4))

		#Son A and B text
		self.TxtSonA	= visual.TextStim(self.win, text = u"Par rapport à ", pos = ( -0.1, 0.6), color = 'black')
		self.TxtSonB  	= visual.TextStim(self.win, text = "trouvez-vous que ", pos = ( -0.1, 0.3), color = 'black')
		self.TxtEst  	= visual.TextStim(self.win, text = "est dit avec : ", pos = ( -0, 0), color = 'black')


		PasSouriant 	= "beaucoup moins de sourire"
		TresSouriant 	= "beaucoup plus de sourire" # Sorry, no accents
		
		self.PasSouriante  		= visual.TextStim(self.win, text = PasSouriant, pos = ( -0.75, -0.4), color = 'black')
		self.TresSouriante  	= visual.TextStim(self.win, text = TresSouriant, pos = ( 0.7, -0.4), color = 'black')
		self.PasSouriante.height 	= 0.06
		self.TresSouriante.height 	= 0.06

		self.MidleLine	= visual.Line(self.win, start=(0, -0.45), end=(0, -0.35), lineColor = 'black', lineWidth=10)
		self.s			= Server().boot() #Audio Server - Important for Playing Audio Files
		self.s.start() # Start audio server

		#For Writing Results
		TotalFiles = len(glob.glob('participant data/*.csv')) + 1
		self.ResultsName = "participant data/Results_"+ str(TotalFiles) +".csv"
		self.fieldnames  = ['File_A', 'File_B', 'Note', 'DecisionTime','Category', 'freq', 'Cue','A Gain', 'B Gain', 'Age', 'Sex', 'Completed']
		
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
		self.AutoDrawForAll(BoolAutoDraw = True)
		
		self.S1.ImgContainer.draw()
		self.S2.ImgContainer.draw()
		self.win.flip()

	def CreateListOfFile(self,):

		#List of all Files from which a stimulus has to be maid
		ListOfFiles = []
		for file in glob.glob("experiment data/Sounds For Stimuli/*.wav"): # Wav Files
			SplitPath = os.path.split(file) # Separate path in list 
			SoundName = SplitPath[-1] # Get the last item of list in order to have the audio file name
			ListOfFiles.append(SoundName)
		shuffle(ListOfFiles) # Random File Example order

		#List of dbs to be compared 
		ListOfDbs = [(0, 0)		
					,(0, 5)		
					,(-5, 5)	
					,(-5, 10)	
					,(-10, 10)	
					,(-10, 15)	
					,(-15, 15)]

		Trials = []
		for Name in ListOfFiles:
			for pair in ListOfDbs:
				NewPair = [ str(pair[0]) + "_" + Name, str(pair[1]) + "_" + Name]
				shuffle(NewPair)
				Trials.append(NewPair)
		shuffle(Trials)
		return Trials

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
	
	def AutoDrawForAll(self, BoolAutoDraw):
		self.TxtSonA.autoDraw 			= BoolAutoDraw
		self.TxtSonB.autoDraw 			= BoolAutoDraw
		self.TxtEst.autoDraw 			= BoolAutoDraw
		self.PasSouriante.autoDraw  	= BoolAutoDraw
		self.TresSouriante.autoDraw 	= BoolAutoDraw
		self.S2.ImgContainer.autoDraw 	= BoolAutoDraw
		self.S1.ImgContainer.autoDraw 	= BoolAutoDraw
		self.ratingScale.autoDraw 		= BoolAutoDraw
		self.ArrowR.autoDraw			= BoolAutoDraw
		self.ArrowL.autoDraw			= BoolAutoDraw
		self.MidleLine.autoDraw			= BoolAutoDraw

	def ISI(self,duration): #Inter Stimulus Interval
		self.AutoDrawForAll(BoolAutoDraw = False)
		
		self.win.flip()
		core.wait(duration)
		self.generateDisplay()

	def ITI(self,duration): #Inter Trial Interval
		self.AutoDrawForAll(BoolAutoDraw = False)
		
		self.win.flip()
		core.wait(duration)

	# End
	def EndOfExperiment(self):
		self.TextStimuli(Fname = "Text/Outro.txt", duration = 8.0)
		self.win.close() # Close the window
		core.quit() # Close PsychoPy

		#Shut Down audio
		self.s.stop()
		time.slepp(2)
		self.s.shutdown()

	# ----- Main Experiment -------
	def RunExperiment(self):
		#Init
		ITItime = 0.5 #Inter Trial Interval

		#Subject Info
			#TODO

		#Intro
		self.TextStimuliUntillKey(Fname = "Text/Intro.txt")
		self.ITI(ITItime)
		self.generateDisplay()
	
		Path = "experiment data/SoundsForExperiment/"

		for NamePair in self.CreateListOfFile():
			SoundA = NamePair[0]
			SoundB = NamePair[1]

			self.S1.SetSound(Path + SoundA)
			self.S2.SetSound(Path + SoundB)
			self.ratingScale.reset(True)

			while self.ratingScale.noResponse:
				self.ratingScale.draw()
				self.win.flip()
				ClickPos = self.MouseClick()
				self.S1.Clicked(ClickPos, self.s)
				self.S2.Clicked(ClickPos, self.s)

			rating 			= self.ratingScale.getRating()
			decisionTime 	= self.ratingScale.getRT()

			GainA	= int(SoundA[0: SoundA.find("_")])
			GainB	= int(SoundB[0: SoundB.find("_")])

			# Write decisions :
			with open(self.ResultsName, 'a') as csvfile :
				writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
				writer.writerow({ 'File_A': Path + SoundA
								, 'File_B': Path + SoundB
								, 'Note'  : rating
								, 'DecisionTime' : decisionTime
								, 'A Gain'  : GainA
								, 'B Gain'  : GainB
								, 'freq'  : 2500
								, 'Cue'	  : 1.12
								})
			self.ISI(0.7)

		self.ITI(ITItime)

		#Write Completed in result
		with open(self.ResultsName, 'a') as csvfile :
			writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
			writer.writerow({'Completed': "True"})
		
		self.EndOfExperiment()

###
### End of experiment definition.

##Main Script - Calling main function and creating object : 
exp = SmileExperiment()
exp.RunExperiment()

