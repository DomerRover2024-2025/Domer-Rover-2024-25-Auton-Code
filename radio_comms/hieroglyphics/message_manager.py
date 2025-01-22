from message import Message
from collections import deque
from datetime import datetime

class messageManager:
    def __init__(self, messages=deque()):
        self.messages : deque[Message] = deque(messages)
        self.log_name = "messages.log"
        self.curr_log_num = 0
        with open(self.log_name, 'w') as f:
            f.write("MSG_NO,METADATA,PYLD_SZ,TIME_RCVD")
    
    def add_message(self, message) -> None:
        if type(message) is not Message:
            raise TypeError("Type Error: Can only add a message of type Message")
        self.messages.append(message)
    
    def log_message(self, message : Message) -> None:
        # log the message
        with open(self.log_name, "a") as f:
            f.write(f"{self.curr_log_num},{message.opcode}:{message.destination},{message.size_of_payload},{datetime.now()}")

    # returns true if the checksum works out, false otherwise
    def check_is_valid_message(self, message : Message) -> None:
        checksum = message.calculate_checksum(message.get_as_bytes()[:-1])
        return checksum == message.checksum

    def read_and_process_next_message(self):
        if not self.messages:
            return
        curr_msg = self.messages.popleft()

        self.log_message(curr_msg)

        if not self.check_is_valid_message(curr_msg):
            pass

        # TODO
        if curr_msg.opcode == 0: # just print it out?
            print(curr_msg.payload.decode())
        elif curr_msg.opcode == 3: # driving?
            pass
    