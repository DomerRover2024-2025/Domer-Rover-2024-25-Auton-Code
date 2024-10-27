import zmq

HOST = 'localhost'
PORT = 5555

CONN_STR = f"tcp://{HOST}:{PORT}"
#"///dev/tty.usbserial-BG00HO5R"
#CONN_STR = 'tcp://localhost:12345'

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect(CONN_STR)
socket.subscribe("")

while True:
    message = socket.recv_string()
    print(message)
