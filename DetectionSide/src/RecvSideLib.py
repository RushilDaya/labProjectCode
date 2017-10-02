from Emokit.emokit.python.emokit.emotiv import Emotiv 
from Emokit.emokit.python.emokit.packet import EmotivNewPacket
import time
import numpy
import math
from msvcrt import getch 
import pickle
import DetectionAlgorithms as DeAl


def storeUserData(detectionType, user,Frequencies, UsedElectrodes, Weights):
	path = 'src/UserData/'+detectionType+'/'+user+'.pickle'
	with open(path ,'w') as file:
		pickle.dump([Frequencies, UsedElectrodes, Weights],file)


def getUserData(detectionType, user):
	if detectionType == 'PSDA':
		Weights = None
		path = 'src/UserData/'+detectionType+'/'+user+'.pickle'
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
		if method == 'PSDA':
			self.method = 'PSDA'
			self.Frequencies = Frequencies
			self.Weights = Weights
			self.electrodeSet = electrodes
			self.SymbolPeriod = SymbolPeriod
			self.DecisionType = DecisionType
		else:
			raise NameError('not Implemented')

	def getSymbols(self,data):
		# the output of this function is either symbol indices or 
		# an array with symbol probabilities
		if self.method == 'PSDA':
			DataSize = len(data)
			NumBatches  = DataSize/(self.SymbolPeriod*128)
			slicedData = numpy.split(data, NumBatches)
			ExpectedSymbols = numpy.zeros([NumBatches, len(self.Frequencies)])
			for index in range(NumBatches):
				ExpectedSymbols[index,:] = DeAl.psdaGet(slicedData[index], self.Frequencies,128)
		else:
			raise NameError('not Implemented')

		if self.DecisionType == 'HARD':
			return(hardDecision(ExpectedSymbols))
		else:
			return(ExpectedSymbols)




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


class ChannelDecoder:
	def __init__(self, method='none',inputType='HARD'):
		if method =='none':
			if inputType != 'HARD':
				raise NameError('Not Implemented')
			else:
				self.method = 'none'
				self.inputType = 'HARD'
		else:
			raise NameError('Not Implemented')

	def Decode(self, data):
		if self.method =='none' and self.inputType =='HARD':
			return (data)
		else:
			raise NameError('Not Implemented')


def loadCharacterSet(SetName):
	fullName = 'src/CharacterSets/'+SetName+'.txt'
	file = open(fullName,'r')
	fullSet = file.read()
	validChars = fullSet.split(',')
	return (validChars)


def breakString(string, brokenLength):
	# Ensure that the string can be broken in equal lengths
	numSubs = len(string)/brokenLength
	brokenData = []
	for i in range(numSubs):
		brokenData = brokenData + [string[i*brokenLength:brokenLength*(i+1)]]
	return (brokenData)


class sourceDecoder:
	def __init__(self, CharSet, method='basic'):
		if method == 'basic':
			alphabetSize = len(CharSet)
			self.CodeLength = int(math.ceil(math.log(alphabetSize,2)))
			self.alphabet = CharSet
		else :
			raise NameError ('Not implemented')

	def Decode(self,data):
		splitData = breakString(data, self.CodeLength)
		String = ""
		for elem in splitData:
			String = String + self.alphabet[int(elem,2)]
		return(String)
