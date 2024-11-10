import serial
import time
import struct

port = "COM4"
baud = 57600
timeout = 2
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
#ser.write(b"Heartbeat\r\n")
input = struct.pack("B", 45)
ser.write(input)
#time.sleep(2)
ser.close()