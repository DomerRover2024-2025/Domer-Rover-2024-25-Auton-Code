import serial
import numpy as np
import cv2
import time


port = "COM4"
baud = 57600
timeout = 10
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
# ser.timeout = 2
# ser.flushInput()
# ser.flushOutput()
#while(True):
    #time.sleep(1)
    #output = ser.readline()
    #print((output.decode("utf-8")))
MAXBYTES = 50_000
while (True):
    bytes = ser.in_waiting
    print(str(bytes))
    b_output = ser.read(MAXBYTES)

    if b_output == b'':
        image = np.frombuffer(b_output, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        cv2.imshow('frame', frame)
        cv2.waitKey(100)
    #print(b_output)





cv2.destroyAllWindows()