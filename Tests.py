import unittest
import numpy as np 
import Source.InputLib as IL
import Source.RecvSideLib as RL
import Source.Frequency_Determination as  FD


class TestSrcEncoder(unittest.TestCase):

	def  test_EncodeSingleCharacterBasic(self):
		CharSet = IL.loadCharacterSet('lowerCaseLiterals')
		SrcEnc  = IL.SrcEncoder(CharSet,'basic')
		SendMessage1 = 'a'
		SendMessage2 = 'k'
		SendMessage3 = 'z'
		self.assertEqual('00001', SrcEnc.EncodeData(SendMessage1))
		self.assertEqual('01011', SrcEnc.EncodeData(SendMessage2))
		self.assertEqual('11010', SrcEnc.EncodeData(SendMessage3))

	def test_EncodeLongData(self):
		CharSet = IL.loadCharacterSet('lowerCaseLiterals')
		SrcEnc = IL.SrcEncoder(CharSet,'basic')
		sendMessage = 'ajyajyajyajy'
		EncDat = '000010101011001000010101011001000010101011001000010101011001'
		self.assertEqual(EncDat, SrcEnc.EncodeData(sendMessage))

class TestSrcDecoder(unittest.TestCase):
	def test_DecodeShortMessage(self):
		chars = IL.loadCharacterSet('lowerCaseLiterals')
		SrcDec = RL.sourceDecoder(chars, 'basic')
		self.assertEqual('yj',SrcDec.Decode('1100101010'))

	def test_DisregardAdditionalBits(self):
		# any bits added by the FEC will be disregarded
		# unless they can create a full character  
		chars = IL.loadCharacterSet('lowerCaseLiterals')
		SrcDec = RL.sourceDecoder(chars, 'basic')
		self.assertEqual('yj',SrcDec.Decode('11001010100000'))		

class TestSymbolMapper(unittest.TestCase):
	def test_mapToNsymbolsNoPadding(self):
		message = '1000111010101110'
		TwoSymbols = IL.SymbolMapping(message,2)
		self.assertEqual(TwoSymbols,[1,0,0,0,1,1,1,0,1,0,1,0,1,1,1,0])
		FourSymbols = IL.SymbolMapping(message,4)
		self.assertEqual(FourSymbols,[2,0,3,2,2,2,3,2])
		message = '100011100'
		EightSymbols = IL.SymbolMapping(message,8)
		self.assertEqual(EightSymbols, [4,3,4])

	def test_mapToSymbolsWithPadding(self):
		message = '1000111'
		EightSybols = IL.SymbolMapping(message,8)
		self.assertEqual(EightSybols, [4,3,4])
		# the following will be padded to '110'-> 6
		message = '11'
		EightSybols = IL.SymbolMapping(message,8)
		self.assertEqual(EightSybols, [6])		
		message ='0'
		FourSymbols = IL.SymbolMapping(message,4)
		self.assertEqual(FourSymbols,[0])

class TestSymbolAndSource(unittest.TestCase):
	def test_doubleFunctionality(self):
		message = 'helloworld'
		chars = IL.loadCharacterSet('lowerCaseLiterals')
		srcEncoder = IL.SrcEncoder(chars,'basic')
		srcDecoder = RL.sourceDecoder(chars,'basic')
		binMessage = srcEncoder.EncodeData(message)
		symbols = IL.SymbolMapping(binMessage, 4)
		recBin = RL.Demapper(symbols,4,'HARD')
		recvMessage = srcDecoder.Decode(recBin)
		self.assertEqual(message, recvMessage)

class TestReceiveTimeCalculate(unittest.TestCase):
	def test_calculate_no_FEC(self):
		Sym_Period = 4
		Num_Symbols = 4
		FEC_blockSize = 1
		FEC_msgSize = 1
		Num_Characters = 4
		AlpaLength = 26
		calcTime = RL.calculateRecvTime(Sym_Period, Num_Symbols, FEC_blockSize, FEC_msgSize, Num_Characters, AlpaLength)
		self.assertEqual(calcTime, 40.0)

		Num_Symbols = 16
		calcTime = RL.calculateRecvTime(Sym_Period, Num_Symbols, FEC_blockSize, FEC_msgSize, Num_Characters, AlpaLength)
		self.assertEqual(calcTime, 20.0)

	def test_calcualte_with_FEC(self):
		Sym_Period = 4
		Num_Symbols = 4
		FEC_blockSize = 2
		FEC_msgSize = 1
		Num_Characters = 4
		AlpaLength = 26
		calcTime = RL.calculateRecvTime(Sym_Period, Num_Symbols, FEC_blockSize, FEC_msgSize, Num_Characters, AlpaLength)
		self.assertEqual(calcTime, 80.0)	

		FEC_blockSize = 15
		FEC_msgSize = 9	
		calcTime = RL.calculateRecvTime(Sym_Period, Num_Symbols, FEC_blockSize, FEC_msgSize, Num_Characters, AlpaLength)
		self.assertEqual(calcTime, 92.0 )	

class TestFreqDetermination(unittest.TestCase):
	def test_GetsCorrectUpAndDown(self):
		self.assertEqual(FD.SenderGetUpAndDown(23.26),[18, 25])
		self.assertEqual(FD.SenderGetUpAndDown(25),[16, 24])
		self.assertEqual(FD.SenderGetUpAndDown(38.46),[13, 13])
	def test_MapsToClosest(self):
		freqs = [23.26, 25, 29.41, 35.71, 25.64]
		self.assertEqual(FD.mapToClosestFrequencies(freqs, 128),[23,25,29,36,26])
		self.assertEqual(FD.mapToClosestFrequencies(freqs, 256),[23.5,25,29.5,35.5,25.5])		
		self.assertEqual(FD.mapToClosestFrequencies(freqs, 384),[23.33,25,29.33,35.66,25.66])	
		self.assertEqual(FD.mapToClosestFrequencies(freqs, 512),[23.25,25,29.5,35.75,25.75])	


if __name__ == '__main__':
	unittest.main()