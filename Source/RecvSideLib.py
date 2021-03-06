from Emokit.emokit.python.emokit.emotiv import Emotiv 
from Emokit.emokit.python.emokit.packet import EmotivNewPacket
import time
import numpy
import math
from msvcrt import getch 
import pickle
import DetectionAlgorithms as DeAl
import FECLib as FECLib


def storeUserData(detectionType, user,Frequencies, UsedElectrodes, Weights):
	path = 'Source/UserData/'+detectionType+'/'+user+'.pickle'
	with open(path ,'w') as file:
		pickle.dump([Frequencies, UsedElectrodes, Weights],file)


def getUserData(detectionType, user):
	if detectionType == 'PSDA':
		Weights = None
		path = 'Source/UserData/'+detectionType+'/'+user+'.pickle'
		with open(path) as file:
			[Frequencies,UsedElectrodes,Weights] = pickle.load(file)
		return([Frequencies, UsedElectrodes, Weights])
	else:
		raise NameError ('Not Implemented')




def hardDecision(Data):
	# function which determines a frequency based on a hard decision
	decisions = numpy.zeros(len(Data),numpy.int8)#based on  number of symbols to find
	for i in range(len(Data)):
		decisions[i] = numpy.where(Data[i]==max(Data[i]))[0][0]
	return(decisions)


class DetectionObject:
	def __init__(self, method, Frequencies, Weights, electrodes, SymbolPeriod, DecisionType):
		self.Frequencies = Frequencies
		self.Weights = Weights
		self.electrodeSet = electrodes
		self.SymbolPeriod = SymbolPeriod
		self.DecisionType = DecisionType
		
		if method == 'PSDA':
			self.method = 'PSDA'
		elif method == 'CCA':
			self.method = 'CCA'
			self.trained_coeffs = None
			self.test_coeffs = None
		elif method == 'Combined':
			self.method = 'Combined'
		#elif method == 'KNN':
		#	self.method = 'KNN'
		#	self.trained_coeffs = None
		#	self.test_coeffs = None
		#	self.target_data = None
		#	self.training_data = True
		else:
			raise NameError('not Implemented')

	def getSymbols(self,data):
		# the output of this function is either symbol indices or 
		# an array with symbol probabilities
		DataSize = len(data)
		NumBatches  = DataSize/(self.SymbolPeriod*128)
		slicedData = numpy.split(data, NumBatches)
		ExpectedSymbols = numpy.zeros([NumBatches, len(self.Frequencies)])
		
		if self.method == 'PSDA':
			for index in range(NumBatches):
				ExpectedSymbols[index,:] = DeAl.psdaGet(slicedData[index], self.Frequencies,128)
		elif self.method == 'CCA':
			for index in range(NumBatches):
				ExpectedSymbols[index,:] = DeAl.ccaGet(slicedData[index], self.Frequencies,128, self.SymbolPeriod)
		elif self.method == 'Combined':
			for index in range(NumBatches):
				ExpectedSymbols[index,:] = DeAl.cca_psda_get(slicedData[index], self.Frequencies,128, self.SymbolPeriod)
		#elif self.method == 'KNN':
		#	for index in range(NumBatches):
		#		ExpectedSymbols[index,:] = DeAl.cca_psda_get(slicedData[index], self.Frequencies,128)	
		#	if self.training_data == True:
		#		self.trained_coeffs = ExpectedSymbols
		#		self.training_data = False
		#	else:
		#		self.test_coeffs = ExpectedSymbols
		else:
			raise NameError('not Implemented')
			
		if self.DecisionType == 'HARD':
			return(hardDecision(ExpectedSymbols))
		else:
			return(ExpectedSymbols) 
'''
	def get_knn_data(self, target_data,data):
		self.getSymbols(target_data)
		self.getSymbols(data)
		
	def find_knn(self): #,train_set,test_set):
		#self.trained_coeffs = DeAl.cca_psda_get(train_set,self.Frequencies,128)
		#self.test_coeffs = DeAl.cca_psda_get(test_set,self.Frequencies,128)
		predictions = []
		k = 3
		#print 'testCo: ', (self.test_coeffs[:][1])
		#print 'lenn: ', len(self.test_coeffs)
		for x in range(len(self.test_coeffs)):
			print 'XXXX:, ', x
			neighbors = DeAl.getNeighbors(self.trained_coeffs, max(self.test_coeffs[:][x]), k)
			result = DeAl.getResponse(neighbors)
			predictions.append(result)
			print('> predicted=' + repr(result) + ', actual=' + repr(self.test_coeffs[x][-1]))
		accuracy = DeAl.getAccuracy(self.test_coeffs, predictions)
		print('Accuracy: ' + repr(accuracy) + '%')
		
		probs = predictions/sum(predictions)
		
		print 'ASSS: ', probs
		
		return hardDecision(probs)
		
		#return probs
'''	

def Demapper(Symbols, num_Symbols,method):
	# the InputType is either hard or Soft and determined by the type of symbols comming in
	# the OutputType is either hard [0;1] or soft [prob(1)]
	# note if the input is hard, then the outputType will also be hard
	if method =='HARD':
		bitsPerSymbol = math.log(num_Symbols,2)
		encodedData = ''
		for Symbol in Symbols:
			newCode = bin(Symbol)
			newCode = newCode[2:]
			newCode = '0'*int(bitsPerSymbol-len(newCode)) +newCode 
			encodedData = encodedData + newCode
		return(encodedData)
	else:
		raise NameError ('not implemented')


def breakString(string, brokenLength):
	# Ensure that the string can be broken in equal lengths
	numSubs = len(string)/brokenLength
	brokenData = []
	for i in range(numSubs):
		brokenData = brokenData + [string[i*brokenLength:brokenLength*(i+1)]]
	return (brokenData)


class ChannelDecoder:
	def __init__(self, method='none',inputType='HARD', blockSize=None, msgSize=None): # blockSize = None, rate = None):
		self.method = method
		self.inputType = inputType
		
		if self.method =='none':
			if self.inputType != 'HARD':
				raise NameError('Not Implemented')
		elif self.method =='HardHamming' and self.inputType =='HARD':
			self.hamming_obj = FECLib.hammingCode(blockSize, msgSize)
			self.blockSize = blockSize #self.hamming_obj.get_blockSize()
		else:
			raise NameError('Not Implemented')



	def Decode(self, data):
		if self.method =='none' and self.inputType =='HARD':
			return (data)
		elif self.method =='HardHamming' and self.inputType=='HARD':
			brokenData = breakString(data, self.blockSize)
			String = ""
			for elem in brokenData:
				String = String + self.hamming_obj.HardHammingDecode(elem) #, self.blockSizes, self.rate)
			return (String)
		else:
			raise NameError('Not Implemented')
			
	def de_interleave(self, message):
		
		message = self.depad(message)
		
		x = len(message)
		n_cols = self.min_cols(x)
		
		if x%n_cols != 0: 
			raise ValueError("In interleave(), len(message)=%d is not a multiple of ncols=%d" % (x,n_cols))
		
		result = []
		for i in range(0, n_cols):
			result.extend(message[i:len(message):n_cols])
			
		str_result = ''
		for i in range(0, len(result)):
			str_result = str_result + str(result[i])
    
		return str_result
		
	def min_cols(self,x):
		#possible_cols = []
		for i in range(2, x):
			if x%i == 0:
				return i
				

	def depad(self,msg):
		x = len(msg)
		
		num_words = int(x/self.blockSize) 
		ind = num_words*self.blockSize
		
		return msg[:ind]
	

def loadCharacterSet(SetName):
	fullName = 'Source/CharacterSets/'+SetName+'.txt'
	file = open(fullName,'r')
	fullSet = file.read()
	validChars = fullSet.split(',')
	return (validChars)


class sourceDecoder:
	def __init__(self, CharSet, method='basic'):
		if method == 'basic':
			alphabetSize = len(CharSet)
			self.CodeLength = int(math.ceil(math.log(alphabetSize,2)))
			self.alphabet = CharSet
		else :
			raise NameError ('Not implemented')

	def Decode(self,data):
		splitData = breakString(data, self.CodeLength) ## this will disregard any bits added by the FEC to fill blocks
		String = ""
		for elem in splitData:  
			try:
				String = String + self.alphabet[int(elem,2)]
			except IndexError:
				String = String + '*'
		return(String)



def calculateRecvTime(SymbolPeriod, NumSymbols, FEC_blockSize, FEC_msgSize, NumCharacters, AlphabetLength):
	# calculate how long it will take to receive the caracters
	FEC_Rate = float(FEC_msgSize)/FEC_blockSize
	#print 'AAAAA: ', FEC_Rate
	bitsPerCharacter = math.ceil(math.log(AlphabetLength, 2))
	#print 'BBBBBB: ', bitsPerCharacter
	bitsAfterSource  = bitsPerCharacter*NumCharacters
	#print 'CCCCC: ', bitsAfterSource
	FECBlocks = math.ceil(float(bitsAfterSource)/(FEC_msgSize))
	#print 'DDDDDD: ', FECBlocks
	encLength = FECBlocks*FEC_blockSize
	#print 'EEEEEE: ', encLength
	bitsPerSymbol = math.log(NumSymbols, 2)
	#print 'FFFFF: ', bitsPerSymbol
	numSymbols = math.ceil(float(encLength)/bitsPerSymbol)
	#print 'GGGGG: ', numSymbols
	recvTime = numSymbols*SymbolPeriod
	#print 'HHHHH: ', recvTime
	return(recvTime)
