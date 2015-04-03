import csv
import glob
import numpy as np
import matplotlib.pyplot as plt


ListOfDbs = [(0, 0)		
			,(0, 5)		
			,(-5, 5)	
			,(-5, 10)	
			,(-10, 10)	
			,(-10, 15)	
			,(-15, 15)]

def IsCompleted(file):
	Completed = False
	with open(file, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['Completed'] == "True":
				Completed = True
	if Completed:
		return Completed
	else:
		print "Attention le fichier "+ str(file) + " n'est pas complet !"
		return Completed


def ReadData():
	Data = []
	for file in glob.glob("participant data/*.csv"): # Wav Files
		if IsCompleted(str(file)):
			with open(file, 'rb') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					Data.append((float(row['Note']), int(row['A Gain']), int(row['B Gain'])))
	return Data

def FormatData(Data):
	PosNote, PosGainA , PosGainB = 0, 1, 2

	DataDict = {}
	for i in range (0, len(Data)):
		row = Data[i]
		GainPair = (row[PosGainA], row[PosGainB] )
		if GainPair in ListOfDbs:
			PairStr = str(GainPair)
			DataDict.setdefault(PairStr,[]).append(row[PosNote])
			print "La pairdB est : "+ PairStr
			print "La note est : "+ str(row[PosNote])
			print

		elif GainPair[::-1] in ListOfDbs:
				PairStr = str(GainPair[::-1])
				DataDict.setdefault(PairStr,[]).append(-row[PosNote])
				print "La pairdB est : "+ PairStr
				print "La note est : "+ str(-row[PosNote])
				print

		else:
			print "Error in Data formating, pair of dB not in list of dB"




	return DataDict

def PlotData(DataDict, means, error):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	## the data
	N = len(ListOfDbs)


	## necessary variables
	ind = np.arange(N)                # the x locations for the groups
	width = 0.35                      # the width of the bars

	## the bars
	rects1 = ax.bar(ind, means, width
	                , color 	= 'black'
	                , yerr 		= error
	                , error_kw 	= dict(elinewidth=2, ecolor = 'green' )
	                )

	# axes and labels
	ax.set_xlim(-width, len(ind)+width)
	ax.set_ylim(-10,10)
	ax.set_ylabel('Score')
	ax.set_title('Scores dependeing on eq')
	xTickMarks = [str(ListOfDbs[i]) for i in range(0,len(ListOfDbs))]
	ax.set_xticks(ind)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation = 45, fontsize = 10)

	## add a legend

	plt.show()



Data = ReadData()
if Data == []:
	print "No data analysed, csv files may be incomplete or damaged"
	exit(0)

DataDict = FormatData(Data)

means = []
error = []

for PairOfGain in ListOfDbs:
	x = DataDict.get(str(PairOfGain))
	means.append(np.mean(x))
	error.append(np.std(x))

PlotData(DataDict, means, error)
