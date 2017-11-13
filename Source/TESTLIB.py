import os
import InputLib  as IL
import RecvSideLib as RL 
import time

def makePath(user, ttype, run):
	path = os.getcwd()
	path  = path +'\\results\\' +user + '\\' + ttype + '\\Run' + str(run)
	return (path)




	recordStartTime = time.time()
	channel.flushBuffer()
	DataBlock = channel.getDataBlock(recordTime, False)
	symbolsCCA = detectorCCA.getSymbols(DataBlock)
	symbolsPSDA = detectorPSDA.getSymbols(DataBlock)
	intCCA = RL.Demapper(symbolsCCA,len(actualFrequencies),'HARD')
	intPSDA = RL.Demapper(symbolsCCA,len(actualFrequencies),'HARD')
	encodedCCA = channelDecoder.de_interleave(intCCA)
	encodedPSDA = channelDecoder.de_interleave(intPSDA)
	binaryCCA = channelDecoder.Decode(encodedCCA)
	binaryPSDA = channelDecoder.Decode(encodedPSDA)
	StringCCA = SrcDecoder.Decode(binaryCCA)
	StringPSDA = SrcDecoder.Decode(binaryPSDA)

def ReceiverSave(path, time='None', symCCA='None', symPSDA='None', intCCA='None', intPSDA='None', encCCA='None', encPSDA='None', binCCA='None', binPSDA='None', strCCA='None', strPSDA='None'):
	print(path)
	print(time)
	print(symCCA)
	print(symPSDA)
	print(intCCA)
	print(intPSDA)
	print(encCCA)
	print(encPSDA)
	print(binCCA)
	print(binPSDA)
	print(strCCA)
	print(strPSDA)
	filepath = path +'\\receive.txt'
	file = open(filepath, "wb")
	file.write(str(time)+'@')
	file.write(str(symCCA)+'@')
	file.write(str(symPSDA)+'@')
	file.write(str(intCCA)+'@')
	file.write(str(intPSDA)+'@')
	file.write(str(encCCA)+'@')
	file.write(str(encPSDA)+'@')
	file.write(str(binCCA)+'@')
	file.write(str(binPSDA)+'@')	
	file.write(str(strCCA)+'@')
	file.write(str(strPSDA)+'@')	
	file.close()



def SenderSave(path, message='None', binary='None', encodedBinary='None', interleaved='None', symbols='None', usedfrequencies='None', messageStartTime='None'):
	print(path)
	print(message)
	print(binary)
	print(encodedBinary)
	print(interleaved)
	print(symbols)
	print(usedfrequencies)
	print(messageStartTime)
	filepath = path +'\\sent.txt'
	file = open(filepath, "wb")
	file.write(message+'@')
	file.write(binary+'@')
	file.write(encodedBinary+'@')
	file.write(interleaved+'@')
	file.write(str(symbols)+'@')
	file.write(str(usedfrequencies)+'@')
	file.write(str(messageStartTime)+'@')
	file.close()


def quickRunSender(path, channel, fec, srcEnc, frequencies,option):

	if option == "1":
		message = raw_input('Enter message: ')
		sendBits = srcEnc.EncodeData(message)
		encBits = fec.EncodeData(sendBits)
		intBits = fec.interleave(encBits)
		symbols = IL.SymbolMapping(intBits, len(frequencies))
		channel.sendHeaderV2()
		_time = time.time()
		for symbol in symbols:
			channel.send(symbol)
		channel.re_header()
		SenderSave(path, message, sendBits, encBits, intBits, symbols, frequencies, _time)

	elif option =="2":
		message = raw_input('Enter message: ')
		time.sleep(5)
		sendBits = srcEnc.EncodeData(message)
		encBits = fec.EncodeData(sendBits)
		intBits = fec.interleave(encBits)
		symbols = IL.SymbolMapping(intBits, len(frequencies))
		for symbol in symbols:
			channel.send(symbol)
		channel.re_header()

		SenderSave(path, message, sendBits, encBits, intBits, symbols, frequencies)


	else:
		channel.sendHeaderV2()
		_time = time.time()
		channel.re_header()
		SenderSave(path, messageStartTime = _time)


def quickRunReceiver(path, channel, detectorCCA, detectorPSDA, channelDecoder, SrcDecoder, recordTime, actualFrequencies):
	recordStartTime = time.time()
	channel.flushBuffer()
	DataBlock = channel.getDataBlock(recordTime, False)
	if recordTime > 1: # hack meaning we are actually recording data
		symbolsCCA = detectorCCA.getSymbols(DataBlock)
		symbolsPSDA = detectorPSDA.getSymbols(DataBlock)
		intCCA = RL.Demapper(symbolsCCA,len(actualFrequencies),'HARD')
		intPSDA = RL.Demapper(symbolsPSDA,len(actualFrequencies),'HARD')
		encodedCCA = channelDecoder.de_interleave(intCCA)
		encodedPSDA = channelDecoder.de_interleave(intPSDA)
		binaryCCA = channelDecoder.Decode(encodedCCA)
		binaryPSDA = channelDecoder.Decode(encodedPSDA)
		StringCCA = SrcDecoder.Decode(binaryCCA)
		StringPSDA = SrcDecoder.Decode(binaryPSDA)
		ReceiverSave(path,recordStartTime, symbolsCCA, symbolsPSDA, intCCA, intPSDA, encodedCCA, encodedPSDA, binaryCCA, binaryPSDA, StringCCA, StringPSDA)
	else:
		ReceiverSave(path,recordStartTime)