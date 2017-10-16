# functions which simplify the choosing of stimulation frequencies
# this is based on an a set of valid frequencies determined externally to this
# code and is based on the experimental data




# format [[UpTime, DownTime, SendFreq, closet = 128, closest = 256, closest = 384, closest = 512, closest =640, closest = 768],..]

FreqLookUp = [[	18,	25,	23.26,	23,	23.5,	23.33,	23.25,	23.2,	23.33],
			[	17,	25,	23.81,	24,	24	,	23.66,	23.75,	23.8,	23.83],
			[	17,	24,	24.39,	24,	24.5,	24.33,	24.5,	24.4,	24.33],
			[	16,	24,	25.00,	25,	25	,	25	,	25	,	25	,	25],
			[	16,	23,	25.64,	26,	25.5,	25.66,	25.75,	25.6,	25.66],
			[	16,	22,	26.36,	26,	26.5,	26.33,	26.25,	26.4,	26.33],
			[	15,	22,	27.03,	27,	27	,	27	,	27	,	27	,	27],
			[	15,	21,	27.78,	28,	28	,	27.66,	27.75,	27.8,	27.83],
			[	14,	21,	28.57,	29,	28.5,	28.66,	28.5,	28.6,	28.5],
			[	14,	20,	29.41,	29,	29.5,	29.33,	29.5,	29.4,	29.33],
			[	14,	19,	30.30,	30,	30.5,	30.33,	30.25,	30.4,	30.33],
			[	13,	19,	31.25,	31,	31.5,	31.33,	31.25,	31.2,	31.33],
			[	13,	18,	32.26,	32,	32.5,	32.33,	32.25,	32.2,	32.33],
			[	13,	17,	33.33,	33,	33.5,	33.33,	33.25,	33.4,	33.33],
			[	13,	16,	34.48,	34,	34.5,	34.33,	34.5,	34.4,	34.5],
			[	13,	15,	35.71,	36,	35.5,	35.66,	35.75,	35.8,	35.66],
			[	13,	14,	37.04,	37,	37	,	37	,	37	,	37	,	37],
			[	13,	13,	38.46,  38,	38.5,	38.33,	38.5,	38.4,	38.5 ]]


def SenderGetUpAndDown(frequency):
	for i in range(len(FreqLookUp)):
		if FreqLookUp[i][2] == frequency:
			return ([FreqLookUp[i][0], FreqLookUp[i][1]])
	print(frequency)
	raise NameError ('Frequency Not Valid')


def getIndex(SS):
	if SS ==   128:
		return(3)
	elif SS == 256:
		return(4)
	elif SS == 384:
		return(5)
	elif SS == 512:
		return(6)
	elif SS == 640:
		return(7)
	elif SS == 768:
		return(8)
	else:
		raise NameError('Block Size Not Implemented')


def mapToClosestFrequencies(frequency_set, sample_size):
	# function which converts a set a set of Send Frequencies to recieve frequencies based on the resolution of the FFT given a certain window size
	index = getIndex(sample_size)
	newSet = []
	badFrequencyFlag = True
	for i in range(len(frequency_set)):
		for j in range(len(FreqLookUp)):
			if FreqLookUp[j][2] == frequency_set[i]:
				newSet = newSet + [FreqLookUp[j][index]]
				badFrequencyFlag = False
		if badFrequencyFlag == True:
			raise NameError('invalid frequency input')
	return(newSet)

