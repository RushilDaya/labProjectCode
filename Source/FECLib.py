
import numpy as np
import math

def ValidHamming(blkSize, rate):
	# for hamming code, determine if a particular block size 
	# and code rate is possible based on what has been implemented
	if blkSize ==1 and rate == 1:
		#case that no FEC is happing a control case
		return (True)
	else:
		return (False)

class hammingCode:		

	def __init__(self,blockSize, msgSize):
		self.blockSize = blockSize #int(math.pow(2,self.m)) - 1
		self.msgSize = msgSize #int(math.pow(2,self.m)) - self.m - 1
		self.m = self.blockSize - self.msgSize
		self.codeRate = float(self.msgSize)/self.blockSize
		self.gen_mat = None
		self.h_mat = None
		self.synd = None
		self.get_gen_mat()
		
		#print 'AAAA; ', self.codeRate
		
	def get_gen_mat(self):
		if ((self.blockSize == 7) and (self.msgSize == 4)):
			self.gen_mat = np.array([[1, 0, 0, 0, 0, 1, 1],[0, 1, 0, 0, 1, 0, 1],[0, 0, 1, 0, 1, 1, 0],[0, 0, 0, 1, 1, 1, 1]])
			self.h_mat = np.array([[0, 0, 0, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1, 1],[1, 0, 1, 0, 1, 0, 1]])
			self.synd = [0,0,0]
		elif ((self.blockSize == 15) and (self.msgSize == 11)):
			self.gen_mat = np.array([[1,1,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,1,1,0,0,1,0,0,0,0,0,0,0,0,0],[0,0,1,1,0,0,1,0,0,0,0,0,0,0,0],[1,1,0,1,0,0,0,1,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,1,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0,1,0,0,0,0,0],[1,1,1,0,0,0,0,0,0,0,1,0,0,0,0],[0,1,1,1,0,0,0,0,0,0,0,1,0,0,0],[1,1,1,1,0,0,0,0,0,0,0,0,1,0,0],[1,0,1,1,0,0,0,0,0,0,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,0,0,0,0,0,1]])
			self.h_mat = np.array([[1,0,0,0,1,0,0,1,1,0,1,0,1,1,1],[0,1,0,0,1,1,0,1,0,1,1,1,1,0,0],[0,0,1,0,0,1,1,0,1,0,1,1,1,1,0],[0,0,0,1,0,0,1,1,0,1,0,1,1,1,1]])
			self.synd = [0,0,0,0]
		elif ((self.blockSize == 9) and (self.msgSize == 4)):
			self.gen_mat = np.array([[1,0,0,0,1,0,1,0,1],[0,1,0,0,1,0,0,1,1],[0,0,1,0,0,1,1,0,1],[0,0,0,1,0,1,0,1,1]])
			self.h_mat = np.array([[1,1,0,0,1,0,0,0,0],[0,0,1,1,0,1,0,0,0],[1,0,1,0,0,0,1,0,0],[0,1,0,1,0,0,0,1,0],[1,1,1,1,0,0,0,0,1]])
			self.synd = [0,0,0,0,0]
		elif ((self.blockSize == 5) and (self.msgSize == 3)):
			self.gen_mat = np.array([[1,0,1,1,0],[1,1,0,1,0],[0,1,0,0,1]]) #np.array([[1,0,0,0,0,1],[0,1,0,0,0,1],[0,0,1,0,0,1],[0,0,0,1,0,1],[0,0,0,0,1,1]])
			self.h_mat =  np.array([[1,0,0,1,0],[1,1,1,0,1]]) #np.array([1,1,1,1,1,1])
			self.synd = [0,0]
		else:
			#raise Error('Hamming code Not Implemented')
			self.blockSize = 1
			self.msgSize = self.blockSize
			self.codeRate = 1
	
	def HardHammingEncode(self, data): #, blkSize, rate):
		if self.blockSize == 1 and self.codeRate == 1:
			return (data)
			
		if (len(data)%self.msgSize) != 0:
			for i in range(0, self.msgSize-len(data)%self.msgSize):
				data += '0' # append(0)
		#Split data - known message length = 4
		#sp_data = []
		c = 0 
		num_words = len(data)/self.msgSize
		words = np.zeros((num_words,self.msgSize))
		for i in range(0, num_words):
			for j in range(0,self.msgSize):
				words[i,j] = float(data[c])
				c = c+1	
				
		enc_data = ''
		for i in range (0, num_words):
			msg = (np.dot(words[i,:],self.gen_mat)%2)
			for j in range(0, len(msg)):
				enc_data = enc_data + (str(int(msg[j])))
		return enc_data
	
	def correctErr(self,syn,recv):
		h_trans = self.h_mat.T
		rows = h_trans.shape[0]

		if np.all([syn == self.synd]) == True:
			if self.blockSize == 7:
				return recv[0,:self.msgSize]
			elif self.blockSize == 15:
				return recv[0,self.m:]
			elif self.blockSize == 9:
				return recv[0,:self.msgSize]
			else:
				return recv[0,:self.msgSize]
		else:
			for i in range(0,rows-1):
			#	print '55555: ', recv
				if np.all([syn == h_trans[i]]) == True:
					recv[0,i] = (recv[0,i]+1)%2
					
			if self.blockSize == 7:
				return recv[0,:self.msgSize]
			elif self.blockSize == 15:
				return recv[0,self.m:]
			elif self.blockSize == 9:
				return recv[0,:self.msgSize]
			else:
			#	print '66666: ', recv
				return recv[0,self.m:]
	
	def HardHammingDecode(self,data):
		data_np = np.zeros((1,len(data)))
		for i in range(0,len(data)):
			data_np[0,i] = int(data[i])
	
	
		syn = np.dot(data_np,self.h_mat.T)%2
		#print 'SSSSS: ', syn 
		dec_msg = self.correctErr(syn,data_np)
	
		dec_data = '' 
		for i in range(0,len(dec_msg)):
			dec_data = dec_data + str(int(dec_msg[i]))
		
		return dec_data
		

	