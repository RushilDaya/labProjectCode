
import Source.InputLib  as IL
import time
import math
import Source.Channel as CH
import Source.RecvSideLib as RL 

CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 7
SourceEncodeMethod = 'basic'
errorCorrection = 'HardHamming'

FEC_blockSize = 7
FEC_msgSize = 4

###########################

ValidDictionary = IL.loadCharacterSet(CharSet)
InputValidationObject = IL.InputValidation(ValidDictionary,CharactersPerMessage)
SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
FEC = IL.ChannelEncoder(errorCorrection, FEC_blockSize , FEC_msgSize)

## DEFINE PARAMETERS ###########
#CharSet = 'lowerCaseLiterals'
#CharactersPerMessage = 3
#SourceEncodeMethod = 'basic'
#errorCorrection = 'HardHamming'
#FEC_Size = 7
#FEC_Rate = float(4)/7


################################


CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection,'HARD', FEC_blockSize, FEC_msgSize)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)

while 1:
	sendString = InputValidationObject.getInput()
	SendBits = SrcEncoder.EncodeData(sendString)
	print 'Sendbits: ', SendBits
	EncBits = FEC.EncodeData(SendBits)
	print 'EncBits:', (EncBits)
	IntBits = FEC.interleave(EncBits)
	print 'IntBITS: ', (IntBits)
	Symbols  = IL.SymbolMapping(IntBits, 4)
	print 'Symbols: ', (Symbols)
	
	
	Encoded = RL.Demapper(Symbols,4, 'HARD')
	print 'Encoded: ', (Encoded)
	DeintBits = CD.de_interleave(Encoded)
	print 'DEint Bits: ',(DeintBits)
	Decoded = CD.Decode(DeintBits)
	print 'Decoded: ', Decoded
	String = SD.Decode(Decoded)
	print 'String: ', String





'''
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
import Source.Frequency_Determination as FD

import csv
import numpy

## DEFINE PARAMETERS ###########
CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 4
SourceEncodeMethod = 'basic'
errorCorrection = 'HardHamming'
FEC_blockSize = 7
FEC_msgSize = 4
# Choose frequencies matching those on the sender side exactly from set:
# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
#  34.48, 35.71, 37.04, 38.46 ]
TransmissionFrequenciesIdeal = [25, 23.81, 28.57, 33.33]
TimePerSymbolSeconds = 4

ChannelSource = 'File'
FlushBuffer = True
Electrodes = ['O1', 'O2', 'P7', 'P8']
DetectionMethod = 'Combined'
DecisionType = 'HARD'
syncMethod = 'KeyPress'
FileWrite = False
readFileName = '20171009-170644.csv' #'20171009-182912.csv'

################################
filetwo = '20171009-182912.csv'
EEGChannel2 = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = filetwo)

################################

# the actual frequencies are the closest FFT bins to a particular sender Freq
TransmissionFrequenciesActual =[23.25, 25, 28.5, 33.25]# FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal, 128*TimePerSymbolSeconds)
print(TransmissionFrequenciesActual)

EEGChannel = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = readFileName)

Detector = RL.DetectionObject(DetectionMethod,TransmissionFrequenciesActual, None, Electrodes ,TimePerSymbolSeconds, DecisionType)
Detector2 = RL.DetectionObject('CCA',TransmissionFrequenciesActual, None, Electrodes ,TimePerSymbolSeconds, DecisionType)

CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection,'HARD',FEC_blockSize,FEC_msgSize)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)


recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(TransmissionFrequenciesActual), FEC_blockSize, FEC_msgSize, CharactersPerMessage, len(CharSet))
print '9999999: ', recordTime
recordTime = int(recordTime)

#while True:
	#EEGChannel.waitForStart(syncMethod)
data = EEGChannel.getDataBlock(recordTime, FlushBuffer)
target_data = EEGChannel2.getDataBlock(recordTime,FlushBuffer)
#remove mean
target_data = target_data - numpy.mean(target_data)	
data = data - numpy.mean(data)

#bo = Detector.get_knn_data(target_data, data)

Symbols2 = Detector2.getSymbols(data)
Symbols = Detector.getSymbols(target_data)    # find_knn()  #getSymbols(data)

print(Symbols)
print(Symbols2)
#Encoded = RL.Demapper(Symbols,len(TransmissionFrequenciesActual), DecisionType)
#Decoded = CD.Decode(Encoded)
#String = SD.Decode(Decoded)

Encoded2 = RL.Demapper(Symbols2,len(TransmissionFrequenciesActual), DecisionType)
Decoded2 = CD.Decode(Encoded2)
String2 = SD.Decode(Decoded2)

#print(String)
print('AAA: ', String2)

'''
