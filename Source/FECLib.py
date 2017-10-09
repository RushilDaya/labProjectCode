
import numpy as np


def ValidHamming(blkSize, rate):
	# for hamming code, determine if a particular block size 
	# and code rate is possible based on what has been implemented
	if blkSize ==1 and rate == 1:
		#case that no FEC is happing a control case
		return (True)
	else:
		return (False)

def HardHammingEncode(data): #, blkSize, rate):
	#if blkSize == 1 and rate == 1:
	#	return (data)
	if (len(data)%4) != 0:
		for i in range(0,4-len(data)%4):
			data += '0' # append(0)
	#Split data - known message length = 4
	sp_data = []
	c = 0
	num_words = len(data)/4 
	words = np.zeros((num_words,4))
	for i in range(0, num_words):
		for j in range(0,4):
			words[i,j] = float(data[c])
			c = c+1	
	
	##Hamming (7,4) code
	g =  np.array([[1, 0, 0, 0, 0, 1, 1],[0, 1, 0, 0, 1, 0, 1],[0, 0, 1, 0, 1, 1, 0],[0, 0, 0, 1, 1, 1, 1]])
	enc_data = ''
	for i in range (0, num_words):
		#print 'KKKKK: ', words[i]
		msg = (np.dot(words[i,:],g)%2)
		for j in range(0, len(msg)):
			enc_data = enc_data + (str(int(msg[j])))
	
	return enc_data
	
def correctErr(syn,recv,h):
	h_trans = h.T
	rows = h_trans.shape[0]
	#print 'Receive: ', (syn)
	if np.all([syn == [0,0,0]]) == True:
		return recv[0,:4]
	else:
		for i in range(0,rows-1):
			if np.all([syn == h_trans[i]]) == True:
				recv[0,i] = (recv[0,i]+1)%2
		return recv[0,:4]
	
def HardHammingDecode(data):
	data_np = np.zeros((1,len(data)))
	for i in range(0,len(data)):
		data_np[0,i] = int(data[i])
	
	#data_np = np.array(data)
	h = np.array([[0, 0, 0, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1, 1],[1, 0, 1, 0, 1, 0, 1]])
	
	#print 'OOOOO: ', data_np
	#print 'OOOOs: ', (data)
	
	syn = np.dot(data_np,h.T)%2 

	#print 'Syndrome: ', (data_np.shape)
	dec_msg = correctErr(syn,data_np,h)
	#print 'Dec_msg: ', (dec_msg[0])
	dec_data = '' 
	for i in range(0,len(dec_msg)):
	#	print 'AA: ', dec_data
		dec_data = dec_data + str(int(dec_msg[i]))
		
	#print 'Decoded: ', dec_data
		
	return dec_data

	