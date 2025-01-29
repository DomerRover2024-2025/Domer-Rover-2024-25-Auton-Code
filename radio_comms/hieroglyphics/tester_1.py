import serial
import struct
from message import Message
from functools import reduce

ser = serial.Serial("/dev/tty.usbserial-B001VC58", baudrate=57600, timeout=0.1)

string = "please work"

msg = Message(purpose=0, payload=string.encode())
print(msg.checksum)

while True:
    if input(">>") == "go":
        print(msg)
        print(msg.get_as_bytes())
        ser.write(msg.get_as_bytes())