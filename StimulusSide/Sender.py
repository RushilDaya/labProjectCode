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

import src.InputLib  as IL

ValidDictionary = IL.loadCharacterSet('lowerCaseLiterals')
InputValidationObject = IL.InputValidation(ValidDictionary,10)
SrcEncoder  = IL.SrcEncoder(ValidDictionary , 'basic')
FEC = IL.ChannelEncoder('none')
Chan = IL.Channel('FixedFrequencyAndDuty',[28, 30, 32, 34],1)

while True:
	sendString = InputValidationObject.getInput()
	SendBits = SrcEncoder.EncodeData(sendString)
	print(SendBits)
	EncBits = FEC.EncodeData(SendBits)
	print(EncBits)
	Symbols  = IL.SymbolMapping(EncBits,4)
	print(Symbols)
	Chan.send(Symbols)


