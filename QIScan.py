#!/usr/bin/env python3
#########################################
#     ____    _________                 #
#    / __ \  /  _/ ___/_________ _____  #
#   / / / /  / / \__ \/ ___/ __ `/ __ \ #
#  / /_/ / _/ / ___/ / /__/ /_/ / / / / #
#  \___\_\/___//____/\___/\__,_/_/ /_/  #
#                                       #
#########################################
#                                       #
#  Proof of concept code for leverging  #
#  AT commands to conduct port scanning #
#  over cellular modules                #
#                                       #
#########################################
#       Deral Heiland @percent_x        #
#             June 2024                 #
######################################### 

import serial
import time

# Configuration variables
port = '/dev/tty.usbserial-DT03NNX0'  # Update this to your module's serial port
baudrate = 115200
timeout = 5  # Seconds to wait for a response

# List of IPs and ports to scan
# ip_addresses = ['192.168.1.100', '192.168.1.101']  # Example IPs
ip_addresses = ['45.33.32.156']  # IP is scanme.nmap.org
ports = [21,22,23,80,3389,8080,9929,31337]

# Initialize serial connection
ser = serial.Serial(port, baudrate, timeout=timeout)

def send_at_command(command):
    """Send an AT command and return the response."""
    ser.write((command + '\r\n').encode())
    time.sleep(2)  # Give the module time to respond
    response = ser.read_all().decode()
    return response

# Open TCP connections on specified IPs and ports
for ip in ip_addresses:
    for port in ports:
        at_command_open = f'AT+QIOPEN=1,0,"TCP","{ip}",{port},0,0'
        at_command_close = f'AT+QICLOSE=0,10'
        response = send_at_command(at_command_open)
        print(f"\033[91mTCP Port Check on {ip}:{port}")
        print(f"\033[0;32m{response}")
        time.sleep(2)  # Prevent overwhelming the module
        response = send_at_command(at_command_close)
        time.sleep(1)  # Prevent overwhelming the module

# Close the serial connection
ser.close()

