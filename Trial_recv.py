# the reciever side code
# starts up the emotiv 
# no visual in this routine for now

# startup emotiv

# run loop:
	# setup user directory and create file (based on trail type) to write in
	# run the user throught the run. its useful to display basic info to the user as the trial is underway

import math
import time
import Source.Channel as Channel
import Source.RecvSideLib as Reciever  
import Source.Frequency_Determination as Frequencies
import numpy
import Source.TESTLIB as TestLib
import os
import random
import time
import copy
import json
import csv

DEFAULT_PARAMETERS ={
	"CHARACTER_SET": 'lowerCaseLiterals',
	"CHARACTERS_PER_MESSAGE": 5,
	"SOURCE_ENCODER": 'basic',
	"ERROR_CORRECTION": 'HardHamming',
	"FEC_BLOCK_SIZE": 7,
	"FEC_MESSAGE_SIZE":4,
	"TIME_PER_SYMBOL":4,
	"CHANNEL_SOURCE": 'Emokit',
	"FLUSH_BUFFER": True,
	"ELECTRODES":['O1','O2','P7','P8'],
	"DECISION_TYPE":'HARD',
	"SYNC_METHOD": "HeaderV2",
	"FILE_WRITE":False,
	"TRANSMISSION_FREQUENCIES" : [23.26, 25, 26.36, 27.78 ,28.57, 30.30, 31.25, 33.33]
}

TEST_OPTIONS = ['full_system','protocol_only','transmission_only']

HOLD_FREQUENCY = 28.57
HEADER_FREQUENCY = 30.30
CROSSOVER_THRESHOLD_RELATIVE = 0.5
START_THRESHOLD = 300
START_THRESHOLD_RELATIVE = 0.8



def getParameters(test_type):
	customParameters = DEFAULT_PARAMETERS.copy()
	print('Set System Parameters:\n')
	for key in customParameters:
		new_setting = raw_input( str(key)+' (' + str(customParameters[key]) + '): ')
		if new_setting != '':
			try:
				customParameters[key] = int(new_setting)
			except:
				customParameters[key] = int(new_setting)

    # these parameters must be hard set as they configure the different tests.
	if test_type == "full_system":
		customParameters["SYNC_METHOD"] = "HeaderV2"

	elif test_type == "protocol_only":
		customParameters["SYNC_METHOD"] = "HeaderV2"
		customParameters["CHARACTERS_PER_MESSAGE"]=0

	elif test_type == "transmission_only":
		customParameters["SYNC_METHOD"] = "KeyPress"

	else:
		raise TypeError('Invalid test_type provided to get parameters function')
	return customParameters


def CreateFiles(username, testType):
	# will insert a new file or clear out an existing file
	# inserts in the testType/ folder
	# will create a file called username_run_n.json (with results) & username_run_n.csv (with raw data)
	print('entering file creation')
	path = os.getcwd()
	path = path + '\\trials\\'+testType
	if not os.path.exists(path):
		os.makedirs(path)

	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
	files = [file for file in files if file.find(username) !=-1]
	csv_files = [file for file in files if file.find('.csv') != -1]
	json_files = [file for file in files if file.find('.json') != -1]

	if len(csv_files) != len(json_files):
		print('inconsistent files please clean up directory')
		raise TypeError

	random.seed(time.time())
	trial_id = str(random.randint(1000000000, 9000000000))
	name_of_csv = path+'\\'+ username+'_trial_'+ trial_id +'.csv'
	name_of_json = path+'\\' + username+'_trial_'+ trial_id +'.json'
	name_of_sender_json = path+'\\' + username+'_trial_'+ trial_id+'_SENDER' +'.json'


	open(name_of_json, 'w').close()
	open(name_of_csv, 'w').close()
	open(name_of_sender_json, 'w').close()

	print('file creation completed')
	return [name_of_csv, name_of_json, name_of_sender_json, trial_id ]



def RunReciever( data_file, results_file , config_parameters, test_option ):
	# function which will execute a run of the emotiv reciever

	channel = Channel.Channel(config_parameters["CHANNEL_SOURCE"], config_parameters["ELECTRODES"], config_parameters["FILE_WRITE"],\
					  holdFreq= HOLD_FREQUENCY, headerFreq = HEADER_FREQUENCY ,startThreshold= START_THRESHOLD ,\
					  startThresholdRelative= START_THRESHOLD_RELATIVE,\
					  crossoverThresholdRelative= CROSSOVER_THRESHOLD_RELATIVE )
	detectorCCA = Reciever.DetectionObject("CCA", config_parameters["TRANSMISSION_FREQUENCIES"], None, config_parameters["ELECTRODES"], config_parameters["TIME_PER_SYMBOL"],config_parameters["DECISION_TYPE"])
	detectorPSDA = Reciever.DetectionObject("PSDA", config_parameters["TRANSMISSION_FREQUENCIES"], None, config_parameters["ELECTRODES"][0], config_parameters["TIME_PER_SYMBOL"],config_parameters["DECISION_TYPE"])


	channelDecoder = Reciever.ChannelDecoder(config_parameters["ERROR_CORRECTION"],"HARD",\
					config_parameters["FEC_BLOCK_SIZE"], config_parameters["FEC_MESSAGE_SIZE"])

	characterSet =  Reciever.loadCharacterSet(config_parameters["CHARACTER_SET"])
	sourceDecoder = Reciever.sourceDecoder(characterSet,config_parameters["SOURCE_ENCODER"])


	#calculate the record time
	recordTime = Reciever.calculateRecvTime(config_parameters["TIME_PER_SYMBOL"],\
										    len( config_parameters["TRANSMISSION_FREQUENCIES"] ),\
										    config_parameters["FEC_BLOCK_SIZE"],\
										    config_parameters["FEC_MESSAGE_SIZE"],\
										    config_parameters["CHARACTERS_PER_MESSAGE"],\
										    len(characterSet))
	print('calculated record time is: '+ str(recordTime))

	# need to now do the actual recording here
	# channel.setFileName(data_file)

	if config_parameters["SYNC_METHOD"] == 'HeaderV2':
		print('--- DETECTING GAZE ----')
		channel.gaze_detect()
		print('--- GAZE DETECTED ----')
		channel.threshold_detect()
		print('--- THRESHOLD DETECTED ----')
	else:
		channel.waitForStart(config_parameters["SYNC_METHOD"])


	recordStartTime = time.time()
	symbolsToCapture = int(float(recordTime)/float(config_parameters["TIME_PER_SYMBOL"]))
	print("--- DATA RECORDING STARTED --- " + str(recordStartTime))
	channel.flushBuffer()

	symbolsCCA = []
	symbolsPSDA = []
	Data = numpy.zeros((0, len(config_parameters["ELECTRODES"])))
	for symbol in range(symbolsToCapture):
		print("Getting Symbol "+str(symbol)+'. . . .')
		DataBlock = channel.getDataBlock(int(config_parameters["TIME_PER_SYMBOL"]),False)
		Data = numpy.concatenate([Data, DataBlock])
		print( 'Number of samples collected: ' + str(len(DataBlock)))

		symbolsPSDA.append(detectorPSDA.getSymbols(DataBlock)[0])
		symbolsCCA.append(detectorCCA.getSymbols(DataBlock)[0])
		print('psda symbol vector :' + str(symbolsPSDA))
		print('cca symbol vector :' +  str(symbolsCCA))

	if int(recordTime) != 0:
		intCCA =     Reciever.Demapper(symbolsCCA,  len(config_parameters["TRANSMISSION_FREQUENCIES"] ),'HARD')
		intPSDA =    Reciever.Demapper(symbolsPSDA,len(config_parameters["TRANSMISSION_FREQUENCIES"] ),'HARD')
		encodedCCA = channelDecoder.de_interleave(intCCA)
		encodedPSDA =channelDecoder.de_interleave(intPSDA)
		binaryCCA =  channelDecoder.Decode(encodedCCA)
		binaryPSDA = channelDecoder.Decode(encodedPSDA)
		StringCCA =  sourceDecoder.Decode(binaryCCA)
		StringPSDA = sourceDecoder.Decode(binaryPSDA)
		print('Message Recieved from the CCA reciever '+StringCCA)
		print('Message Recieved from the PSDA reciever '+StringPSDA)

	successful = raw_input("Was this a successful run (Y/n): ")
	comments = raw_input("Provide any comments on the trial here: \n")

	results = {}
	results["SUCCESSFUL"] = successful
	results["COMMENTS"] = comments
	results["CONFIGURATION"] = config_parameters
	results["RECORD_START_TIME"] = recordStartTime

	if test_option != 'protocol_only':
		results["INTERLEAVED_CCA"]= intCCA
		results["INTERLEAVED_PSDA"]= intPSDA 
		results["ENCODED_CCA"]= encodedCCA
		results["ENCODED_PSDA"]= encodedPSDA
		results["BINARY_CCA"]= binaryCCA
		results["BINARY_PSDA"]= binaryPSDA
		results["STRING_PSDA"]= StringPSDA
		results["STRING_CCA"]= StringCCA

	print(results)
	with open(results_file, 'w') as outfile:
		 json.dump(results, outfile)

	with open(data_file,'w') as outfile:
		outfile.write(Data)

	data_file = open(data_file,'w')
	writer = csv.writer(data_file)
	for i in range(len(Data)):
		writer.writerow(Data[i])
	data_file.close()

def cleanUpSenderFile():
	messageFile = 'message_file.txt'
	open(messageFile, 'w').close()

def messageSender(file_name):
	messageFile = 'message_file.txt'
	with open(messageFile,'w') as outfile:
		outfile.write(file_name)
	print('Message written to communication File')
	raw_input('Press Enter once the reciever has obtained the message')


if __name__ =="__main__":
	
	print('\n +++++++++++++++++++++++ \n Initialize Program...')

	while True:
		# setup routine:
		cleanUpSenderFile()
		name = raw_input('Participant Name: ').upper()
		test_option = int(raw_input('Test Type: \n1 - full system\n2 - protocol only\n3 - transmission only\n'))
		if test_option not in range(len(TEST_OPTIONS)+1):
			print('invalid option selected')
			continue
		test_option = TEST_OPTIONS[test_option-1]
		[csv_file_name, json_file_name, name_of_sender_file ,trial_id] = CreateFiles(name,test_option)
		messageSender(name_of_sender_file)
		configuration_parameters = getParameters(test_option)
		RunReciever( csv_file_name, json_file_name, configuration_parameters, test_option)

