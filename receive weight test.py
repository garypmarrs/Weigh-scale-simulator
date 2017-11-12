# This program reads the serial output from the Health o meter 349KLX-AA
# The serial output is in binary, 2400, 8, no parity, 1 stop bit
#
# Gary Marrs
# 11-5-17
#

import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    #port='COM1'
	port='COM1',
    baudrate=2400,
    timeout =1
)

ser.isOpen()
weightv = 0
lcount = 0
print "reading string from scale once per second"

while 1 :
    # let's wait one second before reading output (let's give device time to answer)
    time.sleep(1)
    
    #print "number of chars: ", ser.in_waiting
    buffer = ser.read(ser.inWaiting())
    print ':'.join(x.encode('hex') for x in buffer)         # convert to hex
    lcount += 1
    if '\r' in buffer:
        #print "loop count ", lcount
        lines = buffer.split('\r')                          # create list from string
        print "lines ", lines
        val = lines[-2]                                     # grab 2nd to last serial message
        print ':'.join(x.encode('hex') for x in val)        # convert to hex and print
        #' '.join([x.decode('hex') for x in val.split()])
        # print "val - ", val[-5]
        # dont convert weight to float until the scale has given 3 readings
        if lcount >4:
            weightv=float(val[-5:])                         # convert to floating point number
            print "Weight = ", weightv
