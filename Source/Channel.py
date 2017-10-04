import numpy
import math
import time
import csv
import datetime 
from msvcrt import getch 

from Emokit.emokit.python.emokit.emotiv import Emotiv
from Emokit.emokit.python.emokit.packet import EmotivNewPacket




class Channel:
	# the channel object has multiple variations to allow for more
	# productive testing and operation
	# the class can operate on pure real time recording:
	# has the option of additionally logging the data to a file for further analyis
	# has the option of reading in data from a file this allows for strict
	# algorithm comparision on the same set of data
	def __init__(self, source, Electrodes, WriteToFile = False, ReadFile = None):
		self.sampleRate = 128

		self.fileWrite = WriteToFile
		self.source = source
		self.ElectrodeList = Electrodes
		if source == 'Emokit':
			self.device = Emotiv(display_output=False, verbose=False)
			time.sleep(2)

		elif source =='File':
			if ReadFile == None:
				raise NameError('File Name Not Given')
			self.File = open(ReadFile, 'r')
			self.Reader = csv.reader(self.File)
			if self.Reader.next() !=self.ElectrodeList:
				raise NameError ('expected Electrodes dont match file')
		else:
			raise NameError('Source Not Implemented')


	def getDataBlock(self, recordTime, flushBuffer = True, restartFileRead = True): 
		numSamples = recordTime*self.sampleRate
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
			filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +'.csv'
			File = open(filename, 'w')
			writer = csv.writer(File)
			writer.writerow(self.ElectrodeList)
			for i in range(len(DataBlock)):
				writer.writerow(DataBlock[i])
			File.close()
		return(DataBlock)

	def flushBuffer(self):
		if self.source == 'Emokit':
			self.device.clear_queue()
		else:
			print('Warning: flush buffer has no effect on file source')



	def waitForStart(self, action):
		# if action == 'KeyPress':
		# 	print('Press S to start: ')
		# 	while True:
		# 		Key  = ord(getch())
		# 		if Key == 115: # S
		# 		#	self.flushBuffer()
		# 			return 
		if action == 'KeyPress':
			A = raw_input('Enter S to begin: ')
			if A == 'S' or A =='s':
				self.flushBuffer()
				return(True)
		else :
			raise NameError ('invalid Action')
