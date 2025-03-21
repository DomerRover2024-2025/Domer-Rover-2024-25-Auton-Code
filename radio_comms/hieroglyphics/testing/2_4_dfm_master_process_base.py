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
from datetime import datetime

#######################
##### GLOBAL VARS #####
#######################

messages_from_rover = deque()
MSG_LOG = "messages_base.log"

################
##### MAIN #####
################

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
        
        if request == 'quit':
            exit_main()
            return 0

        # this request is for debugging, and prints the remaining contents
        # of the buffer into a file
        if request == 'log':
            tail_output = subprocess.run(["tail", '-n', 10, MSG_LOG], capture_output=True, text=True)
            print(tail_output.stdout)

        elif request == "dr":
                # connec to controller?
            capture_controls.pygame.init()
            capture_controls.pygame.joystick.init()
            gen = capture_controls.run({}, 1, False)

            while True:
                lspeed, rspeed, scalar, camleft, camright, button_x, button_y = next(gen)
                b_lspeed = struct.pack(">f", lspeed)
                b_rspeed = struct.pack(">f", rspeed)
                b_scalar = struct.pack(">f", scalar)
                b_camleft = struct.pack(">B", camleft)
                b_camright = struct.pack(">B", camright)
                b_button_x = struct.pack(">B", camright)
                b_button_y = struct.pack(">B", camright)
                payload = b_lspeed + b_rspeed + b_scalar + b_camleft + b_camright + b_button_x + b_button_y

                # pack up the message
                ctrls_msg = Message(new=True, purpose=1, payload=payload)
                print(ctrls_msg.get_as_bytes())

                ser.write(ctrls_msg.get_as_bytes())

        elif request == "test":
            while True:
                hello = input("enter tester phrase, exit to exit: ")
                if hello == "exit":
                    break
                msg = Message(purpose=0, payload=hello.encode())
                ser.write(msg.get_as_bytes())
        
        elif request == "hbt":
            msg = Message(purpose=2, payload=bytes(0))
            ser.write(msg.get_as_bytes())

        elif request == "ldp":
            msg = Message(purpose=3, payload=bytes(0))
            ser.write(msg.get_as_bytes())

        elif request == "hdp":
            msg = Message(purpose=4, payload=bytes(0))
            ser.write(msg.get_as_bytes())

        elif request == "menu":
            print_options()


#####################
##### FUNCTIONS #####
#####################

def print_options() -> None:
    print("----------------")
    print("MENU OF CONTROLS")
    print("----------------")
    print("(quit) to quit")
    print("(log) get most recent 10 msgs of the log")
    print("(ldp) for LD photo")
    print("(hdp) for HD photo")

    # following three may be merged together
    print("(dr) for driving")
    print("(arm) for arm control")
    print("(drl) operate the drill")

    print("(wrd) for sending word to arm to type out")
    print("(hbt) Heartbeat mode: Receive coordinates")
    print("(test) Send over tester strings for debugging purposes")
    print("(menu) See menu options again")

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

    current_video_feed_str = b''
    current_video_feed_num = 0

    current_hdp_str = b''
    current_hdp_num = 0

    while True:
        if len(messages_from_rover) == 0:
            continue
        curr_msg : Message = messages_from_rover.popleft()

        if curr_msg.purpose == 2: # indicates "HEARTBEAT / position"
            payload = curr_msg.get_payload()
            print(payload.decode())
            pass

        if curr_msg.purpose == 3: # indicates 'VIDEO FEED'
            if current_video_feed_num < curr_msg.number:
                current_video_feed_str += curr_msg.get_payload()
                current_video_feed_num += 1
            else:
                current_video_feed_num = 0
                save_and_output_image(current_video_feed_str, "vid_feed")
                current_video_feed_str = b''

        if curr_msg.purpose == 4: # indicates "HIGH DEFINITION PHOTO"
            if current_hdp_str < curr_msg.number:
                current_hdp_str += curr_msg.get_payload()
                current_hdp_num += 1
            else:
                current_hdp_num = 0
                save_and_output_image(current_hdp_str, "hdp")
                current_hdp_str = b''

        if curr_msg.purpose == 0: # indicates DEBUGGING
            payload = curr_msg.get_payload()
            print(payload.decode())

def save_and_output_image(buffer : bytearray, type : str) -> bool:
    try:
        image = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        cv2.imwrite(f"{type}/{datetime.now()}.jpg", frame)
        cv2.imshow(f'{type}', frame)
    #print("Image received and shown.")
        cv2.waitKey(1)
        return True
    except:
        return False

# everything to do on shutdown
def exit_main(executor : concurrent.futures.ThreadPoolExecutor):
    executor.shutdown()





if __name__ == "__main__":
    main()