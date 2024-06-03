#!/usr/bin/env python3
#
###################################################
#        _______    ____                          #
#     /\|__   __|  / __ \                         #
#    /  \  | |    | |  | |_   _  ___ _ __ _   _   #
#   / /\ \ | |    | |  | | | | |/ _ \ '__| | | |  #
#  / ____ \| |    | |__| | |_| |  __/ |  | |_| |  #
# /_/    \_\_|     \___\_\\__,_|\___|_|   \__, |  #
#                                          __/ |  #
#                                         |___/   #
#                                                 #
###################################################
#       Deral Heiland & Carlota Bindner          #
#                Version 0.1B                     #
#                    2024                         #
###################################################

import serial
import time
import sys
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Send AT commands to a cell module.")
    parser.add_argument('brand', choices=['UBLOX', 'TELIT', 'QUECTEL', 'CINTERION'], help="Select the brand of the module.")
    parser.add_argument('mode', choices=['READ', 'TEST'], help="Select the mode: READ or TEST.")
    return parser.parse_args()

def modify_command(command, mode):
    if mode == 'TEST':
        return command.strip() + '=?\r'
    elif mode == 'READ':
        return command.strip() + '?\r'
    return command

if __name__ == '__main__':
    args = parse_args()
    try:
        # setup serial output parameters
        ser = serial.Serial('/dev/tty.usbserial-1421120', 115200, timeout=1) # Change to point to FTDI connected to Cell Module
        ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"Error: Could not open serial connection . Please check the serial dev and set it within the code on line 40 and try again.")
        sys.exit(1)
    time_now = time.strftime("%Y%m%d%H%M%S")

    # Determine file path based on the selected brand
    filepath = f'./ATCMDS/{args.brand}.dat'
    if not os.path.isfile(filepath):
        print(f"Error: The file {filepath} does not exist.")
        sys.exit(1)

    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1

        # While reading file line pass AT command to serial write and read results and write out to file
        while line:
            file1 = open("results_" + time_now + ".txt", "ab")
            cmd = modify_command(line.strip(), args.mode)
            # print(cmd)
            ser.write(cmd.encode())
            msg = ser.read(1024)
            m1 = msg.replace(b'\n', b'\\n')
            m2 = m1.replace(b'\r', b'\\r')
            file1.write(m2)
            file1.write(b'\r\n')
            print(msg)
            line = fp.readline()
            cnt += 1

    # close output file
    file1.close()

