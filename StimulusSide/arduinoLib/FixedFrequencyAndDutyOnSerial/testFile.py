# this is a scratch file showing how to use the the serialCommObj version 1
# load the Sketch: FixedFrequencyAndDutyOnSerial to the arduino

from SerialComs import serialCommObj
import time

a = serialCommObj('COM6',9600)

while True:
	a.setFreqAndDuty(30,0.5)
	time.sleep(12)
	# a.setFreqAndDuty(28,0.5)
	# time.sleep(12)
	# a.setFreqAndDuty(30,0.5)
	# time.sleep(12)
	# a.setFreqAndDuty(32,0.5)
	# time.sleep(12)
