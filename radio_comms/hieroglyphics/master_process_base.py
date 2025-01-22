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
from message import Message
import struct
import subprocess
import concurrent.futures

#p.set_printoptions(threshold=sys.maxsize)

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
    timeout = 0.01
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    messages = []

    # the main control
    while True:
        print_options()
        request = input(">> ")
        
        # this request is for debugging, and prints the remaining contents
        # of the buffer into a file
        if request == 'log':
            pass

        time.sleep(0.25)
        ###### end connection ######
        if request == 0: 
            print("Request to quit sent.")

            # read whether the server quit or not
            ack = struct.unpack("=B", ser.read(1))

            # if the return acknowledgment is 1, then request was successful
            if ack[0] == 1:
                print("Request successful.")
                break
            else:
                print("Request unsuccessful.")

        ##### ask for a photo #####
        elif request == 1:
            request_and_read_image(ser)
        #     size_of_image = b''
        #     while len(size_of_image) != struct.calcsize(">L"):
        #         # read the size of the image from the server
        #         size_of_image += ser.read(struct.calcsize(">L"))

        # # if actually grabbed a number the length of the size of the image,
        # # unpack it and send an acknowledgment that it was received
        #     size_of_image = struct.unpack(">L", size_of_image)[0]
        #     print("size of image:", size_of_image)

        #     # if the size of the image is 0 interpret as a fail
        #     if size_of_image == 0:
        #         print("Image capturing failed. Returning to menu.")
        #         continue
    
        #     print("Size received. Sending acknowledgement.")
        #     ser.write(struct.pack("=B", 1))

        #     b_output = b''
        #     time.sleep(1)

        #     print("Reading image.")

        #     # keep reading until the entire image is read
        #     while len(b_output) < size_of_image:
        #         b_output += ser.read(8_192) # duplicate of 2

        #     print("Bytes equal to size of image read.")

        #     # save and output the image
        #     success = save_and_output_image(b_output=b_output)
        #     if not success:
        #         print("Image failed to be saved/shown.")
        #     else:
        #         print("Image successfully saved and shown.")

        # ##### interactive, controller mode #####
        elif request == 2:
            pass
        #     interactive_mode(ser)
        #     # print("Entering interactive mode. Connecting to controller...")
            
            # # !TODO: fix this controller whatnot
            # # send controller connected
            # controller_connected = True
            
            # joysticks = {}

            # # send over that the controller connected
            # ser.write(struct.pack("=B", controller_connected))

            # # if the controller failed (also unnecessary right now)
            # if not controller_connected:
            #     print("Controller not responding. Exiting interactive mode, sending update.")
            #     continue

            # print("Controller responded.")
            # print("Use the controller now:")

            # # this is a generator to control the controller
            # run = joystickDriving.run(joysticks)

            # # set things up to receive photos at the same time
            # image_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            # keep_reading_images = True
            # future = image_executor.submit(read_images, ser)

            # try:
            #     good_control = 1
            #     while True:
            #         #current_control = input(">> ")

            #         # get the current controls, which is a 16-long array of
            #         # mixed int and float values
            #         try:
            #             current_control = next(run)
            #         except Exception as e:
            #             print(e)
            #             good_control = 0
            #             # if not len(current_control):
            #             #     print("Please enter a number.", file=sys.stderr)
            #             #     continue
            #             # try:
            #             #     int_curr_control = int(cSurrent_control)
            #             # except ValueError as v:
            #             #     print(f"{v}: please enter an integer in [0, 255].", file=sys.stderr)
            #             #     continue
            #             # if int(current_control) > 255 or int(current_control) < 0:
            #             #     print("Controls must be between 0 and 255.", file=sys.stderr)
            #             #     continue
            #         ser.write(struct.pack(">B", good_control))

            #         # stop sending over anything if the controller failed or something along those lines
            #         if good_control == 0:
            #             break

            #         #!TODO: This doesn't work. the ints/floats are ordered strangely in sean's code
            #         float_controls = current_control[:2]
            #         int_controls = current_control[2:]
            #         ser.write(struct.pack(">f", float_controls[0]))
            #         ser.write(struct.pack(">f", float_controls[1]))
            #         ser.write(bytearray(int_controls))
            #         #ser.write(struct.pack("=B", int(current_control)))

            #         # on exit:
            #         if False:
            #         #if int(current_control) == 1_000:
            #             break
            # except Exception as e:
            #     print(e)
            # finally:
            #     keep_reading_images = False
            #     print("cancelling future")
            #     future.cancel()
            #     print("shutting down executor")
            #     image_executor.shutdown()
            #     print("outwaiting: ", ser.out_waiting)
            #     print("inwaiting: ", ser.in_waiting)
            #     data_lost = flush_whats_coming_in(ser)
            #     print("data lost: ", data_lost)

            #     #read_images(ser)

            # print("Quitting interactive mode.")

        ##### send arm a word to autonomously take care of
        elif request == 3:
            arm_request(ser)
            # print("Input word to command arm: ")
            # word = input(">> ")

            # ser.write(f"{word}\n".encode())

            # print("Sent word.")
        
        ##### heartbeat mode: simply receive the float coordinates
        elif request == 4:
            heartbeat(ser)
            # print("Activating heartbeat mode. ^C to quit.")
            # print("Receiving coordinates...")
            # try:
            #     while True:
            #         coordinates = ser.readline()
            #         if len(coordinates) == 0:
            #             print("Rover could not be found.")
            #             continue

            #         coord_x, coord_y = coordinates.decode().split()

            #         print(f"coord_x = {coord_x}, coord_y = {coord_y}")
            # except KeyboardInterrupt:
            #     print("Exiting heartbeat mode.")
            #     ser.write(b"1")        
        ##### TODO read from joystick talker?

if __name__ == "__main__":
    main()