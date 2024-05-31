#!/usr/bin/env python3
# CellModuleATFuzz is an AT fuzz ipython script that will check an AT command for parameters and let you define all parameters and run a basic Fuss against those parameters.

import serial
import time
import sys
import re

# global variables
ttyusb = "/dev/tty.usbserial-1421120"  # Point this variable at the cellular module serial port
fuzzfile = './FuzzStrings/fuzzlist-sample.txt'          # set this to file containing fuzz date


# setup serial output parameters
ser = serial.Serial(ttyusb, 115200, timeout=1)
ser.reset_input_buffer()
time_now  = time.strftime("%Y%m%d%H%M%S")

# Read users inputs to be used to build AT query  
print ("Input command to test:")
atcmd = input()
cmd = "AT+"+atcmd+"=?"+"\r"
ser.write(cmd.encode())
msg=ser.read(1024)
msg1 = msg.decode('ascii')
print(msg1)
print ("Input number of parameters that the AT command "+atcmd+" has:")
atcnt = input()
    
# build array structure for AT command parameters and take input for each to start the process

atparm=[]
atparm = [0 for i in range(int(atcnt))] 
count=0
while count <= int(atcnt)-1:
     # value = parts[count]
     print ("Input data for parameter number "+str(count)+" for the AT command "+atcmd)
     atparm[count] = input()
     count += 1

# Take the above input and build a AT cmd to test against the device
atpbck = atparm.copy()
print(atparm)
OrigParam = ','.join(atparm)
cmdA = "AT+"+atcmd+"="+OrigParam+"\r"
print(cmdA)
ser.write(cmdA.encode())
msgA = ser.read(1024)
msgB = msgA.decode('ascii')
print(msgB)


# select parameter to fuz and start fuzzing

print ("Do you want to fuzz a single parameter or multiple. To fuzz all parameters enter ALL, or enter parameter numbers you want to fuzz seperated with , - example 1,2,3,6,8,0")
ParmT = input()

#fuzzing all paramteres

if ParmT == "ALL" or ParmT == "all" or ParmT == "All": 
  acount=0
  print("So you want to fuzz all parameters")
  while acount <= int(atcnt)-1:
    atparm = atpbck.copy()
    with open(fuzzfile) as fp:
       line = fp.readline()
       print("Fuzzing Parameter: ",acount)
       cnt = 1

       while line:
          file1 = open("fuzz_output_"+time_now+".txt", "ab")
          atparm[int(acount)] = line.strip()
          OrigParam = ','.join(atparm)
          cmdF = "AT+"+atcmd+"="+OrigParam+"\r"
          ser.write(cmdF.encode())
          msgF = ser.read(2048)
          m1F = msgF.replace(b'\n', b'\\n')
          m2F= m1F.replace(b'\r', b'\\r')
          file1.write(m2F)
          file1.write(b'\r\n')
          print(msgF)
          # time.sleep(1)
          line = fp.readline()
          cmd2F = "AT+"+atcmd+"?\r"
          ser.write(cmd2F.encode())
          msg2F=ser.read(2048)
          m3F=msg2F.replace(b'\n', b'\\n')
          m4F= m3F.replace(b'\r', b'\\r')
          file1.write(m4F)
          file1.write(b'\r\n')
    acount += 1

# Fuzzing selected parameters

else:
  print("So you want to fuzz parameters: "+ParmT) 
  for nValue in ParmT.split(","):
       print (nValue)
       atparm = atpbck.copy()
       with open(fuzzfile) as fp:
          line = fp.readline()
          print("Fuzzing Parameter: ",nValue) 
          cnt = 1

          while line:
             file1 = open("fuzz_output_"+time_now+".txt", "ab")
             atparm[int(nValue)] = line.strip() 
          

             OrigParam = ','.join(atparm)
             cmdF = "AT+"+atcmd+"="+OrigParam+"\r" 
             ser.write(cmdF.encode())
             msgF = ser.read(2048)
             m1F = msgF.replace(b'\n', b'\\n')
             m2F= m1F.replace(b'\r', b'\\r')
             file1.write(m2F)
             file1.write(b'\r\n')
             print(msgF)
             # time.sleep(1)
             line = fp.readline()
             cmd2F = "AT+"+atcmd+"?\r"
             ser.write(cmd2F.encode())
             msg2F=ser.read(2048)
             m3F=msg2F.replace(b'\n', b'\\n')
             m4F= m3F.replace(b'\r', b'\\r')
             file1.write(m4F)
             file1.write(b'\r\n')

