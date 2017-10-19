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
import time
import Source.Channel as CH
import Source.RecvSideLib as RL 
import Source.Frequency_Determination as FD
#Import GUI stuff
import Tkinter as tk 
import tkMessageBox
import ttk
Font_type = ('Times New Roman', 14)
import time

class RecvGUI(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.container = tk.Frame(self, width=500, height=500)
		self.container.pack(side="top", fill="both", expand=True) #, side="top") #, fill="both")
		self.container.grid_rowconfigure(10, weight=1)
		self.container.grid_columnconfigure(10, weight=1)
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
			frame.pack(side='left')
		else:
			frame = self.frames[cont]
	
		frame.tkraise()
		
#inheriting from Frame class of Tkinter	
class recvPage(tk.Frame):
	#class attribute to count number of times this page is returned to
	counter = 0
	
	def __init__(self, main_class, controller, new_instance): 
		#All the widgets required for the receive page
		self.create_objects()
		tk.Frame.__init__(self, main_class) 
		#tk.Frame(width=1, height=1)
		self.page_label = ttk.Label(self, text='BrainChannel - Receiver Side', font=('Times New Roman', 22))
		self.page_label.grid(row=0, column=0,padx=30,pady=100)
		self.recv_button = tk.Button(self, text="Receive", command=lambda:self.setup_receive(main_class))
		self.recv_button.grid(row=5, column=0,padx=30,pady=100)

		#self.gaze_detect = False
		#self.threshold_detect = False
		
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
		self.gaze_detect = tk.Label(self, text="Gaze Detected",fg = "red",bg = "black",font = "Helvetica 16 bold italic")
		self.gaze_detect.grid(row=2, column=0, padx=30, pady=10)
		self.threshold_detect = tk.Label(self, text="Threshold Detected",fg = "red",bg = "black",font = "Helvetica 16 bold italic")
		self.threshold_detect.grid(row=3, column=0, padx=30, pady=10)
		self.recv_button.grid_remove()
		self.symbols_label.grid(row=5, column=0, padx=5, pady=50)
		self.recv_symbols.insert(0.0,'Hallllooo mf')
		self.recv_symbols.grid(row=5, column=1, padx=5, pady=50)
		self.dec_label.grid(row=6, column=0, padx=5, pady=50)
		self.dec_msg.grid(row=6, column=1, padx=5, pady=50)

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
		## DEFINE PARAMETERS ###########
		self.CharSet = 'lowerCaseLiterals'
		self.CharactersPerMessage = 5
		self.SourceEncodeMethod = 'basic'
		self.errorCorrection = 'HardHamming'
		self.FEC_Size = 7
		self.FEC_msg = 4
		# Choose frequencies matching those on the sender side exactly from set:
		# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
		#  34.48, 35.71, 37.04, 38.46 ]
		self.TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
		self.TimePerSymbolSeconds = 4

		self.ChannelSource = 'File'
		self.FlushBuffer = True
		self.Electrodes = ['O1','O2','P7','P8']
		self.DetectionMethod = 'PSDA'
		self.DecisionType = 'HARD'
		self.syncMethod = 'KeyPress' #'HeaderV2'
		self.FileWrite = False
		self.readFileName = '20171009-182912.csv'
###########################
		self.TransmissionFrequenciesActual = FD.mapToClosestFrequencies(self.TransmissionFrequenciesIdeal, 128*self.TimePerSymbolSeconds)
		print(self.TransmissionFrequenciesActual)

		self.EEGChannel = CH.Channel(self.ChannelSource, self.Electrodes, WriteToFile = self.FileWrite, ReadFile = self.readFileName, useHeader = False, holdFreq = 28.57, headerFreq = 30.30, startThreshold = 300,startThresholdRelative=0.8, crossoverThresholdRelative=0.5)

		self.Detector = RL.DetectionObject(self.DetectionMethod,self.TransmissionFrequenciesActual, None, self.Electrodes ,self.TimePerSymbolSeconds, self.DecisionType)
		self.CharSet = RL.loadCharacterSet(self.CharSet)
		self.CD = RL.ChannelDecoder(self.errorCorrection,'HARD',self.FEC_Size,self.FEC_msg)
		self.SD = RL.sourceDecoder(self.CharSet, self.SourceEncodeMethod)


		self.recordTime = RL.calculateRecvTime(self.TimePerSymbolSeconds, len(self.TransmissionFrequenciesActual), self.FEC_Size, self.FEC_msg, self.CharactersPerMessage, len(self.CharSet))
		print(self.recordTime)
		self.recordTime = int(self.recordTime)

	
	def run_receiver(self):
		
		#if self.EEGChannel.waitForStart(self.syncMethod) == True:
		#time.sleep(10)
		if self.syncMethod == 'HeaderV2':
			if self.EEGChannel.gaze_detect():
				self.set_gaze_detected()
			if self.EEGChannel.threshold_detect():
				self.set_threshold_detect()
		else:
			self.EEGChannel.waitForStart(self.syncMethod)
		
		data = self.EEGChannel.getDataBlock(self.recordTime, self.FlushBuffer)
		print 'DATA: ', data
		Symbols = self.Detector.getSymbols(data)
		print(Symbols)
		self.recv_symbols.insert(0.0,Symbols)
		Encoded = RL.Demapper(Symbols,len(self.TransmissionFrequenciesActual), self.DecisionType)
		print(Encoded)
		Decoded = self.CD.Decode(Encoded)
		String = self.SD.Decode(Decoded)
		self.dec_msg.insert(0.0,String)
		print(String)
			
			
		self.restart_button.grid(row=8,column=0) #pack(pady=10, padx=20)
		
	def set_gaze_detected(self):
		self.gaze_detect = tk.Label(self, text="Gaze Detected",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic").grid(row=2, column=0)
		
	def set_threshold_detect(self):
		self.threshold_detect = tk.Label(self, text="Threshold Detected",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic").grid(row=3, column=0)



myGUI = RecvGUI()
myGUI.geometry("600x600")
myGUI.mainloop()
