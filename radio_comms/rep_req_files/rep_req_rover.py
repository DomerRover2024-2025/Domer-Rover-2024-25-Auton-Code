import zmq

HOST = 'localhost'
PORT = 5555

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect(f"tcp://{HOST}:{PORT}")
socket.subscribe("")

while True:
    message = socket.recv_string()
    print(message)
