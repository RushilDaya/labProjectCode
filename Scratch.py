import numpy
import math
import Source.Channel as Channel
import Source.DetectionAlgorithms as Detections
import Source.RecvSideLib as RecvLib 



UpdateTime = 1 # one Second
#PSDADetector4s = RecvLib.DetectionObject('PSDA',[28.5. 30.25],None, ['O1'], 4,'HARD')
Chan = Channel.Channel('Emokit',['O1'],False, False)
Data = numpy.zeros([512, 1])


def dataUpdate(OldData, newData):
	for column in range(len(OldData[0])):
		OldData[:,column] = numpy.roll(OldData[:,column], -len(newData))
		OldData[len(OldData)-len(newData):len(OldData),column] = newData[:,column]
	return (OldData)

Chan.flushBuffer()

while True:
	newData = Chan.getDataBlock(UpdateTime)
	Data = dataUpdate(Data, newData)
	Probs = Detections.psdaGetForHeader(Data,[28.5, 30.25],128)
	print(Probs)