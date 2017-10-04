# Script which integrates the receiver side functionality.
# the reciever Should be run with python 2.7


#PseudoCode:
#	-Initialize communication parameters
#	-Load Users trainingData data
#	-Loop:
#		wait for start Signal
#		Collect data 
#		Send  raw data to detection algorithm get Prob data
#		Decode the data
#		Display the decoded Result
import math
import Source.Channel as CH
import Source.RecvSideLib as RL 


## DEFINE PARAMETERS ###########
CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 4
SourceEncodeMethod = 'basic'
errorCorrection = 'none'
TransmissionFrequenciesActual = [23.8, 26.3, 27.7, 30.3]
TimePerSymbolSeconds = 4

ChannelSource = 'Emokit'
FlushBuffer = True
Electrodes = ['O1']
DetectionMethod = 'PSDA'
DecisionType = 'HARD'
syncMethod = 'KeyPress'
FileWrite = True
readFileName = None

recordTime = 40
################################


EEGChannel = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = readFileName)
#[trash1, trash2 ,UserWeights] = RL.getUserData('PSDA','dummy')

Detector = RL.DetectionObject(DetectionMethod,TransmissionFrequenciesActual, None, Electrodes ,4, DecisionType)
CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)



# numBits = int(math.ceil(math.log(len(CharSet),2))*CharactersPerMessage)
# bitsPerSymbol = int(math.log(len(TransmissionFrequenciesActual),2))
# numSymbols = numBits/bitsPerSymbol
# recordTime = TimePerSymbolSeconds*numSymbols
print(recordTime)

while True:
	EEGChannel.waitForStart(syncMethod)
	data = EEGChannel.getDataBlock(recordTime, FlushBuffer)
	Symbols = Detector.getSymbols(data)
	print(Symbols)
	Encoded = RL.Demapper(Symbols,len(TransmissionFrequenciesActual), DecisionType)
	Decoded = CD.Decode(Encoded)
	String = SD.Decode(Decoded)
	print(String)



