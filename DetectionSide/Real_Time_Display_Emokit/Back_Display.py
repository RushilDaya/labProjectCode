## Script to display the fft's of the the back 6 electrodes
## this script is purely for  display puposess

import time
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

from emokit.python.emokit.emotiv import Emotiv 
from emokit.python.emokit.packet import EmotivNewPacket

###### User defined Variables #########

FFT_Size = 1024 #size of window
Sample_Rate = 128
Update_Period = 1 # time (secs) between updates; combined with FFT size and sample rate determines overlap
window_Funct = np.hanning(FFT_Size)
FFT_Axis_Height = 1500 

###### Computed Variables     #########
RollInLength = Update_Period*Sample_Rate
P7Short = np.zeros(RollInLength)
O1Short = np.zeros(RollInLength)
O2Short = np.zeros(RollInLength)
P8Short = np.zeros(RollInLength)

P7Full = np.zeros(FFT_Size)
O1Full = np.zeros(FFT_Size)
O2Full = np.zeros(FFT_Size)
P8Full = np.zeros(FFT_Size)

Half_FFT_Length = FFT_Size/2 +1
X_axis = np.linspace(0, Sample_Rate/2, Half_FFT_Length)
P7FFT = np.zeros(FFT_Size)
O1FFT = np.zeros(FFT_Size)
O2FFT = np.zeros(FFT_Size)
P8FFT = np.zeros(FFT_Size)

P7Half_FFT = np.zeros(Half_FFT_Length)
P7Half_FFT[0] = FFT_Axis_Height
O1Half_FFT = np.zeros(Half_FFT_Length)
O1Half_FFT[0] = FFT_Axis_Height
O2Half_FFT = np.zeros(Half_FFT_Length)
O2Half_FFT[0] = FFT_Axis_Height
P8Half_FFT = np.zeros(Half_FFT_Length)
P8Half_FFT[0] = FFT_Axis_Height


###### define plot objectsS

plt.ion()
fig = plt.figure()
axP7 = fig.add_subplot(221)
axO1 = fig.add_subplot(222)
axO2 = fig.add_subplot(224)
axP8 = fig.add_subplot(223)

sPlotP7, = axP7.plot(X_axis,P7Half_FFT)
sPlotO1, = axO1.plot(X_axis,O1Half_FFT ,'r')
sPlotO2, = axO2.plot(X_axis,O2Half_FFT,'r')
sPlotP8, = axP8.plot(X_axis,P8Half_FFT)


####### enter plot loop #######

if __name__ == "__main__":
	with Emotiv(display_output=True, verbose=False) as emotiv:

		while True:
			counter = 0
			while counter < RollInLength:
				Packet = emotiv.dequeue()
				if Packet is not None:
					P7Short[counter]=Packet.sensors['P7']['value']
					O1Short[counter]=Packet.sensors['O1']['value']
					O2Short[counter]=Packet.sensors['O2']['value']
					P8Short[counter]=Packet.sensors['P8']['value']
					counter+=1
			P7Full = np.roll(P7Full,-RollInLength)
			O1Full = np.roll(O1Full,-RollInLength)
			O2Full = np.roll(O2Full,-RollInLength)
			P8Full = np.roll(P8Full,-RollInLength)

			P7Full[FFT_Size-RollInLength:FFT_Size] = P7Short
			O1Full[FFT_Size-RollInLength:FFT_Size] = O1Short
			O2Full[FFT_Size-RollInLength:FFT_Size] = O2Short
			P8Full[FFT_Size-RollInLength:FFT_Size] = P8Short

			P7FFT = np.fft.fft(window_Funct*(P7Full-np.mean(P7Full)))
			O1FFT = np.fft.fft(window_Funct*(O1Full-np.mean(O1Full)))
			O2FFT = np.fft.fft(window_Funct*(O2Full-np.mean(O2Full)))
			P8FFT = np.fft.fft(window_Funct*(P8Full-np.mean(P8Full)))

			P7Half_FFT = np.abs(P7FFT[0:Half_FFT_Length])
			O1Half_FFT = np.abs(O1FFT[0:Half_FFT_Length])
			O2Half_FFT = np.abs(O2FFT[0:Half_FFT_Length])
			P8Half_FFT = np.abs(P8FFT[0:Half_FFT_Length])

			sPlotP7.set_ydata(P7Half_FFT)
			sPlotO1.set_ydata(O1Half_FFT)
			sPlotO2.set_ydata(O2Half_FFT)
			sPlotP8.set_ydata(P8Half_FFT)
			fig.canvas.draw()