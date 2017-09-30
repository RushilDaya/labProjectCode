import numpy 
import DetectionAlgorithms as DA
import matplotlib.pyplot as plt 

freqs = [20, 20.5, 19.5]
time = numpy.linspace(0,8, 1024)
data = numpy.sin(20*2*numpy.pi*time)

print(DA.psdaGet(data,freqs,128))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
sPlot, = ax.plot(time,abs(numpy.fft.fft(data)))
fig.canvas.draw()
while True:
	True