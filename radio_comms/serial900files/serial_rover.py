import serial
import cv2
import sys

port = "/dev/cu.usbserial-BG00HO5R"
#port = "cu.usbserial-B001VC58"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
print(sys.getsizeof(buffer))
#print(sys.getsizeof(int(sys.getsizeof(buffer))))
#ser.write(sys.getsizeof(buffer))#

ser.write(buffer)
#ser.write(b'hadkfakdf\n')

print(ser.in_waiting)
print(ser.out_waiting)

ser.close()