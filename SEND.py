import Source.InputLib  as IL
import time
import os
import Source.TESTLIB  as TL

# change this for each participant
user = raw_input('Enter Subject ID :')

option = raw_input("1 - wholeSystem; 2 - transmissionOnly;  3 - timingOnly \n")
if option == "1":
	testType = 'WithSync'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage = 5
	SourceEncodeMethod = 'basic'
	errorCorrection = 'HardHamming'
	transFrequencies = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	period = 4
	ValidDictionary = IL.loadCharacterSet(CharSet)
	SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
	FEC = IL.ChannelEncoder(errorCorrection,7,4)
	Chan = IL.Channel('FixedFrequencyAndDuty',transFrequencies,period, True, 28.57,30.30)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		TL.quickRunSender(path,Chan, FEC, SrcEncoder,transFrequencies,option)

		



elif option == "2":
	testType = 'SelfSync'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage = 5
	SourceEncodeMethod = 'basic'
	errorCorrection = 'HardHamming'
	transFrequencies = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	period = 4
	ValidDictionary = IL.loadCharacterSet(CharSet)
	SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
	FEC = IL.ChannelEncoder(errorCorrection,7,4)
	Chan = IL.Channel('FixedFrequencyAndDuty',transFrequencies,period, False)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		TL.quickRunSender(path, Chan, FEC, SrcEncoder,transFrequencies,option)
		

else :
	testType = 'ProtocolTiming'
	CharSet = 'lowerCaseLiterals'
	CharactersPerMessage = 0
	SourceEncodeMethod = 'basic'
	errorCorrection = 'HardHamming'
	transFrequencies = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
	period = 4
	ValidDictionary = IL.loadCharacterSet(CharSet)
	SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
	FEC = IL.ChannelEncoder(errorCorrection,7,4)
	Chan = IL.Channel('FixedFrequencyAndDuty',transFrequencies,period, True, 28.57,30.30)
	while True:
		run = raw_input('Enter Run Number: ')
		path = TL.makePath(user, testType, run)
		TL.quickRunSender(path, Chan, FEC, SrcEncoder,transFrequencies,option)	








