import math
import operator
import numpy
from numpy import pi
from numpy.linalg import cholesky,inv,svd
from scipy.signal import butter, lfilter
#from sklearn.neighbors import KNeighborsRegressor


def cca_psda_get(data,Frequencies,sampleRate):
	psda_probs = psdaGet(data,Frequencies,sampleRate)
	cca_probs = ccaGet(data,Frequencies,sampleRate)
	
	comb = (numpy.add(psda_probs,cca_probs))/2
	
	return comb

def psdaGet(data, Frequencies, sampleRate):
	#very basic form of PSDA
	#will just look for highest peak among those measured
	# ONLY works for one dimensional data
	data = data.transpose() #data.reshape([1,len(data)])
	DATA = abs(numpy.fft.fft(data - numpy.mean(data)))
	#print('=====: ', (DATA.shape))
	Resolution  = float(sampleRate)/len(DATA[0])
	SampleSet = []
	for i in range(len(Frequencies)):
		SampleSet = SampleSet + [int(round(Frequencies[i]/Resolution))]
	softOut = numpy.zeros(len(Frequencies))
	for i in range(len(Frequencies)):
		softOut[i] = DATA[0][SampleSet[i]]

	probs = softOut/sum(softOut)
	
	#print('YAYA: ', probs)
	return(probs)

	
def ccaGet(data,Frequencies,sampleRate):
	#Makes use of the CCA function and returns canonical coefficients for each target frequency
	
	#remove mean
	data = data - numpy.mean(data)
	#filter
	flow = 24
	fhigh = 28
	b,a = bandpass_filt(flow, fhigh, 128)
	DATA = lfilter(b,a,data)
	samples = len(data)
	Nh = 0 #No harmonics
	
	#DATA = data[0][0] + data[:512][1] + data[:,2] + data[:,3]
	#print ('LENGHTT: ', data)
	coeffs = []
	for i in range(0, len(Frequencies)):
		X = ref_signals(Frequencies[i],samples,Nh)
		#print(X)
		coeffs = coeffs + [CCA(X,DATA)]
		
	probs = coeffs/sum(coeffs)
	#print('HELLO: ', probs)
	
	return probs

def CCA(X,Y):
##CCA Implementation via Cholesky Decomposition
#
# Inputs - Two data sets to be analysed - ensure that X dimensionality > Y dimensionality
# Output - Correlation Coefficients - min (xdim,ydim) 
#
# This implementation is based on the description of a CCA function
# provided by IMSL Fortran Numerical Library, with the link below:
# http://docs.roguewave.com/imsl/fortran/7.0/stat/stat.pdf
# An additional document describing pseudocode for the relevant description
# can be found at the following link:
# http://www.itl.nist.gov/div898/software/dataplot/refman2/ch4/cholesky.pdf 
#
# The function is called CANVC and performs CCA based on covariance matrices,
# the function can be found on page 1019. What the function does:
# - Finds the matrix C:
#						C = [(S_xx)^(-1/2)]^T*[S_xy]*[[(S_yy)^(-1/2)]]
# Where:
#		- the power to a half (^1/2) describes the Upper Triangular Cholesky Factorization
#		- the negative (^-1/2) denotes the inverse. 
#		   
#
# To do:  


	#Ensure each dataset has the same number of observations/samples
	if Y.shape[0]!=X.shape[0]:
		raise ValueError,"Incompatible dimensions for X and Y"

	#Get each dataset dimensions
	xdims = X.shape[1]
	ydims = Y.shape[1]

	#Get auto and cross covariance matrices
	Sxx = numpy.dot(X.transpose(),X)
	Syy = numpy.dot(Y.transpose(),Y)
	Sxy = numpy.dot(X.transpose(),Y)

	#Include biasing factor to disable ill conditioned matrices - when finding inverse
	factor = 0.0000000001 #1e-10
	Sxx = Sxx + factor*numpy.eye(xdims,xdims)
	Syy = Syy + factor*numpy.eye(ydims,ydims)

	#Get upper triangular matrix via Cholesky factorization and transposition
	Sxx_UT = (cholesky(Sxx))
	Syy_UT = (cholesky(Syy))

	#Get inverse matrices
	Sxx_inv = (inv(Sxx_UT)).transpose()
	Syy_inv = (inv(Syy_UT)) #.transpose()

	#Get C
	C_temp = numpy.dot(Sxx_inv,Sxy)
	C = numpy.dot(C_temp,Syy_inv)

	#Single Value decomposition to get CCA correlations
	L,coeffs,R = svd(C) 

	return max(coeffs)
		
def ref_signals(freq, samples, harmonics_no):
##Returns array of reference stimulus signals for CCA algorithm

	sig = numpy.zeros((samples,(2+2*harmonics_no)))
	c = 0 
	for i in range (0, harmonics_no+1):
		t = numpy.linspace(0,2*pi*(i+1)*freq*4,samples); #time vector with n observations
		sig[:,c] = numpy.sin(t) # + np.cos(t) #(2*pi*t*(i+1)*f)
		sig[:,c+1] = numpy.cos(t) #(2*pi*t*(i+1)*f)
		c = c + 2
	return sig
	
	
def bandpass_filt(lowF, highF, fs, order=5):
	#Returns coefficients of bandpass butterworth filter
    nyq = 0.5*fs
    low = lowF/nyq
    high = highF/nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a