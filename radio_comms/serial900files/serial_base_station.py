# This is the client side of a client-server model.
# This will be sending requests to the rover.

import serial
import numpy as np
import cv2
import time
import struct

#port = "/dev/cu.usbserial-BG00HO5R"
port = "COM3"
baud = 57600
timeout = 15
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

MAXBYTES = 50_000
while (True):
    request = input("Type (1) for photo: ")
    request = int(request)
    ser.write(struct.pack("B", request))

    if request == 0: # end connection
        print("Request to quit sent.")

        ack = struct.unpack("B", ser.read(1))
        if ack[0] == 1: # successful connection break
            print("Request successful.")
            break
        else:
            print("Request unsucessful.")

    if request == 1: # photo
        gotimage = False
        while True:
            size_of_image = ser.read(4)
            if size_of_image != b'':
                size_of_image = struct.unpack("L", size_of_image)[0]
                break
        while not gotimage:
            b_output = ser.read(size_of_image)

            if b_output != b'':
                print("received image")
                image = np.frombuffer(b_output, dtype=np.uint8)
                frame = cv2.imdecode(image, 1)
                cv2.imshow('frame', frame)
                cv2.waitKey(100)
                gotimage = True
            else:
                print("No photo received. Receiving...")

ser.close()





cv2.destroyAllWindows()