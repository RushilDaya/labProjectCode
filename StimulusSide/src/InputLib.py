import math
import time
import serial


def loadCharacterSet(SetName):
	fullName = 'src/CharacterSets/'+SetName+'.txt'
	file = open(fullName,'r')
	fullSet = file.read()
	validChars = fullSet.split(',')
	return (validChars)


class InputValidation:
	# prompts the user for a valid input
	def __init__(self,CharSet, MaxLength):
		self.set = CharSet
		self.recvState = False
		self.maxLength = MaxLength

	def inputRecv(self):
		return(self.recvState)

	def reset(self):
		self.recvState = False

	def getInput(self):
		self.reset()
		while self.recvState == False:
			self.recvState = True
			msg = input("Enter Message: ")
			if len(msg) > self.maxLength:
				print ('Input Message too long')
				self.recvState = False
			else :
				msgLength = len(msg)
				for   index in range(msgLength):
					if msg[index] not in self.set:
						print('Message Contains invalid Character: '+msg[index])
						self.recvState = False
		return(msg)




def NumToBin(number, outStringLength):
	binNum = bin(number)
	binNum = binNum[2:]
	zeroPadLength = outStringLength-len(binNum)
	for i in range (zeroPadLength):
		binNum = '0'+binNum
	return(binNum)


class SrcEncoder:
	# the source encoder converts the strings to a bit stream based on the minimum 
	# bits required for a particular alphabet
	def __init__(self,CharSet, method):
		if method == 'basic': # the basic method accounts for no compression
			alphabetSize = len(CharSet)
			self.CodeLength  = math.ceil(math.log(alphabetSize, 2))
			self.charset = CharSet
			self.mapSet = []
			for i in range(len(CharSet)):
				self.mapSet = self.mapSet + [NumToBin(i,self.CodeLength)]
		else :
			raise NameError('method argument Not provided')

	def EncodeData(self,inputData):
		encodedString = ""
		for index in range(len(inputData)):
			char  = inputData[index]
			alphabetElement = self.charset.index(char)
			binary = self.mapSet[alphabetElement]
			encodedString += binary
		return(encodedString)


class ChannelEncoder:
	# object to add redundancy to the data 
	def __init__(self, method):
		if method == 'none':
			self.method = 'none'
			self.blockSize = 0
			self.codeRate = 0
		else:
			raise NameError('Invalid Method to Channel Encoder')

	def EncodeData(self, data):
		if self.method == 'none':
			return(data)
		else:
			raise nameError('Bad Method for Encoder')


def SymbolMapping(data, numSymbols):
	bitsPerSymbol = math.log(numSymbols,2)
	if bitsPerSymbol % 1 != 0:
		raise NameError('Number of symbols not a power of 2 - Fix')
	bitsPerSymbol = int(bitsPerSymbol)

	mismatchLength = len(data) % bitsPerSymbol 
	if mismatchLength != 0:
		print('data requires zero padding')
		data = data + '0'*(bitsPerSymbol - mismatchLength)
	brokenData = list(map(''.join,zip(*[iter(data)]*bitsPerSymbol)))
	symbols = []
	for binSymbol in brokenData:
		symbols = symbols +[int(binSymbol,2)]
	return (symbols)


class serialCommObj:
	def __init__(self, port, baud):
		self.Connection = serial.Serial(port,baud)
		time.sleep(2)

	def setFreqAndDuty(self,freq, duty):
		# maximum frequency is 500 Hz
		# duty is a fraction e [0:1]

		if duty > 1:
			duty = 1
		if duty < 0:
			duty = 1

		roundedPeriod = round(1000/freq)
		highTimeInMilliseconds = round(duty*roundedPeriod);
		lowTimeInMilliseconds = roundedPeriod - highTimeInMilliseconds

		UpTimeString = 'u'+str(highTimeInMilliseconds)+'\n'
		DownTimeString = 'd'+str(lowTimeInMilliseconds)+'\n'

		ActualPeriod =  highTimeInMilliseconds+lowTimeInMilliseconds
		print('Actual Transmit Freq: '+str(1000/ActualPeriod))
		self.Connection.write(bytes(UpTimeString,'ASCII'))
		self.Connection.write(bytes(DownTimeString,'ASCII'))
		return True

	def singleDutyPhase(self, freq, phaseIndex):
		qPeriod = round(0.25*(1000/freq))
		comStr = phaseIndex+str(qPeriod)+'\n'
		self.Connection.write(bytes(comStr,'ASCII'))
		return True




class Channel:
	# the channel is the arduino system. 
	# ie data sent to the channel is serially sent to the arduino 
	# refactor this to inheritance later
	def __init__(self,ArdScript, UsedFrequencies, SymbolPeriod):
		self.ArdScript = ArdScript
		self.SerialObj  = serialCommObj('COM6',9600)
		time.sleep(1)
		if ArdScript =='FixedFrequencyAndDuty':
			self.SerialObj.setFreqAndDuty(100,0) # effectively an off state
		else:
			raise NameError ('Channel Model unimplemented')
		self.FrequencySet = UsedFrequencies
		self.SymbolPeriod = SymbolPeriod

	def setFrequencySetAndTime(self, newFreqs, newPeriod):
		self.FrequencySet = newFreqs
		self.SymbolPeriod = newPeriod

	def send(self,SymbolList):
		for Symbol in SymbolList:
			self.SerialObj.setFreqAndDuty(self.FrequencySet[Symbol],0.5 )
			time.sleep(self.SymbolPeriod)
		self.SerialObj.setFreqAndDuty(100, 0)	







