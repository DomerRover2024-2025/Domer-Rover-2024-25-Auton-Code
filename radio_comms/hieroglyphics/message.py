from functools import reduce
import serial
import struct
import sys

### MESSAGE STRUCTURE:
    # OPCODE: 1 BYTE?
    # DESTINATION: 1 BYTE?
    # SIZE OF PAYLOAD: 4 BYTES?
    # PAYLOAD: VARIABLE BYTES?
    # CHECKSUM: 1 BIT
class Message:

    # I am necessitating that the payload ALREADY BE a byte object.
    # I do not know how big it is.
    def __init__(self, opcode: int=None, destination: int=None, payload : bytes=None):
        self.opcode : int = opcode
        self.destination : int = destination
        self.payload : bytes = payload
        if payload:
            self.size_of_payload : int = len(payload)
            self.checksum : bytes = self.calculate_checksum(payload)

    # converting a given bytestring into its corresponding Message counterpart
    def convert_from_bytestring(self, bytestring : bytes):
        self.opcode = struct.unpack(">B", bytestring[0])[0]
        self.destination = struct.unpack(">B", bytestring[2])[0]
        self.size_of_payload = struct.unpack(">L", bytestring[3:7])[0]
        self.payload = bytestring[7:-1]
        self.checksum = bytestring[-1]

    def calculate_checksum(self, payload: str):
        return bytes(reduce(lambda a,b: a ^ b, payload))
    
    def get_payload(self):
        return self.payload

    def get_as_bytes(self):
        if not self:
            return None
        b_opcode = struct.pack(">B", self.opcode)
        b_destination = struct.pack(">B", self.destination)
        b_size = struct.pack(">L", self.size_of_payload)
        return b_opcode + b_destination + b_size + self.payload + self.checksum

    def get_total_size(self):
        return struct.calcsize(self.opcode)
    
    def set_opcode(self, opcode):
        if type(opcode) is bytes:
            self.opcode = struct.unpack(">B", opcode)[0]
        else:
            self.opcode = opcode

    def set_destination(self, destination):
        if type(destination) is bytes:
            self.destination = struct.unpack(">B", destination)[0]
        else:
            self.destination = destination

    def set_payload(self, payload):
        self.payload = payload
        self.size_of_payload = len(payload)
    
    def set_size(self, size):
        if type(size) is not bytes:
            print("potential size isn't bytes! Whatchu trying to do here.", file=sys.stderr)
            return
        self.size_of_payload = struct.unpack(">L", size)[0]

    def __bool__(self):
        return self.opcode and self.destination and self.payload
    
    def __str__(self):
        string = f"opcode,{Message.opcodes[self.opcode]}:destination,<empty_atm>:size,{self.size_of_payload}"
        if not self:
            return f"Invalid:{string}"
        return string