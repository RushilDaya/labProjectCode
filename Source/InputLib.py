import math
import time
import serial
import Frequency_Determination as FD

import FECLib as fec


def loadCharacterSet(SetName):
	fullName = 'Source/CharacterSets/'+SetName+'.txt'
	file = open(fullName,'r')
	fullSet = file.read()
	validChars = fullSet.split(',')
	return (validChars)


class InputValidation:
	# prompts the user for a valid input
	def __init__(self,CharSet, MaxLength, padWithLastChar = True):
		self.set = CharSet
		self.recvState = False
		self.maxLength = MaxLength
		self.pad  = padWithLastChar

	def inputRecv(self):
		return(self.recvState)

	def reset(self):
		self.recvState = False

	def getInput(self):
		self.reset()
		while self.recvState == False:
			self.recvState = True
			msg = raw_input("Enter Message: ")
			if len(msg) > self.maxLength:
				print ('Input Message too long')
				self.recvState = False
			else :
				msgLength = len(msg)
				for   index in range(msgLength):
					if msg[index] not in self.set:
						print('Message Contains invalid Character: '+msg[index])
						self.recvState = False


		# if the message does not take up the entire expected block
		# it will be padded with the last character in the alphabet
		if self.pad == True:
			msg = msg + (self.set[len(self.set)-1])*(self.maxLength - len(msg))


		return(msg)




def NumToBin(number, outStringLength):
	binNum = bin(number)
	binNum = binNum[2:]
	zeroPadLength = int(outStringLength-len(binNum))
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
			for i in range(len(self.charset)):
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
	def __init__(self, method, blockSize=None, rate=None):
		if method == 'none':
			self.method = 'none'
			self.blockSize = 0
			self.codeRate = 0
		elif method == 'HardHamming':
			self.method = 'HardHamming'
			self.blockSize = blockSize
			self.codeRate = rate
		else:
			raise NameError('Invalid Method to Channel Encoder')

	def EncodeData(self, data):
		if self.method == 'none':
			return(data)
		elif self.method == 'HardHamming':
			return fec.HardHammingEncode(data)
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
		highTimeInMilliseconds = (round(duty*roundedPeriod));
		lowTimeInMilliseconds =  (roundedPeriod - highTimeInMilliseconds)

		UpTimeString = 'u'+str(int(highTimeInMilliseconds))+'\n'
		DownTimeString = 'd'+str(int(lowTimeInMilliseconds))+'\n'
		ActualPeriod =  highTimeInMilliseconds+lowTimeInMilliseconds
		print('Actual Transmit Freq: '+str(1000/ActualPeriod))
		self.Connection.write(str(UpTimeString))
		self.Connection.write(str(DownTimeString))
		return True

	def setUpDown(self, UpDownList):
		UpTimeString = 'u'+str(UpDownList[0])+'\n'
		DownTimeString = 'd'+str(UpDownList[1])+'\n'
		print('Send Freq: '+str(float(1000)/(UpDownList[0]+UpDownList[1]))+' Send Duty: '+str(float(UpDownList[0])/(UpDownList[1]+UpDownList[0])))
		self.Connection.write(str(UpTimeString))
		self.Connection.write(str(DownTimeString))
		return True



	def singleDutyPhase(self, freq, phaseIndex):
		# qPeriod = round(0.25*(1000/freq))
		# comStr = phaseIndex+str(qPeriod)+'\n'
		# self.Connection.write(bytes(comStr,'ASCII'))
		return True




class Channel:
	# the channel is the arduino system. 
	# ie data sent to the channel is serially sent to the arduino 
	# refactor this to inheritance later
	def __init__(self,ArdScript, UsedFrequencies, SymbolPeriod, header = False, holdFrequency =None, headerFrequency = None):
		self.ArdScript = ArdScript
		self.SerialObj  = serialCommObj('COM6',9600)
		time.sleep(1)
		self.f1 = holdFrequency
		self.f2 = headerFrequency
		self.header = header
		if ArdScript =='FixedFrequencyAndDuty':
			if self.header == False:
				self.SerialObj.setFreqAndDuty(100,0) # effectively an off state
			else:
				self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1)) # setting the hold frequency
		else:
			raise NameError ('Channel Model unimplemented')
		self.FrequencySet = UsedFrequencies
		self.SymbolPeriod = SymbolPeriod

	def setFrequencySetAndTime(self, newFreqs, newPeriod):
		self.FrequencySet = newFreqs
		self.SymbolPeriod = newPeriod


	def sendHeader(self):
		# the header is the sender side of a protocol when a autostart and sync are required
		# the protocol is non-trivial and may not be easily understood in code
		# Supporting documents are provided which explain the protocol
		print('===START HEADER===')
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f2))
		time.sleep(8)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1))
		time.sleep(4)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f2))
		time.sleep(1)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1))
		time.sleep(4)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f2))
		time.sleep(1)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1))
		time.sleep(4)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f2))
		time.sleep(1)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1))
		time.sleep(4)
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f2))
		time.sleep(4)
		print('===END HEADER===')




	def send(self,SymbolList):
		if self.header == True :
			self.sendHeader()
		print('=== START MESSAGE ===')
		print(time.time())
		for Symbol in SymbolList:
			self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.FrequencySet[Symbol]))
			time.sleep(self.SymbolPeriod)
		print('=== END MESSAGE ===')
		if self.header == False:
			self.SerialObj.setFreqAndDuty(100, 0)	
		else :
			self.SerialObj.setFreqAndDuty(100, 0)
			time.sleep(3)
			self.SerialObj.setUpDown(FD.SenderGetUpAndDown(self.f1)) # reset

	def setSingleFreq(self, SingleFrequency):
		# used in the calibration
		self.SerialObj.setUpDown(FD.SenderGetUpAndDown(SingleFrequency))