# this file will be used merely to determine properties of the
# header it should be deleted.


# create a detector 
# roll values into the detector 
import Source.InputLib as IL
import time



Channel = IL.Channel('FixedFrequencyAndDuty',[23.26, 25],1)
time.sleep(2)
Channel.setSingleFreq(28.57)
time.sleep(20)
Channel.setSingleFreq(30.30)
time.sleep(4)
Channel.setSingleFreq(28.57)
time.sleep(20)
Channel.setSingleFreq(23.26)
time.sleep(20)

