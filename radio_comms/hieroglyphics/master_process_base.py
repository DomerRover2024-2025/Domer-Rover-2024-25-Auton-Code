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
import numpy as np
import cv2
import time
from message import Message
import struct
import concurrent.futures

#p.set_printoptions(threshold=sys.maxsize)

#####################
##### FUNCTIONS #####
#####################

def print_options() -> None:
    print("----------------")
    print("MENU OF CONTROLS")
    print("----------------")
    print("(0) to quit")
    print("(1) for photo")
    print("(2) for interactive mode")
    print("(3) for sending word to arm to type out")
    print("(4) Heartbeat mode: Receive coordinates")

def read_from_port(ser: serial.Serial, messages : list[Message]):
##### READ FROM THE SERIAL PORT
    ##### TODO this should be threaded, I think
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

        # TODO replace with a message manager
        messages.append(potential_message)

def main():
    port = "/dev/tty.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM3"
    baud = 57600
    timeout = 3
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # must be replaced with some sort of message manager
    messages = []

    # TODO thread the reading into the messages list thing

    # the main control
    while True:
        print_options()
        request = input(">> ")
        request = int(request)

        if request == 2:
            while True:
                # just 17 0's
                example_data = [0 for _ in range(0,18)]
                # TODO pack the data
                ctrls_msg = Message(opcode=0, destination=0, payload=example_data)
                ser.write(ctrls_msg.get_as_bytes())
                time.sleep(0.2)

        ##### TODO read from joystick talker?

if __name__ == "__main__":
    main()