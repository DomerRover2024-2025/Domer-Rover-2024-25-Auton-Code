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
import atexit

#######################
##### GLOBAL VARS #####
#######################

messages_from_rover = deque()
MSG_LOG = "messages_base.log"
ERR_LOG = "errors_from_rover.log"
kill_threads = False

################
##### MAIN #####
################

def main():
    #port = "/dev/tty.usbserial-BG00HO5R"
    port = "/dev/cu.usbserial-B001VC58"
    #port = "COM3"
    baud = 57600
    timeout = 0.01
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    open(MSG_LOG, 'w').close()

    executor = concurrent.futures.ThreadPoolExecutor(3)
    future = executor.submit(process_messages)
    future = executor.submit(read_from_port, ser)
    atexit.register(exit_main, executor)

    # the main control
    while True:
        print_options()
        request = input(">> ")
        
        if request == 'quit':
            exit_main(executor=executor)
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
                b_lspeed = struct.pack(">h", lspeed)
                b_rspeed = struct.pack(">h", rspeed)
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
        
        elif request == "hdp":
            msg = Message(new=True, purpose=4, payload=bytes(1))
            ser.write(msg.get_as_bytes())
        
        elif request == "ldp":
            msg = Message(new=True, purpose=6, payload=bytes(1))
            ser.write(msg.get_as_bytes())

#####################
##### FUNCTIONS #####
#####################

##### READ FROM THE SERIAL PORT for incoming messages
def read_from_port(ser: serial.Serial):
    while not kill_threads:
        b_input = ser.read(1)
        if len(b_input) != 0:
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
            print(f"Message added {potential_message}; len = {len(messages_from_rover)}")

##### THE BRAINS FOR DECODING IMPORTED MESSAGES FROM ROVER
def process_messages() -> None:
    print("thread activated :)")

    current_video_feed_str = b''
    current_video_feed_num = 0

    current_hdp_str = b''
    current_hdp_num = 0

    while not kill_threads:
        if len(messages_from_rover) == 0:
            continue
        curr_msg : Message = messages_from_rover.popleft()
        if curr_msg.purpose == 0: # indicates ERROR
            error_msg = curr_msg.get_payload().decode()
            print(error_msg)
            with open(ERR_LOG,  'a') as f:
                f.write(error_msg + '\n')

        if curr_msg.purpose == 2: # indicates "HEARTBEAT / position"
            pass

        if curr_msg.purpose == 3: # indicates 'VIDEO FEED'
            if current_video_feed_num < curr_msg.number:
                current_video_feed_str += curr_msg.get_payload()
                current_video_feed_num += 1
            else:
                current_video_feed_num = 0
                current_video_feed_str += curr_msg.get_payload()
                try:
                    save_and_output_image(current_video_feed_str, "vid_feed")
                except Exception as e:
                    print(e)
                current_video_feed_str = b''

        if curr_msg.purpose == 4: # indicates "HIGH DEFINITION PHOTO"
            if current_hdp_num < curr_msg.number:
                current_hdp_str += curr_msg.get_payload()
                current_hdp_num += 1
            else:
                current_hdp_num = 0
                current_hdp_str += curr_msg.get_payload()
                try:
                    save_and_output_image(current_hdp_str, "hdp")
                except Exception as e:
                    print(e)
                current_hdp_str = b''

        if curr_msg.purpose == 0: # indicates DEBUGGING
            payload = curr_msg.get_payload()
            print(payload.decode())

def save_and_output_image(buffer : bytearray, type : str) -> bool:
    try:
        #buffer = buffer.frombytes()
        image = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        if not os.path.isdir(f"{type}"):
            os.mkdir(f"{type}")
        cv2.imwrite(f"{type}/{time.time()}.jpg", frame)
        cv2.imshow(f'{type}', frame)
        cv2.waitKey(1)
        return True
    except Exception as e:
        print(e)
        return False

# everything to do on shutdown
def exit_main(executor : concurrent.futures.ThreadPoolExecutor):
    kill_threads = True
    executor.shutdown()

def print_options() -> None:
    print("----------------")
    print("MENU OF CONTROLS")
    print("----------------")
    print("(quit) to quit THIS SIDE ONLY")
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
    print("(literally anything else) See menu options again")


if __name__ == "__main__":
    main()