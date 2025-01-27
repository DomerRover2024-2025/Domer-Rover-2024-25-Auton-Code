from functools import reduce
import serial
import struct
import sys

### MESSAGE STRUCTURE:
    # UID: 2 BYTES?
    # PURPOSE: 1 BYTE?
    # SIZE OF PAYLOAD: 4 BYTES?
    # PAYLOAD: VARIABLE BYTES?
    # CHECKSUM: 1 BIT
class Message:

    message_count = 0

    # I am necessitating that the payload ALREADY BE a byte object.
    # I do not know how big it is.
    def __init__(self, new=True, purpose: int=0, payload : bytes=None):
        if new:
            self.msg_id : int = self.message_count
            self.message_count += 1
        else:
            self.msg_id : int = -1
        self.purpose : int = purpose
        self.number : int = 0
        self.payload : bytes = payload
        if payload:
            self.size_of_payload : int = len(payload)
            self.checksum : bytes = self.calculate_checksum(payload)

    # converting a given bytestring into its corresponding Message counterpart
    def convert_from_bytestring(self, bytestring : bytes):
        self.msg_id = struct.unpack(">H", bytestring[0:2])[0]
        self.purpose = struct.unpack(">B", bytestring[2])[0]
        self.number = struct.unpack(">B", bytestring[3])[0]
        self.size_of_payload = struct.unpack(">L", bytestring[4:8])[0]
        self.payload = bytestring[8:-1]
        self.checksum = bytestring[-1]

    def set_msg_id(self, id):
        if type(id) is bytes:
            self.msg_id = struct.unpack(">H", id)[0]
        else:
            self.msg_id = id

    def calculate_checksum(self, payload: str):
        return bytes(reduce(lambda a,b: a ^ b, payload))
    
    def get_payload(self):
        return self.payload

    def get_as_bytes(self):
        # if not self:
            # return None
        b_id = struct.pack(">H", self.msg_id)
        b_purpose = struct.pack(">B", self.purpose)
        b_number = struct.pack(">B", self.number)
        b_size = struct.pack(">L", self.size_of_payload)
        return b_id + b_purpose + b_number + b_size + self.payload + self.checksum

    def get_total_size(self):
        return struct.calcsize(self.purpose)
    
    def set_purpose(self, purpose):
        if type(purpose) is bytes:
            self.purpose = struct.unpack(">B", purpose)[0]
        else:
            self.purpose = purpose

    def set_payload(self, payload):
        self.payload = payload
        self.size_of_payload = len(payload)
    
    def set_size(self, size):
        if type(size) is not bytes:
            print("potential size isn't bytes! Whatchu trying to do here.", file=sys.stderr)
            return
        self.size_of_payload = struct.unpack(">L", size)[0]

    def __bool__(self):
        return self.purpose and self.payload
    
    def __str__(self):
        string = f"ID:{self.msg_id}:purpose,{self.purpose}:destination,<empty_atm>:size,{self.size_of_payload}"
        if not self:
            return f"Invalid:{string}"
        return string