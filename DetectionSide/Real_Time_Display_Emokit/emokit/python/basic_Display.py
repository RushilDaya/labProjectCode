import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from emokit.emotiv import Emotiv
from emokit.packet import EmotivNewPacket


if __name__ == "__main__":
	with Emotiv(display_output=True, verbose=False) as emotiv:

		FFT_Length = 1024
		Samp_Rate = 128
		Update_period = 1 
		ShortWinLength = Update_period*Samp_Rate
		shortWin = np.zeros(ShortWinLength)
		x = np.linspace(0,Samp_Rate/2,FFT_Length/2+1)
		LongData = np.zeros(FFT_Length)

		plt.ion()
 		fig = plt.figure()
 		axO1fft = fig.add_subplot(224)

		fftDat = np.zeros(FFT_Length/2+1)
		fftDat[0]= 4000
		fftPlot, = axO1fft.plot(x,fftDat,'r')
		fullfft = np.zeros(FFT_Length)
		count_30hertz = 0;

		while True:
			counter = 0
			while counter < ShortWinLength:
				Packet = emotiv.dequeue()
				if Packet is not None:
					shortWin[counter]=Packet.sensors['O1']['value']
					counter +=1
			LongData = np.roll(LongData,-ShortWinLength)
			LongData[FFT_Length- ShortWinLength:FFT_Length] = shortWin
			fullfft = np.fft.fft(LongData-np.mean(LongData))
			fftDat = fullfft[0:FFT_Length/2+1]
			fftDat = np.abs(fftDat)

			# max_peak_ind = np.argmax(fftDat[165:512]) #from 13 hertz onwards find the max peak
			# if ((max_peak_ind <= 245) and (max_peak_ind >= 236)):
			# 	count_30hertz = count_30hertz+1
			# 	print('SSVEP at 30Hz detected')
			

			fftPlot.set_ydata(fftDat)
			fig.canvas.draw()











# if __name__ == "__main__":
#     with Emotiv(display_output=True, verbose=False) as emotiv:
# 		print('start')
# 		vecSize = 20
# 		longDataSize = 300*vecSize
# 		plt.ion()
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		x = np.linspace(0, longDataSize-1, longDataSize)
# 		data = np.zeros(longDataSize)
# 		data[0]= 500
# 		data[1]=-500
# 		line1, = ax.plot(x,data,'r')

# 		while True:
# 			data_ = np.zeros(vecSize)
# 			counter = 0
# 			while counter <vecSize:
# 				PACK = emotiv.dequeue()
# 				if PACK is not None:
# 					data_[counter]=PACK.sensors['O1']['value'] - 4836
# 					counter +=1
# 			data = np.roll(data,-vecSize)
# 			data[longDataSize-vecSize : longDataSize]=data_
# 			line1.set_ydata(data)
# 			fig.canvas.draw()
