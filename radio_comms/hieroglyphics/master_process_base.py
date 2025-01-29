#### This is going to be more of a user-interface
#### based program than the rover version, which
#### doesn't *have* a UI, so it will be completely covered
#### by the scheduler and message manager.

# This is the client side of a client-server model.
# This will be sending requests to the rover.

###################
##### IMPORTS #####
###################

import serial
import re
import numpy as np
import cv2
import time
import os
from collections import deque
from message import Message
import struct
import capture_controls
import subprocess
import concurrent.futures

#p.set_printoptions(threshold=sys.maxsize)

messages_from_rover = deque()

#####################
##### FUNCTIONS #####
#####################

def print_options() -> None:
    print("----------------")
    print("MENU OF CONTROLS")
    print("----------------")
    print("(q) to quit")
    print("(log) get most recent 10 msgs of the log")
    print("(ldp) for LD photo")
    print("(hdp) for HD photo")

    # following three may be merged together
    print("(dr) for driving")
    print("(arm) for arm control")
    print("(drl) operate the drill")

    print("(wrd) for sending word to arm to type out")
    print("(hbt) Heartbeat mode: Receive coordinates")

def read_from_port(ser: serial.Serial):
##### READ FROM THE SERIAL PORT
    while True:
        b_input = ser.read(1)
        if len(b_input) != 0:
            print(b_input )
            potential_message = Message(new=False)
            b_input += ser.read(1)
            potential_message.set_msg_id(struct.unpack(">H", b_input)[0])
            b_input = ser.read(1)
            potential_message.set_purpose(b_input)
            b_input = ser.read(1)
            potential_message.number = struct.unpack(">B", b_input)[0]
            b_input = ser.read(struct.calcsize(">L"))
            potential_message.set_size(b_input)
            payload = b''
            # print(potential_message.size_of_payload)
            while len(payload) < potential_message.size_of_payload:
                payload += ser.read(potential_message.size_of_payload - len(payload))
            # print(len(payload))
            potential_message.set_payload(payload)
            potential_message.checksum = ser.read(1)

            messages_from_rover.append(potential_message)

def process_messages() -> None:

    print("thread activated :)")
    while True:
        if len(messages_from_rover) == 0:
            continue
        print("Processing message")
        curr_msg : Message = messages_from_rover.popleft()

        if curr_msg.purpose == 0: # indicates DEBUGGING
            print("debugging message")
            payload = curr_msg.get_payload()
            print(payload.decode())

def main():
    #port = "/dev/tty.usbserial-BG00HO5R"
    port = "/dev/cu.usbserial-B001VC58"
    #port = "COM8"
    baud = 57600
    timeout = 0.01
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    executor = concurrent.futures.ThreadPoolExecutor(3)
    future = executor.submit(process_messages)
    future = executor.submit(read_from_port, ser)

    # the main control
    while True:
        print_options()
        request = input(">> ")
        
        # this request is for debugging, and prints the remaining contents
        # of the buffer into a file
        if request == 'log':
            pass

        if request == "dr":
                # connec to controller?
            capture_controls.pygame.init()
            capture_controls.pygame.joystick.init()
            gen = capture_controls.run({}, 1, False)

            while True:
                lspeed, rspeed, scalar, camleft, camright = next(gen)
                b_lspeed = struct.pack(">f", lspeed)
                b_rspeed = struct.pack(">f", rspeed)
                b_scalar = struct.pack(">f", scalar)
                b_camleft = struct.pack(">B", camleft)
                b_camright = struct.pack(">B", camright)
                payload = b_lspeed + b_rspeed + b_scalar + b_camleft + b_camright

                # pack up the message
                ctrls_msg = Message(new=True, purpose=1, payload=payload)
                print(ctrls_msg.get_as_bytes())

                ser.write(ctrls_msg.get_as_bytes())
        if request == "test":
            while True:
                hello = input("enter tester phrase: ")
                msg = Message(purpose=0, payload=hello.encode())
                ser.write(msg.get_as_bytes())



if __name__ == "__main__":
    main()