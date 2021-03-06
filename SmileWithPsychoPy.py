# coding=utf-8
from psychopy import visual, core, event, visual, logging
from PsychopyObjects.ImageForSound import *
from PsychopyObjects import Button
import glob
import csv
from random import shuffle
import codecs

class SmileExperiment:
	def __init__(self):
		self.win 		= visual.Window(size=(1280, 800), pos=None, color=(255, 255, 255), allowGUI = True) # Add : fullscr=True before experience
		self.mouse 		= event.Mouse(visible = True, win = self.win)
		self.trialClock = core.Clock()
		self.expClock 	= core.Clock()
		self.clickGap 	= .1 #seconds
		self.ratingScale = None

		self.s			= Server(duplex=0).boot() #Audio Server - Important for Playing Audio Files
		self.s.start() # Start audio server

		self.S1 = ImageForSound(	pos 		= ( - 0.6, - 0.4 )
							, Image 			= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							) 

		self.S2 = ImageForSound(	pos 		= ( + 0.6 , -0.4)
							, Image 			= "experiment data/pics/play.png"
							, ClickedImage	 	= "experiment data/pics/play_small.png"
							, win 				= self.win
							, size 				= 0.15
							, SoundName 		= "experiment data/sounds/C1.wav"
							)

		self.ratingScale = visual.RatingScale(self.win
							, scale			= ''
							, low 			= -10.
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

		#Question
		self.TxtEst  	= visual.TextStim(self.win, text = u"Quel locuteur vous semble être le plus souriant?", pos = ( -0, 0), color = 'black')

		self.MidleLine	= visual.Line(self.win, start=(0, -0.45), end=(0, -0.35), lineColor = 'black', lineWidth=10)

		self.TxtMid  	= visual.TextStim(self.win, text = u"Pas de différence", pos = (0, -0.5), color = 'black', height = 0.05)

		#For Writing Results
		TotalFiles = len(glob.glob('participant data/*.csv')) + 1
		self.ResultsName = "participant data/Results_" + str(TotalFiles) + ".csv"
		self.fieldnames  = ['File_A', 'File_B', 'Note', 'DecisionTime','SpeakerGenre', 'Sentence', 'freq', 'Cue','A Gain', 'B Gain', 'NumberOfPlaysSoundA', 'NumberOfPlaysSoundB','Age', 'Sex', 'Completed']

		with open(self.ResultsName, 'w+') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
			writer.writeheader()

	def MouseClick(self):
		c, c_old 	= (0, 0)
		while True :
			any_press 	= self.mouse.getPressed()
			c 			= self.trialClock.getTime()
			b1_press 	= any_press[0]
			time.sleep(0.01)  # For controlling the process from taking too much CPU
			if b1_press and c - c_old > self.clickGap:
				c_old = c
				return self.mouse.getPos()

	#Display Functions
	def generateDisplay(self):
		self.AutoDrawForAll(BoolAutoDraw = True)
		
		self.S1.ImgContainer.draw()
		self.S2.ImgContainer.draw()
		self.win.flip()

	def CreateListOfFile(self):

		#List of all Files from which a stimulus has to be maid
		ListOfFiles = []
		for file in glob.glob("experiment data/Sounds For Stimuli/*.wav"): # Wav Files
			SplitPath = os.path.split(file) # Separate path in list 
			SoundName = SplitPath[-1] # Get the last item of list in order to have the audio file name
			ListOfFiles.append(SoundName)
		shuffle(ListOfFiles) # Random File Example order

		#List of dbs to be compared 
		ListOfDbs = [(0, 0)
					,(5, 10)
					,(0, 5)
					,(-5, 0)
					,(-10, -5)
					,(-10, 0)			
					,(-5, 5)
					,(0, 10)	
					,(-10, 5)
					,(-5, 10)	
					,(-10, 10)	
					]


		Trials = []
		for Name in ListOfFiles:
			for pair in ListOfDbs:
				NewPair = [ str(pair[0]) + "_" + Name, str(pair[1]) + "_" + Name]
				shuffle(NewPair)
				Trials.append(NewPair)
		shuffle(Trials)
		return Trials

	def WriteCompleted(self, bool):
		with open(self.ResultsName, 'rb') as file1, open('aux.csv', 'wb') as aux:
			reader = csv.reader(file1)
			writer = csv.writer(aux)
			IndexCompleted = self.fieldnames.index('Completed')
			for i, row in enumerate(reader):
				if i == 1:
					row[IndexCompleted] = bool
				writer.writerow(row)

			os.rename('aux.csv', self.ResultsName)

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
		self.TxtEst.autoDraw 			= BoolAutoDraw
		self.S2.ImgContainer.autoDraw 	= BoolAutoDraw
		self.S1.ImgContainer.autoDraw 	= BoolAutoDraw
		self.ratingScale.autoDraw 		= BoolAutoDraw
		self.ArrowR.autoDraw			= BoolAutoDraw
		self.ArrowL.autoDraw			= BoolAutoDraw
		self.MidleLine.autoDraw			= BoolAutoDraw
		self.TxtMid.autoDraw 			= BoolAutoDraw

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

		#Intro
		self.TextStimuliUntillKey(Fname = "Text/Intro.txt")
		self.ITI(ITItime)
		self.generateDisplay()

		Path = "experiment data/SoundsForExperiment/"

		for NamePair in self.CreateListOfFile():
			SoundA = NamePair[0]
			SoundB = NamePair[1]
			NumberOfPlaysSoundA = 0
			NumberOfPlaysSoundB = 0

			self.S1.SetSound(Path + SoundA)
			self.S2.SetSound(Path + SoundB)
			self.ratingScale.reset(True)

			#print "Le Gain de A est : "+ str(SoundA[0: SoundA.find("_")])
			#print "Le Gain de B est : "+ str(SoundB[0: SoundB.find("_")])

			while self.ratingScale.noResponse:
				self.ratingScale.draw()
				self.win.flip()
				ClickPos = self.MouseClick()
				if self.S1.Clicked(ClickPos, self.s):
					NumberOfPlaysSoundA = NumberOfPlaysSoundA + 1

				if self.S2.Clicked(ClickPos, self.s):
					NumberOfPlaysSoundB = NumberOfPlaysSoundB + 1

			rating 			= self.ratingScale.getRating()
			decisionTime 	= self.ratingScale.getRT()

			GainA	= int(SoundA[0: SoundA.find("_")])
			GainB	= int(SoundB[0: SoundB.find("_")])

			Category = SoundA[SoundA.find("_")+1: SoundA.find("_") + 2] # parse Sound Name
			Sentence = SoundA[SoundA.find("_")+2: SoundA.find("_") + 3] # parse Sound Name
			
			# Write results :
			with open(self.ResultsName, 'a') as csvfile :
				writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
				writer.writerow({ 'File_A': Path + SoundA
				, 'File_B': Path + SoundB
				, 'Note'  : rating
				, 'DecisionTime' : decisionTime
				, 'A Gain'  : GainA
				, 'B Gain'  : GainB
				, 'freq'  : 4000
				, 'Cue'	  : 0.6
				, 'SpeakerGenre' : Category
				, 'Sentence' : Sentence
				, 'NumberOfPlaysSoundA' : NumberOfPlaysSoundA
				, 'NumberOfPlaysSoundB' : NumberOfPlaysSoundB
				})

			self.ISI(0.7)

		self.ITI(ITItime)
		self.WriteCompleted(True)

		self.EndOfExperiment()

###
### End of experiment definition.

### Main Script - Calling main function and creating object :
exp = SmileExperiment()
exp.RunExperiment()

