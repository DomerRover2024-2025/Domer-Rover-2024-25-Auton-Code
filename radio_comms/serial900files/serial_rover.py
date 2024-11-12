# This is the server side of a client-server model.
# This will be receiving requests from the base station.

import serial
import cv2
import sys
import struct

#port = "/dev/cu.usbserial-BG00HO5R"
port = "/dev/cu.usbserial-B001VC58"
#port = "COM4"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

while True:
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
            size_of_buffer = sys.getsizeof(buffer)
            packed = struct.pack("L", size_of_buffer)
            ser.write(packed)
            ser.write(buffer)

ser.close()