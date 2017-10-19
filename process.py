
import Source.InputLib  as IL
import time
import math
import Source.Channel as CH
import Source.RecvSideLib as RL 

import Tkinter as tk 
import tkMessageBox
import ttk
Font_type = ('Times New Roman', 12)

class RecvGUI(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.container = tk.Frame(self, width=500, height=500)
		self.container.pack(expand=True) #side="top", fill="both"
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {} #initialise array for app pages - start page, home page, send page
		
		frame = recvPage(self.container, self, 'no') #, self.connect) #, self.tcp_obj, self.pop3_obj)
		self.frames[recvPage] = frame
		frame.grid(row=0, column=0) #pack()
		
		self.renderFrame(recvPage, 'no')
			
		
	def renderFrame(self,cont,new_instance): #, rend_no):
		if new_instance == 'yes':  #need to know if a new instance of the class is required
			frame = cont(self.container, self, new_instance)
			self.frames[cont] = frame
			frame.grid(row=0, column=0)
		else:
			frame = self.frames[cont]
	
		frame.tkraise() #check this command -> makes frame go to front

#inheriting from Frame class of Tkinter	
class recvPage(tk.Frame):
	#class attribute to count number of times this page is returned to
	counter = 0
	
	def __init__(self, main_class, controller, new_instance): 
		#tk.Frame.__init__(self, main_class) 
		#tk.Frame(width=800, height=800)
		#All the widgets required for the receive page
		self.create_objects()
		tk.Frame.__init__(self, main_class) 
		tk.Frame(width=800, height=800)
		self.page_label = ttk.Label(self, text='BrainChannel - Receiver Side', font=('Times New Roman', 14))
		self.page_label.grid(row=0, column=0)
		self.recv_button = tk.Button(self, text="Receive", command=lambda:self.setup_receive(main_class))
		self.recv_button.grid(row=5, column=0)

		self.gaze_detect = False
		self.threshold_detect = False
		
		recvPage.counter += 1
		
	def setup_receive(self, main_class):
		#tk.Frame.__init__(self, main_class) 
		#tk.Frame(width=800, height=800)
		#pack(pady=30, padx=30)  #grid(row=0, column=0) #pack(pady=10, padx=10)
		self.symbols_label = tk.Label(self, text='Received Symbols: ', font=Font_type)
		#self.symbols_label.pack(pady=30, padx=20) #grid(row=2, column=0) #pack(pady=30, padx=20) #grid(row=1, column=0)
		self.recv_symbols = tk.Text(self, width=35, height=1)
		self.dec_msg = tk.Text(self, width=35, height=1)
		#self.recv_symbols.insert(0.0,'Hallllooo mf')
		#self.recv_symbols.pack(pady=10, padx=20) #grid(row=2, column=2) #pack(pady=10, padx=20) #grid(row=1, column=3)
		self.dec_label = ttk.Label(self, text='Decoded Bits: ', font=Font_type)
		#self.dec_label.pack(pady=20, padx=20) #grid(row=3, column=0) #pack(pady=20, padx=20) #grid(row=2, column=0)
		#   #pack(pady=10, padx=20) #grid(row=3, column=2) #
		self.restart_button = ttk.Button(self, text="Receive Again", command=lambda:self.restart(main_class))
	
		self.recv_button.grid_remove()
		self.symbols_label.grid(row=2, column=0)
		self.recv_symbols.insert(0.0,'Hallllooo mf')
		self.recv_symbols.grid(row=2, column=1)
		self.dec_label.grid(row=4, column=0)
		self.dec_msg.grid(row=4, column=1)
		
		self.run_receiver()
			
	def restart(self, main_class):
		#self.page_label.pack_forget() #
		self.symbols_label.grid_remove() #3pack_forget()
		self.recv_symbols.grid_remove()
		self.dec_label.grid_remove()
		self.dec_msg.grid_remove()
		self.restart_button.grid_remove()
		
		self.setup_receive(main_class)
		

	def create_objects(self):
		self.CharSet = 'lowerCaseLiterals'
		self.CharactersPerMessage = 7
		self.SourceEncodeMethod = 'basic'
		self.errorCorrection = 'HardHamming'
		self.FEC_blockSize = 15
		self.FEC_msgSize = 11
###########################
		self.ValidDictionary = IL.loadCharacterSet(self.CharSet)
		self.InputValidationObject = IL.InputValidation(self.ValidDictionary,self.CharactersPerMessage)
		self.SrcEncoder  = IL.SrcEncoder(self.ValidDictionary , self.SourceEncodeMethod)
		self.FEC = IL.ChannelEncoder(self.errorCorrection, self.FEC_blockSize , self.FEC_msgSize)
################################
		self.CharSet = RL.loadCharacterSet(self.CharSet)
		self.CD = RL.ChannelDecoder(self.errorCorrection,'HARD', self.FEC_blockSize, self.FEC_msgSize)
		self.SD = RL.sourceDecoder(self.CharSet, self.SourceEncodeMethod)
		
		
	def run_receiver(self):
		
		#while 1:
		sendString = self.InputValidationObject.getInput()
		SendBits = self.SrcEncoder.EncodeData(sendString)
		#print 'Sendbits: ', SendBits
		EncBits = self.FEC.EncodeData(SendBits)
		#print 'EncBits:', (EncBits)
		IntBits = self.FEC.interleave(EncBits)
		#print 'IntBITS: ', (IntBits)
	
		NoisyBits = ''
		for i in range(0, len(IntBits)):
			if i == 2:
				NoisyBits += '1'
			else:
				NoisyBits += IntBits[i]
	
		print 'NoisyBits: ', NoisyBits
		Symbols  = IL.SymbolMapping(NoisyBits, 4)
		print 'Symbols: ', (Symbols)
	
		Encoded = RL.Demapper(Symbols,4, 'HARD')
		print 'Encoded: ', (Encoded)
		self.encoded = Encoded
		self.recv_symbols.insert(0.0,Encoded)
		DeintBits = self.CD.de_interleave(Encoded)
		print 'DEint Bits: ',(DeintBits)
		Decoded = self.CD.Decode(DeintBits)
		print 'Decoded: ', Decoded
		String = self.SD.Decode(Decoded)
		print 'String: ', String
			
			
		self.restart_button.grid(row=5,column=0) #pack(pady=10, padx=20)

myGUI = RecvGUI()
myGUI.mainloop()

'''
# Script which integrates the receiver side functionality.
# the reciever Should be run with python 2.7


#PseudoCode:
#	-Initialize communication parameters
#	-Load Users trainingData data
#	-Loop:
#		wait for start Signal
#		Collect data 
#		Send  raw data to detection algorithm get Prob data
#		Decode the data
#		Display the decoded Result
import math
import Source.Channel as CH
import Source.RecvSideLib as RL 
import Source.Frequency_Determination as FD

import csv
import numpy

## DEFINE PARAMETERS ###########
CharSet = 'lowerCaseLiterals'
CharactersPerMessage = 4
SourceEncodeMethod = 'basic'
errorCorrection = 'HardHamming'
FEC_blockSize = 7
FEC_msgSize = 4
# Choose frequencies matching those on the sender side exactly from set:
# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
#  34.48, 35.71, 37.04, 38.46 ]
TransmissionFrequenciesIdeal = [25, 23.81, 28.57, 33.33]
TimePerSymbolSeconds = 4

ChannelSource = 'File'
FlushBuffer = True
Electrodes = ['O1', 'O2', 'P7', 'P8']
DetectionMethod = 'Combined'
DecisionType = 'HARD'
syncMethod = 'KeyPress'
FileWrite = False
readFileName = '20171009-170644.csv' #'20171009-182912.csv'

################################
filetwo = '20171009-182912.csv'
EEGChannel2 = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = filetwo)

################################

# the actual frequencies are the closest FFT bins to a particular sender Freq
TransmissionFrequenciesActual =[23.25, 25, 28.5, 33.25]# FD.mapToClosestFrequencies(TransmissionFrequenciesIdeal, 128*TimePerSymbolSeconds)
print(TransmissionFrequenciesActual)

EEGChannel = CH.Channel(ChannelSource, Electrodes, WriteToFile = FileWrite, ReadFile = readFileName)

Detector = RL.DetectionObject(DetectionMethod,TransmissionFrequenciesActual, None, Electrodes ,TimePerSymbolSeconds, DecisionType)
Detector2 = RL.DetectionObject('CCA',TransmissionFrequenciesActual, None, Electrodes ,TimePerSymbolSeconds, DecisionType)

CharSet = RL.loadCharacterSet(CharSet)
CD= RL.ChannelDecoder(errorCorrection,'HARD',FEC_blockSize,FEC_msgSize)
SD = RL.sourceDecoder(CharSet, SourceEncodeMethod)


recordTime = RL.calculateRecvTime(TimePerSymbolSeconds, len(TransmissionFrequenciesActual), FEC_blockSize, FEC_msgSize, CharactersPerMessage, len(CharSet))
print '9999999: ', recordTime
recordTime = int(recordTime)

#while True:
	#EEGChannel.waitForStart(syncMethod)
data = EEGChannel.getDataBlock(recordTime, FlushBuffer)
target_data = EEGChannel2.getDataBlock(recordTime,FlushBuffer)
#remove mean
target_data = target_data - numpy.mean(target_data)	
data = data - numpy.mean(data)

#bo = Detector.get_knn_data(target_data, data)

Symbols2 = Detector2.getSymbols(data)
Symbols = Detector.getSymbols(target_data)    # find_knn()  #getSymbols(data)

print(Symbols)
print(Symbols2)
#Encoded = RL.Demapper(Symbols,len(TransmissionFrequenciesActual), DecisionType)
#Decoded = CD.Decode(Encoded)
#String = SD.Decode(Decoded)

Encoded2 = RL.Demapper(Symbols2,len(TransmissionFrequenciesActual), DecisionType)
Decoded2 = CD.Decode(Encoded2)
String2 = SD.Decode(Decoded2)

#print(String)
print('AAA: ', String2)

'''
