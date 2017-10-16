import time
import numpy
import math
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import Source.Channel as Channel
import Source.RecvSideLib as RecvLib 
import Source.InputLib as SendLib
import Source.DetectionAlgorithms as Detections
import Source.Frequency_Determination as FD





# ===========Frequency Selection Routine==============================================
#=====Variables====

FrequencySet = [23.26, 23.81, 24.39, 25]#, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,34.48, 35.71, 37.04, 38.46]
SymbolVector = [0,1,2,3]#,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
ElectrodesForCCA = ['O1','O2','P7','P8']
NumRuns = 2 # how many detection loops should be performed
# =================

#########
#===Collect Data ======

TransmissionFrequencies4s = FD.mapToClosestFrequencies(FrequencySet, 512)
Sender =  SendLib.Channel('FixedFrequencyAndDuty',None,None)
Receiver =   Channel.Channel('Emokit',ElectrodesForCCA, False, False)
CCADetector4s = RecvLib.DetectionObject('CCA',TransmissionFrequencies4s,None, ElectrodesForCCA, 4,'HARD')
PSDADetector4s = RecvLib.DetectionObject('PSDA',TransmissionFrequencies4s,None, ['O1'], 4,'HARD')
CombinedDetector4s = RecvLib.DetectionObject('Combined',TransmissionFrequencies4s,None, ElectrodesForCCA, 4,'HARD')
ResultsCCA4s = numpy.zeros([len(SymbolVector),NumRuns])
ResultsPSDA4s = numpy.zeros([len(SymbolVector),NumRuns])
ResultsCombined4s = numpy.zeros([len(SymbolVector),NumRuns])
time.sleep(2)
Receiver.flushBuffer()

for i in range(NumRuns):
	Data4Seconds = numpy.zeros([len(SymbolVector)*512,len(ElectrodesForCCA)])
	Receiver.flushBuffer()
	counter = 0
	for Symbol in SymbolVector:
		Sender.setSingleFreq(FrequencySet[Symbol])
		Data4Seconds[counter*512:counter*512+512,:] = Receiver.getDataBlock(4,False)
		counter +=1
	detectedCCA = CCADetector4s.getSymbols(Data4Seconds)
	print(detectedCCA)
	detectedPSDA = PSDADetector4s.getSymbols(Data4Seconds)
	print(detectedPSDA)
	detectedCombined = CombinedDetector4s.getSymbols(Data4Seconds)
	print(detectedCombined)
	ResultsCCA4s[:,i]= detectedCCA
	ResultsPSDA4s[:,i]=detectedPSDA
	ResultsCombined4s[:,i]=detectedCombined
	Sender.SerialObj.setFreqAndDuty(100, 0)
	time.sleep(1)


TransmissionFrequencies3s = FD.mapToClosestFrequencies(FrequencySet, 384)
CCADetector3s = RecvLib.DetectionObject('CCA',TransmissionFrequencies3s,None, ElectrodesForCCA, 3,'HARD')
PSDADetector3s = RecvLib.DetectionObject('PSDA',TransmissionFrequencies3s,None, ['O1'], 3,'HARD')
CombinedDetector3s = RecvLib.DetectionObject('Combined',TransmissionFrequencies3s,None, ElectrodesForCCA, 3,'HARD')
ResultsCCA3s = numpy.zeros([len(SymbolVector),NumRuns])
ResultsPSDA3s = numpy.zeros([len(SymbolVector),NumRuns])
ResultsCombined3s = numpy.zeros([len(SymbolVector),NumRuns])
time.sleep(2)
Receiver.flushBuffer()

for i in range(NumRuns):
	Data3Seconds = numpy.zeros([len(SymbolVector)*384,len(ElectrodesForCCA)])
	Receiver.flushBuffer()
	counter = 0
	for Symbol in SymbolVector:
		Sender.setSingleFreq(FrequencySet[Symbol])
		Data3Seconds[counter*384:counter*384+384,:] = Receiver.getDataBlock(3,False)
		counter +=1
	detectedCCA = CCADetector3s.getSymbols(Data3Seconds)
	print(detectedCCA)
	detectedPSDA = PSDADetector3s.getSymbols(Data3Seconds)
	print(detectedPSDA)
	detectedCombined = CombinedDetector3s.getSymbols(Data3Seconds)
	print(detectedCombined)
	ResultsCCA3s[:,i]= detectedCCA
	ResultsPSDA3s[:,i]=detectedPSDA
	ResultsCombined3s[:,i]=detectedCombined
	Sender.SerialObj.setFreqAndDuty(100, 0)
	time.sleep(1)

#=== End Data Collect ====
########################

DetectionAccuracy3s = numpy.zeros([len(SymbolVector),4])
DetectionAccuracy4s = numpy.zeros([len(SymbolVector),4])

DetectionAccuracy3s[:,0]= numpy.linspace(0,len(SymbolVector)-1,len(SymbolVector))
DetectionAccuracy4s[:,0]= numpy.linspace(0,len(SymbolVector)-1,len(SymbolVector))

for Symbol in range(len(SymbolVector)):
	for j in range(NumRuns):
		if ResultsCCA3s[Symbol,j] == Symbol:
			DetectionAccuracy3s[Symbol,1] = DetectionAccuracy3s[Symbol,1]+float(1)/NumRuns
		if ResultsPSDA3s[Symbol,j] == Symbol:
			DetectionAccuracy3s[Symbol,2] = DetectionAccuracy3s[Symbol,2]+float(1)/NumRuns
		if ResultsCombined3s[Symbol,j] == Symbol:
			DetectionAccuracy3s[Symbol,3] = DetectionAccuracy3s[Symbol,3]+float(1)/NumRuns
		if ResultsCCA4s[Symbol,j]  == Symbol:
			DetectionAccuracy4s[Symbol,1] = DetectionAccuracy4s[Symbol,1]+float(1)/NumRuns
		if ResultsPSDA4s[Symbol,j] == Symbol:
			DetectionAccuracy4s[Symbol,2] = DetectionAccuracy4s[Symbol,2]+float(1)/NumRuns
		if ResultsCombined4s[Symbol,j] == Symbol:
			DetectionAccuracy4s[Symbol,3] = DetectionAccuracy4s[Symbol,3]+float(1)/NumRuns

print(DetectionAccuracy4s)
print(DetectionAccuracy3s)

# Calculate the Average detection accuracies for the different configurations
LargestValidConstellationSize = int(math.floor(math.log(len(SymbolVector),2)))
results = numpy.zeros([1,LargestValidConstellationSize*2*3]) # accounts for all the results
# format of the results
# [3sCCA_2Sym,3sPSDA_2Sym,3sCOM_2Sym,4sCCA_2Sym,4sPSDA_2Sym,4sCOM_2Sym,3sCCA_4Sym,3sPSDA_4Sym,3sCOM_4Sym,4sCCA_4Sym,4sPSDA_4Sym,4sCOM_4Sym,...]
for i in range(LargestValidConstellationSize):
	CSize = i + 1 
	NumPoints = int(math.pow(2,CSize)) # the number of points for a particular constellation
	length = len(SymbolVector)
	results[i*6+0] = numpy.sort(DetectionAccuracy3s[:,1])[length-NumPoints:length].mean()
	results[i*6+1] = numpy.sort(DetectionAccuracy3s[:,2])[length-NumPoints:length].mean()
	results[i*6+2] = numpy.sort(DetectionAccuracy3s[:,3])[length-NumPoints:length].mean()
	results[i*6+3] = numpy.sort(DetectionAccuracy4s[:,1])[length-NumPoints:length].mean()
	results[i*6+4] = numpy.sort(DetectionAccuracy4s[:,2])[length-NumPoints:length].mean()
	results[i*6+5] = numpy.sort(DetectionAccuracy4s[:,3])[length-NumPoints:length].mean()

print(results)











# for Symbol in SymbolVector:
# 	DetectionRate = numpy.zeros([1,3])
# 	for i in numRuns:













# ## set up the display window =====
# plt.ion()
# fig = plt.figure()
# axisO1 = fig.add_subplot(221)
# axisO1.set_title('O1 electrode')
# axisO2 = fig.add_subplot(222)
# axisO2.set_title('O2 electrode')
# axisP7 = fig.add_subplot(224)
# axisP7.set_title('P7 electrode')
# axisP8 = fig.add_subplot(223)
# axisP8.set_title('P8 electrode')



# FrequencySet = [23.26, 25, 28.57, 30.30, 33.33, 35.71, 38.46]
# Electrodes = ['O1', 'O2','P7', 'P8']
# FFTLength = 1024
# FFTUpdateTime = 1 # in seconds
# numUpdates  = int(FFTLength/(FFTUpdateTime*128))*2

# SenderChannel =  SendLib.Channel('FixedFrequencyAndDuty',None,None)
# ReceiveChannel = Channel.Channel('Emokit',Electrodes, False, False)

# Data = numpy.zeros([FFTLength, len(Electrodes)])


# def dataUpdate(OldData, newData):
# 	for column in range(len(OldData[0])):
# 		OldData[:,column] = numpy.roll(OldData[:,column], -len(newData))
# 		OldData[len(OldData)-len(newData):len(OldData),column] = newData[:,column]
# 	return (OldData)



# def getFFTs(Data):
# 	Hann = numpy.hanning(len(Data))
# 	ffts = numpy.zeros([len(Data), len(Data[0])])
# 	halfLength = len(Data)/2 + 1
# 	for column in range(len(Data[0])):
# 		ffts[:,column]=numpy.fft.fft(Hann*(numpy.transpose(Data[:,column]-numpy.mean(Data[:,column]))))
# 		ffts[:,column]=numpy.abs(ffts[:,column])
# 	return(ffts[0:halfLength,:])


# def getIndexes(frequencies, sampleSize):
# 	returnSet = []
# 	resolution = float(128)/(sampleSize)
# 	for freq in frequencies:
# 		index = int(round(freq/resolution))
# 		returnSet = returnSet + [index]
# 		print(index*resolution)
# 	return(returnSet)


# freqIndices = getIndexes(FrequencySet, FFTLength)
# maxPoints = numpy.zeros([len(FrequencySet),len(Electrodes)])

# time.sleep(2)
# print('Record Begin')

# freqIndex = 0
# for Frequency in FrequencySet:
# 	SenderChannel.setSingleFreq(Frequency)
# 	X_axis = numpy.linspace(0, 64, len(Data)/2+1)
# 	ReceiveChannel.flushBuffer()
# 	for update in range(numUpdates):
# 		newData = ReceiveChannel.getDataBlock(FFTUpdateTime)
# 		Data = dataUpdate(Data,newData)
# 		plotData = getFFTs(Data)

# 		for channel in range(len(Electrodes)):
# 			if plotData[freqIndices[freqIndex]-1,channel]>maxPoints[freqIndex,channel]:
# 				maxPoints[freqIndex,channel] = max(plotData[freqIndices[freqIndex-1],channel],plotData[freqIndices[freqIndex],channel],plotData[freqIndices[freqIndex+1],channel])

# 		axisO1.cla()
# 		axisO2.cla()
# 		axisP7.cla()
# 		axisP8.cla()
# 		sPlotO1, = axisO1.plot(X_axis, plotData[:,0])
# 		sPlotO1, = axisO1.plot(FrequencySet,maxPoints[:,0],'o')
# 		axisO1.set_title('O1 electrode')
# 		axisO1.set_autoscaley_on(False)
# 		axisO1.set_ylim([0,1500])

# 		sPlotO2, = axisO2.plot(X_axis, plotData[:,1],'r')
# 		sPlotO2, = axisO2.plot(FrequencySet,maxPoints[:,1],'o')		
# 		axisO2.set_title('O2 electrode')
# 		axisO2.set_autoscaley_on(False)
# 		axisO2.set_ylim([0,1500])

# 		sPlotP7, = axisP7.plot(X_axis, plotData[:,2],'g')
# 		sPlotP7, = axisP7.plot(FrequencySet,maxPoints[:,2],'o')
# 		axisP7.set_title('P7 electrode')
# 		axisP7.set_autoscaley_on(False)
# 		axisP7.set_ylim([0,1500])

# 		sPlotP8, = axisP8.plot(X_axis, plotData[:,3],'y')
# 		sPlotP8, = axisP8.plot(FrequencySet,maxPoints[:,3],'o')
# 		axisP8.set_title('P8 electrode')
# 		axisP8.set_autoscaley_on(False)
# 		axisP8.set_ylim([0,1500])

# 		fig.canvas.draw()
# 		plt.pause(0.001)
# 	freqIndex +=1



# send data through in the form of symbols determine the symbols which show the lowest error,
# The visual process is fine but it does not actually show the truth of the situation.
# we do not know whats going on in terms of the error rates for a particular symbol 
# we need to do that sweep first

# We have 8 symbols to work with
# We have 3 and 4 seconds to work with
# Our aim to to determine the symbol, time, error combination to maximize the FEC and the next step is to determine the 
# FEC rate which will allow us to correct the errors for the chosen scheme.

# Send the 8 Symbols at 4 second
# Send the 8 Symbols at 3 second
# Using these results we must determine the 

# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
#  34.48, 35.71, 37.04, 38.46 ]
# Frequencies = [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,34.48, 35.71, 37.04, 38.46]
# TransmissionFrequencies4s = FD.mapToClosestFrequencies(Frequencies, 512)
# TransmissionFrequencies3s = FD.mapToClosestFrequencies(Frequencies, 384)
# SymbolVector = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]#,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]
# ElectrodesForCCA = ['O1','O2','P7','P8']
# Sender =  SendLib.Channel('FixedFrequencyAndDuty',None,None)
# Receiver =   Channel.Channel('Emokit',ElectrodesForCCA, False, False)
# CCADetector4s = RecvLib.DetectionObject('CCA',TransmissionFrequencies4s,None, ElectrodesForCCA, 4,'HARD')
# PSDADetector4s = RecvLib.DetectionObject('PSDA',TransmissionFrequencies4s,None, ['O1'], 4,'HARD')
# CombinedDetector4s = RecvLib.DetectionObject('Combined',TransmissionFrequencies4s,None, ElectrodesForCCA, 4,'HARD')


# time.sleep(2)
# Receiver.flushBuffer()
# Data4Seconds = numpy.zeros([len(SymbolVector)*512,len(ElectrodesForCCA)])

# counter = 0
# for Symbol in SymbolVector:
# 	Sender.setSingleFreq(Frequencies[Symbol])
# 	Data4Seconds[counter*512:counter*512+512,:] = Receiver.getDataBlock(4,False)
# 	counter +=1

# detectedCCA = CCADetector4s.getSymbols(Data4Seconds)
# detectedPSDA = PSDADetector4s.getSymbols(Data4Seconds)
# detectedCombined = CombinedDetector4s.getSymbols(Data4Seconds)
# print('CCA: ', detectedCCA)
# print('PSDA: ',detectedPSDA)

# ccaErrors = 0
# psdaErrors = 0
# CombinedErrors = 0
# for i in range(len(SymbolVector)):
# 	if SymbolVector[i] != detectedCCA[i]:
# 		ccaErrors+=1
# 	if SymbolVector[i] !=detectedPSDA[i]:
# 		psdaErrors+=1
# 	if SymbolVector[i] !=detectedCombined[i]:
# 		CombinedErrors+=1
# print('cca error rate ' + str(float(ccaErrors)/len(SymbolVector)))
# print('psda error rate ' + str(float(psdaErrors)/len(SymbolVector)))
# print('Combined error rate ' + str(float(CombinedErrors)/len(SymbolVector)))


# Best of 4: for each frequency have a detection rate.
# this is a calibration routine which works in a  particular environment
# if the environment is changed the ITR which can be achieved will also change




