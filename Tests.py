import unittest
import numpy as np 
import Source.InputLib as IL
import Source.RecvSideLib as RL


class TestSrcEncoder(unittest.TestCase):

	def  test_EncodeSingleCharacterBasic(self):
		CharSet = IL.loadCharacterSet('lowerCaseLiterals')
		SrcEnc  = IL.SrcEncoder(CharSet,'basic')
		SendMessage1 = 'a'
		SendMessage2 = 'k'
		SendMessage3 = 'z'
		self.assertEqual('00000', SrcEnc.EncodeData(SendMessage1))
		self.assertEqual('01010', SrcEnc.EncodeData(SendMessage2))
		self.assertEqual('11001', SrcEnc.EncodeData(SendMessage3))

	def test_EncodeLongData(self):
		CharSet = IL.loadCharacterSet('lowerCaseLiterals')
		SrcEnc = IL.SrcEncoder(CharSet,'basic')
		sendMessage = 'akzakzakzakz'
		EncDat = '000000101011001000000101011001000000101011001000000101011001'
		self.assertEqual(EncDat, SrcEnc.EncodeData(sendMessage))

if __name__ == '__main__':
	unittest.main()