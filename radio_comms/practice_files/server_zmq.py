import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:12345")

print("waiting on receiving info...")

while True:
    message = socket.recv()
    message = message.decode()
    print(message)
    socket.send_string("Got your message!")