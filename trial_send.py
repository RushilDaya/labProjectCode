import Source.InputLib as Sender
import time
import os
import Source.TestLib as TestLib

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


def RunSender( file_name , config_parameters, test_option ):
	# function which will execute on the sender

	sendHeader = True 
	if config_parameters["SYNC_METHOD"] == "KeyPress":
		sendHeader = False

	characterSet =  Sender.loadCharacterSet(config_parameters["CHARACTER_SET"])
	sourceEncoder = Sender.srcEncoder(characterSet, config_parameters["SOURCE_ENCODER"])

	channelEncoder = Sender.ChannelEncoder(config_parameters["ERROR_CORRECTION"],\
										   config_parameters["FEC_BLOCK_SIZE"],\
										   config_parameters["FEC_MESSAGE_SIZE"])

	channel = Sender.Channel('FixedFrequencyAndDuty',\
							 config_parameters["TRANSMISSION_FREQUENCIES"],\
							 config_parameters["TIME_PER_SYMBOL"],\
							 sendHeader,\
							 HOLD_FREQUENCY,\
							 HEADER_FREQUENCY)

	# need to do the actual sending here
	symbols = []
	if config_parameters["CHARACTERS_PER_MESSAGE"] !=0:

		message = raw_input("Enter a Message ("+str(config_parameters["CHARACTERS_PER_MESSAGE"])+") characters \n")
		sendBits = sourceEncoder.EncodeData(message)
		encodedBits = channelEncoder.EncodeData(sendBits)
		intBits = channelEncoder.interleave(encodedBits)
		symbols = Sender.SymbolMapping(intBits, len(config_parameters["TRANSMISSION_FREQUENCIES"]))
		print("Symbols to Transmit "+str(symbols))

	if sendHeader:
		channel.sendHeaderV2()
	sendStartTime = time.time()
	print("Starting to Send message at time "+ str(sendStartTime))
	for symbol in symbols:
		channel.send(symbol)
	channel.re_header()

	results = {}
	results["CONFIGURATION"] = config_parameters
	results["SEND_START_TIME"] = sendStartTime

	if test_option != 'protocol_only':
		results["INTERLEAVED_BITS"]= intBits
		results["ENCODED_BITS"]= encBits
		results["BINARY_MESSAGE"]= sendBits
		results["STRING_MESSAGE"]= message

	print(results)
	with open(file_name, 'w') as outfile:
		 json.dump(results, outfile)

def getFile():
	raw_input('Ready For File Input:  press enter to read file')
	message_file = "message_file.txt"
	file = open(message_file,"r")
	file_name = file.read()
	file.close()
	print("With Print to File: "+ file_name)
	return file_name


if __name__ =="__main__":
	
	print('\n +++++++++++++++++++++++ \n Initialize Program...')

	while True:
		test_option = int(raw_input('Test Type: \n1 - full system\n2 - protocol only\n3 - transmission only\n'))
		if test_option not in range(len(TEST_OPTIONS)+1):
			print('invalid option selected')
			continue
		file_name = getFile()
		configuration_parameters = getParameters(test_option)
		RunSender( file_name, configuration_parameters, test_option)

