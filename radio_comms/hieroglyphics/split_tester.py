import serial
from message import Message
from functools import reduce

ser = serial.Serial("/dev/tty.usbserial-B001VC58", baudrate=57600, timeout=0.1)

string = ['h' for i in range(60000)]

msg = Message(purpose=3, payload=string.encode())
print(msg.payload[0] ^ msg.payload[1])
print(bytes(reduce(lambda a,b: a ^ b, msg.payload)))
print(msg.checksum)
msg_list = msg.message_split(msg.get_as_bytes())

current_msg = Message()

for list_msgs in msg_list:
    current_msg = current_msg.convert_from_bytestring(current_msg, list_msgs)
    print(current_msg.payload[0] ^ current_msg.payload[1])
