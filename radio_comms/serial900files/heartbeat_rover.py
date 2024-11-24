import serial
import time
import struct

port = "COM4"
baud = 57600
timeout = 2
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

try:
    while True:
        ser.write(b"Heartbeat\r\n")
        output = ser.readline()
        print(output)
        #time.sleep(2)
except KeyboardInterrupt:
    ser.close()
