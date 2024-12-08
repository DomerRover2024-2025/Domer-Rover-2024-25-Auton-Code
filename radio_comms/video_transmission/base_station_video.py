import zmq
import cv2
import numpy as np

##### CONSTANTS ######
HOST = "192.168.1.2"
PORT = 12346

# create subscribe socket
context = zmq.Context()
socket = context.socket(zmq.SUB)

# connect to the video publish socket
socket.connect(f"tcp://{HOST}:{PORT}")
socket.subscribe("") # subscribe to everything

print("connection established")

while True:
    # receive the message (an encoded image)
    message = socket.recv()
    if not message:
        break

    # decode the image and show it
    image = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(image, 1)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
socket.close()