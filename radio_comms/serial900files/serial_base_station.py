import serial
import numpy as np
import cv2
import time
import struct

#port = "/dev/cu.usbserial-BG00HO5R"
port = "COM4"
baud = 57600
timeout = 15
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

MAXBYTES = 50_000
while (True):
    request = input("Type (1) for photo: ")
    request = int(request)
    ser.write(struct.pack("B", request))

    if request == 1:
        gotimage = False
        while not gotimage:
            b_output = ser.read(MAXBYTES)

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