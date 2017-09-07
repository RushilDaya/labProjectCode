# this is a scratch file showing how to use the the serialCommObj version 1
# load the Sketch: FixedFrequencyAndDutyOnSerial to the arduino

from SerialComs import serialCommObj
import time

a = serialCommObj('COM6',9600)


a.setFreqAndDuty(20,0.50)
time.sleep(3)
a.setFreqAndDuty(1,0.5)
