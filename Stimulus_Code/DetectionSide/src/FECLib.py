# functions here are unoptimized

def ValidHamming(blkSize, rate):
	# for hamming code, determine if a particular block size 
	# and code rate is possible based on what has been implemented
	if blkSize ==1 and rate == 1:
		#case that no FEC is happing a control case
		return (True)
	else:
		return (False)

def HardHammingDecode(data, blkSize, rate):
	if blkSize == 1 and rate == 1:
		return (data)