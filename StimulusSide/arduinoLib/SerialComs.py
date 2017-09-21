import serial 
import time 

# define version one object which does basic communication with arduino

class serialCommObj:
	def __init__(self, port, baud):
		self.Connection = serial.Serial(port,baud)
		time.sleep(2)

	def setFreqAndDuty(self,freq, duty):
		# maximum frequency is 500 Hz
		# duty is a fraction e [0:1]

		if duty > 1:
			duty = 1
		if duty < 0:
			duty = 1

		roundedPeriod = round(1000/freq)
		highTimeInMilliseconds = round(duty*roundedPeriod);
		lowTimeInMilliseconds = roundedPeriod - highTimeInMilliseconds

		UpTimeString = 'u'+str(highTimeInMilliseconds)+'\n'
		DownTimeString = 'd'+str(lowTimeInMilliseconds)+'\n'

		print(bytes(UpTimeString,'ASCII'))
		print(bytes(DownTimeString,'ASCII'))
		self.Connection.write(bytes(UpTimeString,'ASCII'))
		self.Connection.write(bytes(DownTimeString,'ASCII'))
		return True

	def singleDutyPhase(self, freq, phaseIndex):
		qPeriod = round(0.25*(1000/freq))
		comStr = phaseIndex+str(qPeriod)+'\n'
		self.Connection.write(bytes(comStr,'ASCII'))
		return True

