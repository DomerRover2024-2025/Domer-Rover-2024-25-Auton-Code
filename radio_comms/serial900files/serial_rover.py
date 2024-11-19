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

    # if nothing received, ask again
    if len(request == 0):
        continue

    request = struct.unpack("B", request)

    # quit the connection
    if request[0] == 0:
        print("Request to quit received.")
        exit_success = 1 # hardcode a success right now
        ser.write(struct.pack("B", exit_success))
        if exit_success == 1:
            break

    # ask for a photo
    elif request[0] == 1:
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
    
    # interactive mode
    elif request[0] == 2:
        # # do the control thing
        print("Receiving status update on controller...")
        while True:
            did_controller_connect = ser.read(1)
            if len(did_controller_connect):
                break
        did_controller_connect = struct.unpack("=B", did_controller_connect)[0]
        if did_controller_connect:
            print("Controller connected. Receiving inputs.")
            while True:
                current_output = ser.read(struct.calcsize("=B"))
                if not len(current_output):
                    continue
                print(struct.unpack("=B", current_output))
    awaiting_request = True
    request = b''           

ser.close()