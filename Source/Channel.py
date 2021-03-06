import numpy
import math
import time
import csv
import datetime 
from msvcrt import getch 

from Emokit.emokit.python.emokit.emotiv import Emotiv
from Emokit.emokit.python.emokit.packet import EmotivNewPacket

import DetectionAlgorithms as DA


def dataUpdate(OldData, newData):
	for column in range(len(OldData[0])):
		OldData[:,column] = numpy.roll(OldData[:,column], -len(newData))
		OldData[len(OldData)-len(newData):len(OldData),column] = newData[:,column]
	return (OldData)

def movingAverageFilter(Data, newValue):
	Data = numpy.roll(Data,1)
	Data[0] = newValue
	return([Data, sum(Data)/len(Data)])


class Channel:
	# the channel object has multiple variations to allow for more
	# productive testing and operation
	# the class can operate on pure real time recording:
	# has the option of additionally logging the data to a file for further analyis
	# has the option of reading in data from a file this allows for strict
	# algorithm comparision on the same set of data
	def __init__(self, source, Electrodes, WriteToFile = False, ReadFile = None, useHeader = False, holdFreq = None, headerFreq =None, startThreshold=None, startThresholdRelative=None, crossoverThresholdRelative=None):
		self.sampleRate = 128

		self.fileWrite = WriteToFile
		self.source = source
		self.ElectrodeList = Electrodes
		self.useHeader = useHeader
		self.holdFreq = holdFreq
		self.headerFreq = headerFreq
		self.startThreshold = startThreshold
		self.startThresholdRelative = startThresholdRelative
		self.crossoverThresholdRelative = crossoverThresholdRelative

		if useHeader == True :
			if holdFreq == None or headerFreq == None or startThreshold == None:
				raise NameError('Must provide parameters when using header')

		if source == 'Emokit':
			self.device = Emotiv(display_output=False, verbose=False)
			time.sleep(2)

		elif source =='File':
			if ReadFile == None:
				raise NameError('File Name Not Given')
			if useHeader == True:
				raise NameError('Cannot use  header Sync with File input')
			self.File = open(ReadFile, 'r')
			self.Reader = csv.reader(self.File)
			if self.Reader.next() !=self.ElectrodeList:
				raise NameError ('expected Electrodes dont match file')
		else:
			raise NameError('Source Not Implemented')


	def setFileName(self, directedName):
		self.runFileName = directedName

	def getDataBlock(self, recordTime, flushBuffer = True, restartFileRead = True, UseNumSamples = 0, overrideRecord = False): 
		# the overrideRecord is to prevent the channel logging recordings when this function in the header

		if overrideRecord == True:
			# ignore self.fileWrite in this call of the function
			storeFileWrite = self.fileWrite
			self.fileWrite = False

		if UseNumSamples == 0:
			numSamples = recordTime*self.sampleRate
		else:
			numSamples = UseNumSamples # a hard set of the number of samples to use

		DataBlock = numpy.zeros((numSamples, len(self.ElectrodeList)))

		if self.source == 'Emokit':
			if flushBuffer == True:
				self.device.clear_queue()
			counter = 0
			while counter < numSamples:
				Packet  = self.device.dequeue()
				if Packet is not None:
					for i in range(len(self.ElectrodeList)):
						DataBlock[counter, i] = Packet.sensors[self.ElectrodeList[i]]['value']
					counter +=1

		if self.source == 'File':
			if restartFileRead == True:
				self.File.seek(0) #resets the file pointer to the first data row in file
				self.Reader.next()
				counter = 0
				while counter <numSamples:
					dat = self.Reader.next() # get the next data row
					for i in range(len(self.ElectrodeList)):
						DataBlock[counter, i]=float(dat[i])
					counter +=1
			else :
				raise NameError('Continous reading not implemented')


		if self.fileWrite == True:
	#		filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +'.csv'
			filename = self.runFileName
			File = open(filename, 'w')
			writer = csv.writer(File)
			writer.writerow(self.ElectrodeList)
			for i in range(len(DataBlock)):
				writer.writerow(DataBlock[i])
			File.close()

		if overrideRecord == True:
			self.fileWrite = storeFileWrite
			
		return(DataBlock)



	def flushBuffer(self):
		if self.source == 'Emokit':
			print('flushing Emotiv Buffer')
			self.device.clear_queue()
		else:
			print('Warning: flush buffer has no effect on file source')



#### AUTO SYNC CODE BEGIN #####################################################
	def shortDataCollect(self, numSamples, SingleElectrode):
		# collect just a single short batch of data, Only on one electrode
		counter = 0
		Data = numpy.zeros(numSamples)
		while counter < numSamples:
			Packet = self.device.dequeue()
			if Packet is not None:
				Data[counter] = Packet.sensors[SingleElectrode]['value']
				counter +=1
		return(Data)

	def autoSync(self):
		# the autoSync routine is non-trivial
		# based on the header information which is sent on the sender side
		# the process has 3 stages :
			# 1) Passive: not looking at the light
			# 2) Active: looking at the light waiting for transmission
			# 3) Sync: engaged in the header stage of transmission
		blockSize = 512 #corresponds to the header Not the actual data stream size
		DetectionMethod = 'PSDA'
		ElectrodeForSync = 'O1'
		relativeHeightForStart = self.startThresholdRelative
		relativeHeightForHeaderDetection = self.crossoverThresholdRelative
		numHeaderBatches = 6 # how many blocks to record as part of the header
		if DetectionMethod != 'PSDA':
			raise NameError ('Sync Procedure not yet extended for None PSDA')


		self.flushBuffer()
		state = 'Passive'
		while state == 'Passive':
			Data = self.shortDataCollect(blockSize, ElectrodeForSync)
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data,[self.holdFreq, self.headerFreq],128, True)
			print(absHeights)
			print(Probabilities)
			if Probabilities[0] > relativeHeightForStart and absHeights[0] > self.startThreshold:
				state = 'Active'
		print('Gaze Detected')

		while state == 'Active':
			Data = self.shortDataCollect(blockSize, ElectrodeForSync)
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data,[self.holdFreq, self.headerFreq],128, True)
			print(absHeights)
			print(Probabilities)
			if Probabilities[0]<relativeHeightForHeaderDetection*Probabilities[1]:
				state = 'Sync'
		print('Header Begin')

		heights = []
		for i in range(numHeaderBatches):
			Data = self.shortDataCollect(blockSize, ElectrodeForSync)
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data,[self.holdFreq, self.headerFreq],128, True)
			print(absHeights)
			print(Probabilities)
			heights = heights + [Probabilities[0]]

		if heights[1] == max(heights):
			print('3s pause')
			time.sleep(3)
			return(True)
		if heights[2] == max(heights):
			print('2s pause')
			time.sleep(2)
			return(True)
		if heights[3] == max(heights):
			print('1s pause')
			time.sleep(1)
			return(True)
		if heights[5] == max(heights):
			print('4s pause')
			time.sleep(4)
			return(True)
		else :
			# bad sync may not be correctable. 
			# however the fact that a bad sync occured may be useful in decoding
			print('bad Sync')
			time.sleep(4)
			return (False)


	#def headerV2(self):
		# this header only allows for the use of psda for now
		# the O1 electrode is assumed to be the first electrode on the electrode list
	def gaze_detect(self):
		updateSize = 128
		fftSize = 512
		ElectrodePositionInList = 0 # make sure the O1 electrode is first on the list
		GazeThresholdAbs = self.startThreshold
		GazeThresholdRelative = self.startThresholdRelative
		HeaderThresholdRelative = self.crossoverThresholdRelative
		smoothProb = numpy.zeros(4) # is the vector of the last 4 probabilitity readings of the hold Frequency
		PeakDelay = 1.5 # the peak delay is lag induced by the moving average ( dependant on the size of the MA)
		timeToStart = 8 # this is based on the time between the sender sending the start signal and data transmission (8 seconds)

		self.flushBuffer()
		state = 'Passive'
		while state == 'Passive':
			Data = self.shortDataCollect(fftSize, self.ElectrodeList[ElectrodePositionInList])
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data,[self.holdFreq, self.headerFreq],128, True)
			print(absHeights)
			print(Probabilities)
			if Probabilities[0] > GazeThresholdRelative and absHeights[0] > GazeThresholdAbs:
				state = 'Active'
		print('Gaze Detected')
		return True
		
	def threshold_detect(self):
		updateSize = 128
		fftSize = 512
		ElectrodePositionInList = 0 # make sure the O1 electrode is first on the list
		GazeThresholdAbs = self.startThreshold
		GazeThresholdRelative = self.startThresholdRelative
		HeaderThresholdRelative = self.crossoverThresholdRelative
		smoothProb = numpy.zeros(4) # is the vector of the last 4 probabilitity readings of the hold Frequency
		PeakDelay = 1.5 # the peak delay is lag induced by the moving average ( dependant on the size of the MA)
		timeToStart = 8 # this is based on the time between the sender sending the start signal and data transmission (8 seconds)
		
		self.flushBuffer()
		Data = numpy.zeros([fftSize,1])
		DataFull = self.getDataBlock(0,flushBuffer = False, restartFileRead = False, UseNumSamples = fftSize, overrideRecord = True)
		Data = DataFull
		ThresholdReached = False
		while ThresholdReached == False:
			newDataFull = self.getDataBlock(0,flushBuffer = False, restartFileRead = False, UseNumSamples = updateSize, overrideRecord = True)
			newData  = newDataFull
			Data = dataUpdate(Data, newData)
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data[:,0],[self.holdFreq, self.headerFreq],128, True)
			[smoothProb, currentValue] = movingAverageFilter(smoothProb,Probabilities[1])

			if currentValue> HeaderThresholdRelative:
					ThresholdReached = True
					print ('Threshold Reached')
			print(currentValue)
		ThresholdDrop = False
		PeakProbSet = numpy.zeros(10) # safety buffer
		PeakProbSet[0] = currentValue
		PeakTimeSet = numpy.zeros(10)
		PeakTimeSet[0] = time.time()
		count = 1
		while ThresholdDrop == False:
			newDataFull = self.getDataBlock(0,flushBuffer = False, restartFileRead = False, UseNumSamples = updateSize, overrideRecord = True)
			newData  = newDataFull
			Data = dataUpdate(Data, newData)
			[Probabilities, absHeights] = DA.psdaGetForHeader(Data[:,0],[self.holdFreq, self.headerFreq],128, True)
			[smoothProb, currentValue] = movingAverageFilter(smoothProb, Probabilities[1])
			PeakProbSet[count] = currentValue
			PeakTimeSet[count] = time.time()
			if currentValue< HeaderThresholdRelative:
					ThresholdDrop = True
					print ('Threshold Reached')
			print(currentValue)
			print(time.time())
			count +=1
		print(PeakProbSet)
		print(PeakTimeSet)
		print('Max Value', max(PeakProbSet))
		print('Time of Max', PeakTimeSet[PeakProbSet.argmax()] )
		ptime = PeakTimeSet[PeakProbSet.argmax()]
		currentTime = time.time()
		time.sleep(timeToStart-(currentTime-ptime+PeakDelay))
		print(time.time())
		return(True)


#### AUTO SYNC CODE END #####################################################



	def waitForStart(self, action):
		if action == 'KeyPress':
			A = raw_input('Enter S to begin: ')
			if A == 'S' or A =='s':
				print('Started')
				self.flushBuffer()
				return(True)
		if action == 'HeaderBased':
			if self.useHeader == False:
				raise NameError ('Provide Channel Constructer with arguments when using HeaderBased Sync')
			status = self.autoSync()
			return(status)
		elif action == 'HeaderV2':
			self.gaze_detect()
			self.threshold_detect()
		else :
			raise NameError ('invalid Action')


