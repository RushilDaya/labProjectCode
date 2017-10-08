import numpy

def psdaGet(data, Frequencies, sampleRate):
	#very basic form of PSDA
	#will just look for highest peak among those measured
	# ONLY works for one dimensional data
	data = data.reshape([1,len(data)])
	DATA = abs(numpy.fft.fft(data - numpy.mean(data)))
	print('=====')
	Resolution  = float(sampleRate)/len(DATA[0])
	SampleSet = []
	for i in range(len(Frequencies)):
		SampleSet = SampleSet + [int(round(Frequencies[i]/Resolution))]
	softOut = numpy.zeros(len(Frequencies))
	for i in range(len(Frequencies)):
		softOut[i] = DATA[0][SampleSet[i]]

	probs = softOut/sum(softOut)
	return(probs)
