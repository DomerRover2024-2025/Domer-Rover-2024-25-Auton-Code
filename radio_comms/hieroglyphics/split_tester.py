#import serial
from message import Message
from functools import reduce

#ser = serial.Serial("/dev/tty.usbserial-B001VC58", baudrate=57600, timeout=0.1)

string = [0xef for i in range(9000)]

string = bytearray(string)

msg = Message(purpose=3, payload=string)
print(msg.payload[0] ^ msg.payload[1])
print(msg.payload)
print()
print(msg.checksum)
msg_list = msg.message_split(msg.payload,3)

current_msg = Message()

for list_msgs in msg_list:
    print()
    print(list_msgs.payload[0] ^ list_msgs.payload[1])
    print()
    print(list_msgs.payload)
    print()
    print(list_msgs.checksum)
