# This is the client side of a client-server model.
# This will be sending requests to the rover.

import serial
import numpy as np
import cv2
import time
import struct
import sys

np.set_printoptions(threshold=sys.maxsize)

#port = "/dev/cu.usbserial-BG00HO5R"
port = "COM3"
baud = 57600
timeout = 5
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

MAXBYTES = 70_000
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
            size_of_image = ser.read(struct.calcsize("=L"))
            if len(size_of_image) == struct.calcsize("=L"):
                size_of_image = struct.unpack("=L", size_of_image)[0]
                print("size of image:", size_of_image)
                print("Size received. Sending acknowledgement.")
                ser.write(struct.pack("B", 1))
                break
        b_output = b''
        prev_len = -1
        time.sleep(1)
        while True:
            b_output += ser.read(4096)
            
            if len(b_output) < size_of_image:
            #    print(len(b_output))
                continue
            #print(len(b_output))
            image = np.frombuffer(b_output, dtype=np.uint8)
            with open("temp.txt", "w") as f:
                f.write(str(image))
            #print(image)
            frame = cv2.imdecode(image, 1)
            cv2.imwrite("tester.jpg", frame)
            cv2.imshow('frame', frame)
            print("Image received and shown.")
            cv2.waitKey(10)
            break
ser.close()
cv2.destroyAllWindows()