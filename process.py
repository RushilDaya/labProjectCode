import Source.InputLib  as IL
import time
import math
import Source.Channel as CH
import Source.RecvSideLib as RL 

CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 3
SourceEncodeMethod = 'basic'
errorCorrection = 'HardHamming'
###########################

ValidDictionary = IL.loadCharacterSet(CharSet)
InputValidationObject = IL.InputValidation(ValidDictionary,CharactersPerMessage)
SrcEncoder  = IL.SrcEncoder(ValidDictionary , SourceEncodeMethod)
FEC = IL.ChannelEncoder(errorCorrection, 7 , 4/7)

## DEFINE PARAMETERS ###########
#CharSet = 'lowerCaseLiterals'
#CharactersPerMessage = 3
#SourceEncodeMethod = 'basic'
#errorCorrection = 'HardHamming'
FEC_Size = 7
FEC_Rate = float(4)/7


################################


CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection,'HARD', FEC_Size, FEC_Rate)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)

while 1:
	sendString = InputValidationObject.getInput()
	SendBits = SrcEncoder.EncodeData(sendString)
	print 'Sendbits: ', SendBits
	EncBits = FEC.EncodeData(SendBits)
	print 'EncBits:', EncBits
	Symbols  = IL.SymbolMapping(EncBits, 4)
	print 'Symbols: ', Symbols
	Encoded = RL.Demapper(Symbols,4, 'HARD')
	print 'Encoded: ', Encoded
	Decoded = CD.Decode(Encoded)
	print 'Decoded: ', Decoded
	String = SD.Decode(Decoded)
	print 'String: ', String
