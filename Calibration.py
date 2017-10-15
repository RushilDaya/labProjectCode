# # This file must be run on the reciever Side PC.

# # objectives of the Calibration routine:
# # Determine Best Transmission Frequencies
# # Determine Time required for transmission
# # Use time and frequency to determine the ITR parameters.
# # based on the Detection method it may require that Calibration
# # records data as well

# import math
# import time
# import numpy
# import Source.Channel as Channel
# import Source.RecvSideLib as RecvLib 
# import Source.InputLib as SendLib
# import Source.DetectionAlgorithms as Detections


# # ========= Define Parameters =============================================
# # ========= Set Up Objects ================================================
# # ========= determine the Connection ======================================
# # ========= Do a frequency Sweep ==========================================
# # ========= Vary Times ====================================================
# # ========= Calculate maximum ITR =========================================

 
import time
import numpy
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import Source.Channel as Channel
import Source.RecvSideLib as RecvLib 
import Source.InputLib as SendLib
import Source.DetectionAlgorithms as Detections
import Source.Frequency_Determination as FD



## set up the display window =====
plt.ion()
fig = plt.figure()
axisO1 = fig.add_subplot(221)
axisO1.set_title('O1 electrode')
axisO2 = fig.add_subplot(222)
axisO2.set_title('O2 electrode')
axisP7 = fig.add_subplot(224)
axisP7.set_title('P7 electrode')
axisP8 = fig.add_subplot(223)
axisP8.set_title('P8 electrode')



FrequencySet = [23.26, 25, 28.57, 30.30, 33.33, 35.71, 38.46]
Electrodes = ['O1', 'O2','P7', 'P8']
FFTLength = 1024
FFTUpdateTime = 1 # in seconds
numUpdates  = int(FFTLength/(FFTUpdateTime*128))*2

SenderChannel =  SendLib.Channel('FixedFrequencyAndDuty',None,None)
ReceiveChannel = Channel.Channel('Emokit',Electrodes, False, False)

Data = numpy.zeros([FFTLength, len(Electrodes)])


def dataUpdate(OldData, newData):
	for column in range(len(OldData[0])):
		OldData[:,column] = numpy.roll(OldData[:,column], -len(newData))
		OldData[len(OldData)-len(newData):len(OldData),column] = newData[:,column]
	return (OldData)



def getFFTs(Data):
	Hann = numpy.hanning(len(Data))
	ffts = numpy.zeros([len(Data), len(Data[0])])
	halfLength = len(Data)/2 + 1
	for column in range(len(Data[0])):
		ffts[:,column]=numpy.fft.fft(Hann*(numpy.transpose(Data[:,column]-numpy.mean(Data[:,column]))))
		ffts[:,column]=numpy.abs(ffts[:,column])
	return(ffts[0:halfLength,:])


def getIndexes(frequencies, sampleSize):
	returnSet = []
	resolution = float(128)/(sampleSize)
	for freq in frequencies:
		index = int(round(freq/resolution))
		returnSet = returnSet + [index]
		print(index*resolution)
	return(returnSet)


freqIndices = getIndexes(FrequencySet, FFTLength)
maxPoints = numpy.zeros([len(FrequencySet),len(Electrodes)])

time.sleep(2)
print('Record Begin')

freqIndex = 0
for Frequency in FrequencySet:
	SenderChannel.setSingleFreq(Frequency)
	X_axis = numpy.linspace(0, 64, len(Data)/2+1)
	ReceiveChannel.flushBuffer()
	for update in range(numUpdates):
		newData = ReceiveChannel.getDataBlock(FFTUpdateTime)
		Data = dataUpdate(Data,newData)
		plotData = getFFTs(Data)

		for channel in range(len(Electrodes)):
			if plotData[freqIndices[freqIndex]-1,channel]>maxPoints[freqIndex,channel]:
				maxPoints[freqIndex,channel] = max(plotData[freqIndices[freqIndex-1],channel],plotData[freqIndices[freqIndex],channel],plotData[freqIndices[freqIndex+1],channel])

		axisO1.cla()
		axisO2.cla()
		axisP7.cla()
		axisP8.cla()
		sPlotO1, = axisO1.plot(X_axis, plotData[:,0])
		sPlotO1, = axisO1.plot(FrequencySet,maxPoints[:,0],'o')
		axisO1.set_title('O1 electrode')
		axisO1.set_autoscaley_on(False)
		axisO1.set_ylim([0,1500])

		sPlotO2, = axisO2.plot(X_axis, plotData[:,1],'r')
		sPlotO2, = axisO2.plot(FrequencySet,maxPoints[:,1],'o')		
		axisO2.set_title('O2 electrode')
		axisO2.set_autoscaley_on(False)
		axisO2.set_ylim([0,1500])

		sPlotP7, = axisP7.plot(X_axis, plotData[:,2],'g')
		sPlotP7, = axisP7.plot(FrequencySet,maxPoints[:,2],'o')
		axisP7.set_title('P7 electrode')
		axisP7.set_autoscaley_on(False)
		axisP7.set_ylim([0,1500])

		sPlotP8, = axisP8.plot(X_axis, plotData[:,3],'y')
		sPlotP8, = axisP8.plot(FrequencySet,maxPoints[:,3],'o')
		axisP8.set_title('P8 electrode')
		axisP8.set_autoscaley_on(False)
		axisP8.set_ylim([0,1500])

		fig.canvas.draw()
		plt.pause(0.001)
	freqIndex +=1













