import math
import time
import Source.Channel as CH
import Source.RecvSideLib as RL 
import Source.Frequency_Determination as FD
import numpy
import Source.TESTLIB as TL

user = raw_input('Enter Subject ID :')

option = raw_input("1 - wholeSystem; 2 - transmissionOnly;  3 - timingOnly \n")
if option == "1":
	testType = 'WithSync'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage =5
	SourceEncodeMethod='basic'
	errorCorrection = 'HardHamming'
	FEC_Size = 7
	FEC_msg = 4
	TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	TimePerSymbolSeconds = 4
	ChannelSource = 'Emokit'
	flushBuffer = True
	Electrodes = ['O1','O2','P7','P8']
	DecisionType = 'HARD'
	syncMethod = 'HeaderV2'
	fileWrite = True
	CharSet = RL.loadCharacterSet(CharSet)

	actualFrequencies = FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal,512)
	Channel = CH.Channel(ChannelSource, Electrodes, fileWrite, useHeader = True, holdFreq = 28.57, headerFreq = 30.30, startThreshold = 300, startThresholdRelative=0.8, crossoverThresholdRelative=0.5)
	DetectorCCA = RL.DetectionObject('CCA',actualFrequencies, None, Electrodes , TimePerSymbolSeconds, DecisionType)
	DetectorPSDA = RL.DetectionObject('PSDA', actualFrequencies, None,['O1'], TimePerSymbolSeconds, DecisionType)
	chnDecoder = RL.ChannelDecoder(errorCorrection,'HARD',FEC_Size, FEC_msg)
	srcDecoder = RL.sourceDecoder(CharSet, SourceEncodeMethod)

	recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(actualFrequencies), FEC_Size, FEC_msg, CharactersPerMessage, len(CharSet))
	recordTime = int(recordTime)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		Channel.setFileName(path+'\\raw.csv')
		Channel.gaze_detect()
		Channel.threshold_detect()
		TL.quickRunReceiver(path, Channel, DetectorCCA, DetectorPSDA, chnDecoder, srcDecoder, recordTime, actualFrequencies)




elif option =="2":
	testType = 'SelfSync'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage =5
	SourceEncodeMethod='basic'
	errorCorrection = 'HardHamming'
	FEC_Size = 7
	FEC_msg = 4
	TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	TimePerSymbolSeconds = 4
	ChannelSource = 'Emokit'
	flushBuffer = True
	Electrodes = ['O1','O2','P7','P8']
	DecisionType = 'HARD'
	syncMethod = 'KeyPress'
	fileWrite = True
	CharSet = RL.loadCharacterSet(CharSet)

	actualFrequencies = FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal,512)
	Channel = CH.Channel(ChannelSource, Electrodes, fileWrite, useHeader = False)
	DetectorCCA = RL.DetectionObject('CCA',actualFrequencies, None, Electrodes , TimePerSymbolSeconds, DecisionType)
	DetectorPSDA = RL.DetectionObject('PSDA', actualFrequencies, None,['O1'], TimePerSymbolSeconds, DecisionType)
	chnDecoder = RL.ChannelDecoder(errorCorrection,'HARD',FEC_Size, FEC_msg)
	srcDecoder = RL.sourceDecoder(CharSet, SourceEncodeMethod)

	recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(actualFrequencies), FEC_Size, FEC_msg, CharactersPerMessage, len(CharSet))
	recordTime = int(recordTime)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		Channel.setFileName(path+'\\raw.csv')
		Channel.waitForStart(syncMethod)
		TL.quickRunReceiver(path, Channel, DetectorCCA, DetectorPSDA, chnDecoder, srcDecoder, recordTime, actualFrequencies)


else :
	testType = 'ProtocolTiming'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage = 0
	SourceEncodeMethod='basic'
	errorCorrection = 'HardHamming'
	FEC_Size = 7
	FEC_msg = 4
	TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	TimePerSymbolSeconds = 4
	ChannelSource = 'Emokit'
	flushBuffer = True
	Electrodes = ['O1','O2','P7','P8']
	DecisionType = 'HARD'
	syncMethod = 'HeaderV2'
	fileWrite = False
	CharSet = RL.loadCharacterSet(CharSet)

	actualFrequencies = FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal,512)
	Channel = CH.Channel(ChannelSource, Electrodes, fileWrite, useHeader = True, holdFreq = 28.57, headerFreq = 30.30, startThreshold = 300, startThresholdRelative=0.8, crossoverThresholdRelative=0.5)
	DetectorCCA = RL.DetectionObject('CCA',actualFrequencies, None, Electrodes , TimePerSymbolSeconds, DecisionType)
	DetectorPSDA = RL.DetectionObject('PSDA', actualFrequencies, None,['O1'], TimePerSymbolSeconds, DecisionType)
	chnDecoder = RL.ChannelDecoder(errorCorrection,'HARD',FEC_Size, FEC_msg)
	srcDecoder = RL.sourceDecoder(CharSet, SourceEncodeMethod)

	recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(actualFrequencies), FEC_Size, FEC_msg, CharactersPerMessage, len(CharSet))
	recordTime = int(recordTime)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		Channel.setFileName(path+'\\raw.csv')
		Channel.gaze_detect()
		Channel.threshold_detect()
		TL.quickRunReceiver(path, Channel, DetectorCCA, DetectorPSDA, chnDecoder, srcDecoder, recordTime, actualFrequencies)

