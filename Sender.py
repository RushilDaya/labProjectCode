# Sender Side Frame Work Script

# this script is a sender Side client which allows for the user
# to send data in a from keyboard input to the LED output
# this script is a framework and allows modules to change

#PseudoCode:
# Init Variables
# Enter Loop:
#	get user Input
#	Encode stream to bits 
#	Perform FEC 
#	Send Data to the Serial Out Module
#	wait for stream to finish
#	

import Source.InputLib  as IL
import time
import Tkinter as tk 
import tkMessageBox
import ttk
Font_type = ('Times New Roman', 14)
import time

class SendGUI(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.container = tk.Frame(self, width=500, height=500)
		self.container.pack(side="top", fill="both", expand=True) #, side="top") #, fill="both")
		self.container.grid_rowconfigure(10, weight=1)
		self.container.grid_columnconfigure(10, weight=1)
		self.frames = {} #initialise array for app pages - start page, home page, send page
		
		frame = sendPage(self.container, self, 'no') #, self.connect) #, self.tcp_obj, self.pop3_obj)
		self.frames[sendPage] = frame
		frame.grid(row=0, column=0) #pack()
		
		self.renderFrame(sendPage, 'no')
			
		
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
class sendPage(tk.Frame):
	#class attribute to count number of times this page is returned to
	counter = 0
	
	def __init__(self, main_class, controller, new_instance): 
		#All the widgets required for the receive page
		self.create_objects()
		tk.Frame.__init__(self, main_class) 
		#tk.Frame(width=1, height=1)
		self.main_class = main_class
		
		self.setup_send(main_class)
		

		#self.gaze_detect = False
		#self.threshold_detect = False
		
		sendPage.counter += 1
		
	def setup_send(self, main_class):
		self.page_label = ttk.Label(self, text='BrainChannel - Sender Side', font=('Times New Roman', 22))
		self.page_label.grid(row=0, column=0,padx=30,pady=30)
		self.send_button = tk.Button(self, text="Send Message:", command=lambda:self.run_send())
		self.send_button.grid(row=1, column=0,padx=0,pady=30)
		self.send_msg = tk.StringVar()
		self.msg_entry = ttk.Entry(self, textvariable=self.send_msg)
		self.msg_entry.grid(row=1, column=1, padx=0, pady=30)
		
		self.sent_header = tk.Label(self, text="Header Sent",fg = "red",bg = "black",font = "Helvetica 16 bold italic")
		self.sent_header.grid(row=2, column=0, padx=30, pady=5)
		self.sending_msg = tk.Label(self, text="Sending Message",fg = "red",bg = "black",font = "Helvetica 16 bold italic")
		self.sending_msg.grid(row=2, column=1, padx=30, pady=5)
		
		self.sentf_label = ttk.Label(self, text='Sent Frequencies/Symbols: ', font=Font_type)
		self.sentf_label.grid(row=4, column=0, pady=20, padx=5)
		self.sent_freq = tk.Text(self, width=35, height=1)
		self.sent_freq.grid(row=4, column=1)
		self.symbols_label = ttk.Label(self, text='Symbols: ', font=Font_type)
		self.symbols_label.grid(row=5,column=0, pady=20, padx=5)
		self.symbols = tk.Text(self, width=35, height=1)
		self.symbols.grid(row=5, column=1) 
		self.sentb_label = ttk.Label(self, text='Send Bits: ', font=Font_type)
		self.sentb_label.grid(row=6,column=0,pady=20, padx=0)
		self.send_bits = tk.Text(self, width=35, height=1)
		self.send_bits.grid(row=6, column=1)
		self.enc_label = ttk.Label(self, text='Encoded Bits: ', font=Font_type)
		self.enc_label.grid(row=7, column=0, pady=20, padx=0)
		self.enc_bits = tk.Text(self, width=35, height=1)
		self.enc_bits.grid(row=7, column=1)
		
		self.restart_button = tk.Button(self, text = 'Send Another Message',command=lambda:self.restart(main_class))

			
	def restart(self, main_class):
		#self.page_label.pack_forget() #
		self.page_label.grid_remove() #3pack_forget()
		self.send_button.grid_remove()
		self.msg_entry.grid_remove()
		self.sentf_label.grid_remove()
		self.sent_freq.grid_remove()
		self.symbols_label.grid_remove()
		self.symbols.grid_remove()
		self.sentb_label.grid_remove()
		self.send_bits.grid_remove()
		self.enc_label.grid_remove()
		self.enc_bits.grid_remove()
		self.restart_button.grid_remove()
		self.sent_header.grid_remove()
		
		self.setup_send(main_class)
		

	def create_objects(self):
		## DEFINE PARAMETERS ###########
		self.CharSet = 'lowerCaseLiterals'
		self.CharactersPerMessage = 5
		self.SourceEncodeMethod = 'basic'
		self.errorCorrection = 'HardHamming'

		# NOTE: Only use frequencies From the following Set:
		# [23.26, 23.81, 24.39, 25, 25.64, 26.36, 27.03, 27.78, 28.57, 29.41, 30.30, 31.25, 32.26, 33.33,
		#  34.48, 35.71, 37.04, 38.46 ]
		self.TransmissionFrequenciesIdeal = [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]

		self.TimePerSymbolSeconds = 4

		
		self.ValidDictionary = IL.loadCharacterSet(self.CharSet)
		self.InputValidationObject = IL.InputValidation(self.ValidDictionary,self.CharactersPerMessage)
		self.SrcEncoder  = IL.SrcEncoder(self.ValidDictionary , self.SourceEncodeMethod)
		self.FEC = IL.ChannelEncoder(self.errorCorrection,7,4)
		self.Chan = IL.Channel('FixedFrequencyAndDuty',self.TransmissionFrequenciesIdeal,self.TimePerSymbolSeconds, True, 28.57,30.30)

	
	def run_send(self):
		
		sendString = (self.send_msg.get()) #self.InputValidationObject.getInput()
		#print 'JJJJ:: ', (sendString)
		time.sleep(2)
		SendBits = self.SrcEncoder.EncodeData(sendString)
		print(SendBits)
		self.send_bits.insert(0.0, SendBits)
		EncBits = self.FEC.EncodeData(SendBits)
		print(EncBits)
		self.enc_bits.insert(0.0, EncBits)
		IntBits = self.FEC.interleave(EncBits)
		
		Symbols  = IL.SymbolMapping(IntBits, len(self.TransmissionFrequenciesIdeal))
		print(Symbols)
		self.symbols.insert(0.0, Symbols)
		
		self.sent_header = tk.Label(self, text="Sending Header...",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic")
		self.sent_header.grid(row=2, column=0, padx=30, pady=5)
		self.main_class.update()
		self.Chan.sendHeaderV2()
		
		
		self.sent_header.grid_remove()
		self.sent_header = tk.Label(self, text="Header Sent",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic")
		self.sent_header.grid(row=2, column=0, padx=30, pady=5)
		self.main_class.update()
		
		print time.time()
		self.sending_msg.grid_remove()
		self.sending_msg = tk.Label(self, text="Sending Message...",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic")
		self.sending_msg.grid(row=2, column=1, padx=30, pady=5)
		self.main_class.update()
		for symbol in Symbols:
			fre = self.Chan.send(symbol)
			self.sent_freq.insert(0.0, fre)
			self.main_class.update()
			
		self.sending_msg.grid_remove()
		self.sending_msg = tk.Label(self, text="Message Sent",fg = "light green",bg = "dark green",font = "Helvetica 16 bold italic")
		self.sending_msg.grid(row=2, column=1, padx=30, pady=5)
			
		self.Chan.re_header()
			
		self.restart_button.grid(row=8,column=0) #pack(pady=10, padx=20)
		



myGUI = SendGUI()
myGUI.geometry("600x600")
#myGUI.update_idletasks() #  after(100, 'update')
#myGUI.update()
myGUI.mainloop()

