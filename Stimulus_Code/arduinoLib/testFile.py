# this is a scratch file showing how to use the the serialCommObj version 1
# load the Sketch: FixedFrequencyAndDutyOnSerial to the arduino

from SerialComs import serialCommObj
import time

a = serialCommObj('COM6',9600)



while True:
	frequency_selected = input('Select A Frequency: ')
	frequency_selected = float(frequency_selected)
	a.setFreqAndDuty(frequency_selected,0.5)
	print('current frequency'+str(frequency_selected))
	print('*********')
