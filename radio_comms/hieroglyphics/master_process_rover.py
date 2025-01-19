# This is the server side of a client-server model.
# This will be receiving requests from the base station.

###################
##### IMPORTS #####
###################

import serial
import cv2
import sys
import struct
import numpy as np
import concurrent.futures
import time
from message import Message
np.set_printoptions(threshold=sys.maxsize)

if __name__ == "__main__":
    #port = "/dev/cu.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM4"
    port = "/dev/ttyTHS1"
    baud = 57600
    timeout = 0.001
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # temporary. to be replaced by a message handler class
    messages : list[Message] = []

    while True:

        ##### READ: SERIAL PORT #####
        potential_message = Message()
        b_input = ser.read(1)
        if len(potential_message) != 0:
            potential_message.set_opcode(b_input)
            b_input = ser.read(1)
            potential_message.set_destination(b_input)
            b_input = ser.read(struct.calcsize(">L"))
            potential_message.set_size(b_input)
            payload = b''
            while len(payload) < potential_message.size_of_payload:
                payload += ser.read(1024)
            potential_message.set_payload(payload=payload)
            messages.add(potential_message)
    
        ##### READ: IMU #####
        