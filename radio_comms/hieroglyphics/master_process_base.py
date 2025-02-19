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
    #port = "/dev/cu.usbserial-BG00HO5R"
    port = "/dev/cu.usbserial-B001VC58"
    #port = "COM3"
    baud = 57600
    timeout = 0.1
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # make sure the log file is empty
    open(MSG_LOG, 'w').close()

    # 3 concurrent threads: one read from serial port, 
    # one for processing messages, one for writing messages
    executor = concurrent.futures.ThreadPoolExecutor(3)
    future = executor.submit(process_messages)
    future = executor.submit(read_from_port, ser)
    atexit.register(exit_main, executor)

    try:
            
        # the main control
        while True:
            # Continuously display options and ask for user input
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
                # get joystick
                gen = capture_controls.run({}, 1, False)

                while True:
                    lspeed, rspeed, scalar, camleft, camright, button_x, button_y = next(gen) # get joystick values
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

            # Send test messages
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
    except KeyboardInterrupt or Exception:
        exit(0)

#####################
##### FUNCTIONS #####
#####################

##### READ FROM THE SERIAL PORT for incoming messages
def read_from_port(ser: serial.Serial):
    while not kill_threads:

        try:
            b_id = read_num_bytes(ser, 1)
            # ID, PURPOSE, NUMBER, SIZE, PAYLOAD, CHECKSUM
            if len(b_id) == 0:
                continue
            #print("Got a message")
            pot_msg = Message(new=False)
            b_id += read_num_bytes(ser, 1)
            pot_msg.set_msg_id(struct.unpack(">H", b_id)[0])
            #print("Got id")
            b_purpose = read_num_bytes(ser, 1)
            pot_msg.set_purpose(struct.unpack(">B", b_purpose)[0])
            #print("Got purpose")
            b_number = read_num_bytes(ser, 1)
            pot_msg.number = struct.unpack(">B", b_number)[0]
            #print("Got number")
            b_size = read_num_bytes(ser, struct.calcsize(">L"))
            #print(struct.calcsize(">L"))
            pot_msg.set_size(b_size)
            print(f"{b_id}{b_purpose}{b_number}{b_size}")
            print("Got size", pot_msg.size_of_payload)

            # print(pot_msg.size_of_payload)
            payload = read_num_bytes(ser, pot_msg.size_of_payload)
            # print(len(payload))
            pot_msg.set_payload(payload)
            #print("Got payload")
            checksum = read_num_bytes(ser, 1)
            #print("Got checksum")

            #print(checksum)
            if not Message.test_checksum(bytestring=pot_msg.get_as_bytes()[:-1], checksum=checksum):
                print("Checksum error")
                continue
            messages_from_rover.append(pot_msg)
            print(f"Message added {pot_msg}; len = {len(messages_from_rover)}")
        except Exception as e:
            print(e)

##### THE BRAINS FOR DECODING IMPORTED MESSAGES FROM ROVER
def process_messages() -> None:
    print("thread activated :)")

    vid_feed_str = b''
    vid_feed_num = 0
    vid_feed_dict = {}

    hdp_str = b''
    hdp_num = 0
    hdp_dict = {}

    ldp_str = b''
    ldp_num = 0
    ldp_dict = {}

    # Continuously check for messages, process them according to their purpose.
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

        # if curr_msg.purpose == 3: # indicates 'VIDEO FEED'
        #     # curr_msg.number: number of 'packets' needed to reconstruct the image
        #     if curr_msg.number != 0:
        #         video_feed_dict[curr_msg.number] = curr_msg.get_payload()

        #     else:
        #         for i in range(1, len(video_feed_dict) + 1):
        #             if i not in video_feed_dict:
        #                 video_feed_dict = {}
        #                 video_feed_str = b''
        #                 print("some error occurred in getting the video feed")
        #             video_feed_str += video_feed_dict[i]

        #         video_feed_str += curr_msg.get_payload()
        #         try:
        #             save_and_output_image(video_feed_str, "vid_feed")
        #         except Exception as e:
        #             print(e)

        #         video_feed_dict = {}
        #         video_feed_str = b''

        # if curr_msg.purpose == 4: # indicates 'VIDEO FEED'
        #     # curr_msg.number: number of 'packets' needed to reconstruct the image
        #     if curr_msg.number != 0:
        #         hdp_dict[curr_msg.number] = curr_msg.get_payload()

        #     else:
        #         for i in range(1, len(hdp_dict) + 1):
        #             if i not in video_feed_dict:
        #                 hdp_dict = {}
        #                 hdp_str = b''
        #                 print("some error occurred in getting the high definition photo")
        #             hdp_str += hdp_dict[i]
                    
        #         hdp_str += curr_msg.get_payload()
        #         try:
        #             save_and_output_image(video_feed_str, "vid_feed")
        #         except Exception as e:
        #             print(e)

                # video_feed_dict = {}
                # video_feed_str = b''
        
        if curr_msg.purpose == 3: # indicates "VIDEO FEED"
            if vid_feed_num < curr_msg.number:
                print("found msg")
                vid_feed_str += curr_msg.get_payload()
                vid_feed_num += 1
            else:
                print("went here instead")
                vid_feed_num = 0
                vid_feed_str += curr_msg.get_payload()
                try:
                    save_and_output_image(vid_feed_str, "vid_feed")
                except Exception as e:
                    print(e)
                hdp_str = b''
        
        if curr_msg.purpose == 4: # indicates "HIGH DEFINITION PHOTO"
            if hdp_num < curr_msg.number:
                print("found msg")
                hdp_str += curr_msg.get_payload()
                hdp_num += 1
            else:
                print("went here instead")
                hdp_num = 0
                hdp_str += curr_msg.get_payload()
                try:
                    save_and_output_image(hdp_str, "hdp")
                except Exception as e:
                    print(e)
                hdp_str = b''
        
        if curr_msg.purpose == 6: # indicates "LOW DEFINITION PHOTO"
            if ldp_num < curr_msg.number:
                print("found msg")
                ldp_str += curr_msg.get_payload()
                ldp_num += 1
            else:
                print("went here instead")
                ldp_num = 0
                ldp_str += curr_msg.get_payload()
                try:
                    save_and_output_image(ldp_str, "ldp")
                except Exception as e:
                    print(e)
                hdp_str = b''
    

def save_and_output_image(buffer : bytearray, type : str) -> bool:
    try:
        #buffer = buffer.frombytes()
        # Convert the byte array to an integer numpy array 
        # (decoded image with ".imdecode", written to a file (".imwrite")
        # and displayed (".imshow"))
        image = np.frombuffer(buffer, dtype=np.uint8)
        print("unbuffered image, len", len(buffer))
        frame = cv2.imdecode(image, 1)
        print("decoded image")
        if not os.path.isdir(f"{type}"):
            os.mkdir(f"{type}")
        print("made directory")
        cv2.imwrite(f"{type}/{time.time()}.jpg", frame)
        print("saved image")
        cv2.imshow(f'{type}', frame)
        print('showed image')
        cv2.waitKey(1)
        return True
    except Exception as e:
        print(e)
        return False

# everything to do on shutdown
def exit_main(executor : concurrent.futures.ThreadPoolExecutor):
    global kill_threads
    kill_threads = True
    executor.shutdown(wait=False, cancel_futures=True)

def read_num_bytes(ser: serial.Serial, numbytes : int):
    read_bytes = b''
    while len(read_bytes) < numbytes:
        if kill_threads:
            return
        read_bytes += ser.read(numbytes - len(read_bytes))

    return read_bytes

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