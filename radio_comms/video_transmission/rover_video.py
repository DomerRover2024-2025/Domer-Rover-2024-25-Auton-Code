import cv2
import zmq
import time

###### CONSTANTS ######
HOST = "*"
PORT = 12346
QUALITY = 75
TIME_BETWEEN_FRAMES = 0.05

# create publish socket and video capture object
context = zmq.Context()
socket = context.socket(zmq.PUB)
cap = cv2.VideoCapture(0)

# bind the host and port
socket.bind(f"tcp://{HOST}:{PORT}")

while True:
    # capture frame; if successful encode it and publish it with quality QUALITY
    ret, frame = cap.read()
    if ret:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY]
        encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
        socket.send(buffer)
    time.sleep(TIME_BETWEEN_FRAMES)
cap.release()
cv2.destroyAllWindows()
socket.close()
