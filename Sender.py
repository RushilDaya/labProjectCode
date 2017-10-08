# Sender Side Frame Work Script

# this script is a sender Side client which allows for the user
# to send data in a from keyboard input to the LED output
# this script is a framework and allows modules to change

#PseudoCode:
# Init Variables
# Enter Loop:
#	get user Input
#	Encode stream to bits 
#	Perform FEC 
#	Send Data to the Serial Out Module
#	wait for stream to finish
#	

import Source.InputLib  as IL
import time

## DEFINE PARAMETERS ######
CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 4
SourceEncodeMethod = 'basic'
errorCorrection = 'none'

# NOTE: Only use frequencies From the following Set:
# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
#  34.48, 35.71, 37.04, 38.46 ]
TransmissionFrequenciesIdeal = [23.26, 25, 28.57, 33.33]

TimePerSymbolSeconds = 4
###########################

ValidDictionary = IL.loadCharacterSet(CharSet)
InputValidationObject = IL.InputValidation(ValidDictionary,CharactersPerMessage)
SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
FEC = IL.ChannelEncoder(errorCorrection)
Chan = IL.Channel('FixedFrequencyAndDuty',TransmissionFrequenciesIdeal,TimePerSymbolSeconds)

while True:
	sendString = InputValidationObject.getInput()
	time.sleep(2)
	SendBits = SrcEncoder.EncodeData(sendString)
	print(SendBits)
	EncBits = FEC.EncodeData(SendBits)
	print(EncBits)
	Symbols  = IL.SymbolMapping(EncBits, len(TransmissionFrequenciesIdeal))
	print(Symbols)
	Chan.send(Symbols)
