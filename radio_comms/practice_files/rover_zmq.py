import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)

HOST = "*"
PORT = 12346

socket.connect(f"tcp://{HOST}:{PORT}")
socket.subscribe("")

print("connection established")

while True:

    message = socket.recv()
    if not message:
        break

    image = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(image, 1)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
socket.close()