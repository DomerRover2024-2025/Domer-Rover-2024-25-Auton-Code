import serial
import cv2
import sys
import struct

#port = "/dev/cu.usbserial-BG00HO5R"
#port = "cu.usbserial-B001VC58"
port = "COM4"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

while True:
    request = ser.read(1)
    request = struct.unpack("B", request)

    if request == 'p':
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
        encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
        ser.write(buffer)

ser.close()