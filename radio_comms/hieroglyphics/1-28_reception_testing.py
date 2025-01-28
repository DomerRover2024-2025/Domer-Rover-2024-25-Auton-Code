import serial
import struct
from message import Message

ser = serial.Serial('COM4', baudrate=57600, timeout=0.1)

while True:
    ##### READ: SERIAL PORT #####
    b_input = ser.read(1)
    if len(b_input) != 0:
        print(b_input)
        potential_message = Message(new=False)
        b_input += ser.read(1)
        potential_message.set_msg_id(struct.unpack(">H", b_input)[0])
        b_input = ser.read(1)
        potential_message.set_purpose(b_input)
        b_input = ser.read(1)
        potential_message.number = struct.unpack(">B", b_input)[0]
        b_input = ser.read(struct.calcsize(">L"))
        potential_message.set_size(b_input)
        payload = b''
        print(potential_message.size_of_payload)
        while len(payload) < potential_message.size_of_payload:
            payload += ser.read(potential_message.size_of_payload - len(payload))
        print(len(payload))
        potential_message.set_payload(payload)
        potential_message.checksum = ser.read(1)
        
        print(potential_message)
        print(potential_message.get_as_bytes())
        print("Payload decoded: ", potential_message.get_payload().decode())