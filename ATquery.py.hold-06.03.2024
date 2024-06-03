#!/usr/bin/env python3
import serial
import time
import sys

if __name__ == '__main__':

# setup serial output parameters
    ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=1) # Change to point to FTDI connected to Cell Module
    ser.reset_input_buffer()
    time_now  = time.strftime("%Y%m%d%H%M%S")

# Read from file
    # filepath = './AT_UBLOX_TEST.txt'
    filepath = './AT_UBLOX_READ.txt' # Enter the correct file name and path for AT commands to test with
    with open(filepath) as fp:
       line = fp.readline()
       cnt = 1

# While reading file line pass AT command to serial write and read results and write out to file
       while line:
          file1 = open("results_"+time_now+".txt", "ab")
          junk = ("Line {}: {}".format(cnt, line.strip())) 
          cmd = junk+"\r"
          ser.write(cmd.encode())
          msg=ser.read(1024)
          m1=msg.replace(b'\n', b'\\n')
          m2= m1.replace(b'\r', b'\\r')
          file1.write(m2)
          file1.write(b'\r\n')
          print(msg)
          line = fp.readline()
          cnt += 1

# close output file
file1.close()
