# this is a scratch file showing how to use the the serialCommObj version 1
# load the Sketch: FixedFrequencyAndDutyOnSerial to the arduino

from SerialComs import serialCommObj
import time

a = serialCommObj('COM6',9600)


a.singleDutyPhase(30,'c')

# a.singleDutyPhase(14,'a')
# time.sleep(10)
# a.singleDutyPhase(14,'b')
# time.sleep(10)
# a.singleDutyPhase(14,'c')
# time.sleep(10)
# a.singleDutyPhase(14,'d')
# time.sleep(10)
