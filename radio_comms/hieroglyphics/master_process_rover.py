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
from scheduler import Scheduler
np.set_printoptions(threshold=sys.maxsize)

def main():
    #port = "/dev/cu.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM4"
    port = "/dev/ttyTHS1"
    baud = 57600
    timeout = 0.001
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # set of output topics
    topics = {
        "status" : 7,
        "camera" : 5,
        "heartbeat" : 1
    }

    dst_str_to_int = {
        "status" : 0,
        "camera" : 1,
        "motors?" : 2
    }

    dst_int_to_str = {
        0 : "status",
        1 : "camera",
        2 : "motors?"
    }

    # temporary. to be replaced by a message handler class
    scheduler = Scheduler(ser=ser, topics=topics)

    # !TODO to be replaced by a message manager
    messages = []

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

            # TODO replace with a message manager
            messages.append(potential_message)

    
        ##### READ: IMU? #####

        ##### READ: CAMERA? #####
        should_capture_image = True
        if should_capture_image:
            _, buffer = capture_image()
            image_msg = Message(destination=dst_str_to_int["camera"], payload=buffer)
            scheduler.sort_message(image_msg, dst_int_to_str)

        ##### READ: ARM? #####

def capture_image() -> tuple[int, bytearray]:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        #print("Failed to capture image.")
        return 0, None

    # with open("temp2.txt", 'bw') as f:
    #     f.write(frame)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    size_of_data = len(buffer)
    #size_packed = struct.pack(">L", size_of_data)
    return size_of_data, buffer

if __name__ == "__main__":
    main()