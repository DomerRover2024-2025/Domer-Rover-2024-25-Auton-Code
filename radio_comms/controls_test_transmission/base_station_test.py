import zmq

HOST = '*'
PORT = 5555

context = zmq.Context()
socket = context.socket(zmq.PUB)

socket.bind(f"tcp://{HOST}:{PORT}")

while True:
    message = input("Enter message: ")
    if(message == "quit"):
        break
    #numbers = int(message)
    socket.send_string(message)

socket.close()