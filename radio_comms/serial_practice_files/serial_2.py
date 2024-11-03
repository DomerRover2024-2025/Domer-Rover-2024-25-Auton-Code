import serial
import time

port = "COM3"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
# ser.flushInput()
# ser.flushOutput()
while(True):
    time.sleep(1)
    output = ser.readline()
    print((output))
