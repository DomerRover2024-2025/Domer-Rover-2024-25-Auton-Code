import serial
import time
import struct

port = "COM4"
baud = 57600
timeout = 2
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
<<<<<<< HEAD
#ser.write(b"Heartbeat\r\n")
input = struct.pack("B", 45)
ser.write(input)
#time.sleep(2)
ser.close()
=======
ser.write(b"Heartbeat\r\n")
time.sleep(2)
try:
    while True:
        pass
except KeyboardInterrupt:
    ser.close()
>>>>>>> 68c4015 (radio_comms -- working on serial connection)
