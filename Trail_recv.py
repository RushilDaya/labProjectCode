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
	"FILE_WRITE":True,
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
			customParameters[key] = new_setting

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


	open(name_of_json, 'w').close()
	open(name_of_csv, 'w').close()

	print('file creation completed')
	return [name_of_csv, name_of_json, trial_id ]



def RunReciever( data_file, results_file , config_parameters ):
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


	# need to now do the actual recording here



if __name__ =="__main__":
	
	print('\n +++++++++++++++++++++++ \n Initialize Program...')

	while True:
		# setup routine:

		name = raw_input('Participant Name: ').upper()
		test_option = int(raw_input('Test Type: \n 1 - full system\n'))
		if test_option not in range(len(TEST_OPTIONS)):
			print('invalid option selected')
			continue
		test_option = TEST_OPTIONS[test_option-1]
		[csv_file_name, json_file_name, trial_id] = CreateFiles(name,test_option)
		configuration_parameters = getParameters(test_option)
		RunReciever( csv_file_name, json_file_name, configuration_parameters)

