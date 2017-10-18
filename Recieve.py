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
import time
import Source.Channel as CH
import Source.RecvSideLib as RL 
import Source.Frequency_Determination as FD


## DEFINE PARAMETERS ###########
CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 5
SourceEncodeMethod = 'basic'
errorCorrection = 'HardHamming'
FEC_Size = 7
FEC_Rate = float(4)/7
# Choose frequencies matching those on the sender side exactly from set:
# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
#  34.48, 35.71, 37.04, 38.46 ]
TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
TimePerSymbolSeconds = 4

ChannelSource = 'Emokit'
FlushBuffer = True
Electrodes = ['O1']
DetectionMethod = 'PSDA'
DecisionType = 'HARD'
syncMethod = 'HeaderV2'
FileWrite = True
readFileName = None

################################

# the actual frequencies are the closest FFT bins to a particular sender Freq
TransmissionFrequenciesActual = FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal, 128*TimePerSymbolSeconds)
print(TransmissionFrequenciesActual)

EEGChannel = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = readFileName, useHeader = True, holdFreq = 28.57, headerFreq = 30.30, startThreshold = 300,startThresholdRelative=0.8, crossoverThresholdRelative=0.5)

Detector = RL.DetectionObject(DetectionMethod,TransmissionFrequenciesActual, None, Electrodes ,TimePerSymbolSeconds, DecisionType)
CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection,'HARD',FEC_Size,FEC_Rate)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)


recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(TransmissionFrequenciesActual), FEC_Size, FEC_Rate, CharactersPerMessage, len(CharSet))
print(recordTime)
recordTime = int(recordTime)

while True:
	EEGChannel.waitForStart(syncMethod)
	data = EEGChannel.getDataBlock(recordTime, FlushBuffer)
	Symbols = Detector.getSymbols(data)
	print(Symbols)
	Encoded = RL.Demapper(Symbols,len(TransmissionFrequenciesActual), DecisionType)
	print(Encoded)
	Decoded = CD.Decode(Encoded)
	String = SD.Decode(Decoded)
	print(String)
