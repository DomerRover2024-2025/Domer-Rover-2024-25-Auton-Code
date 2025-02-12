from message import Message
from collections import deque
from datetime import datetime

class MessageManager:
    def __init__(self, messages=deque()):
        # below line: a typehint, #comment, for a deque of Message objects
        self.messages : deque[Message] = deque(messages)
        self.log_name = "messages.log"
        with open(self.log_name, 'w') as f:
            f.write("MSG_NO,METADATA,PYLD_SZ,TIME_RCVD")
    
    def add_message(self, message) -> None:
        if type(message) is not Message:
            raise TypeError("Type Error: Can only add a message of type Message")
        self.messages.append(message)
    
    def log_message(self, message : Message) -> None:
        # log the message
        with open(self.log_name, "a") as f:
            f.write(f"ID,{message.msg_id}:purpose,{message.purpose}:number,{message.number}:size,{message.size_of_payload}:time,{datetime.now()}")

    # returns true if the checksum works out, false otherwise
    def check_is_valid_message(self, message : Message) -> None:
        checksum = message.calculate_checksum(message.get_as_bytes()[:-1])
        return checksum == message.checksum

    def read_next_message(self):
        if not self.messages:
            return
        curr_msg = self.messages.popleft()

        self.log_message(curr_msg)

        if not self.check_is_valid_message(curr_msg):
            pass
        
        self.process_next_message(curr_msg)

    def process_next_message(self):
        pass