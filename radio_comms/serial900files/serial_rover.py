# This is the server side of a client-server model.
# This will be receiving requests from the base station.

import serial
import cv2
import sys
import struct
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

#port = "/dev/cu.usbserial-BG00HO5R"
port = "/dev/cu.usbserial-B001VC58"
#port = "COM4"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

awaiting_request = True

while True:
    if awaiting_request:
        print("Awaiting request.")
        awaiting_request = False
    request = ser.read(1)
    if request != b'':
        request = struct.unpack("B", request)

        if request[0] == 0: # quit
            print("Request to quit received.")
            exit_success = 1 # hardcode a success right now
            ser.write(struct.pack("B", exit_success))
            if exit_success == 1:
                break

        if request[0] == 1: # photo
            print("Request for image received.")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
            encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
            size_of_data = len(buffer)
            size_packed = struct.pack("=L", size_of_data)

            print(size_of_data, sys.getsizeof(buffer))
            print("Size of image calculating. Sending.")
            ser.write(size_packed)

            while True:
                b_output = ser.read(1)
                if b_output != b'':
                    if struct.unpack("B", b_output)[0] == 1:
                        print("Size was acknowledged.")
                        break
            print("Image sending.")
            with open("temp.txt", "w") as f:
                f.write(str(buffer))
            ser.write(buffer)
        
        awaiting_request = True
        request = b''

ser.close()