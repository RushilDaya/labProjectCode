# Stimulus Side
## Current Version

This version is comprised of two basic elements. A script is to be loaded on the Arduino Uno, this script will toggle port 13 at a frequency defined via serial communication. The second element is a python serial communications object which calculated the uptime and downtime in milliseconds for a certain frequency and duty cycle and transmits it to the arduino

to use:
* load the sketch FixedFrequencyAndDutyOnSerial to the arduino
* use the file testFile.py to change the frequency and duty cycle of arduino Pin 13
* Note: the port name may need to be changed based on which port you have the arduino connected to.