import cv2
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

print("Looking for server...")

socket.connect("tcp://localhost:12345")

while True:
    message = input("--Enter message: ")
    print("Sending request {0}".format(message))
    socket.send(message.encode())

    received_message = socket.recv()
    print("Received {0} from server".format(received_message))
