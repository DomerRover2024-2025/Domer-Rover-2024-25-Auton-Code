import cv2
import zmq
import time

###### CONSTANTS ######
HOST = "*"
PORT = 12345
QUALITY = 80
TIME_BETWEEN_FRAMES = 0.05
CAM_PATH = '/dev/v4l/by-id/usb-046d_081b_32750F50-video-index0'
NUM_CAMS = 1
# create publish socket and video capture object
context = zmq.Context()
socket = context.socket(zmq.PUB)
caps = [cv2.VideoCapture(i) for i in range(0, NUM_CAMS)]


# bind the host and port
socket.bind(f"tcp://{HOST}:{PORT}")

while True:
    # capture frame; if successful encode it and publish it with quality QUALITY
    for i in range(0, NUM_CAMS):
        ret, frame = caps[i].read()
        if ret:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY]
            encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
            socket.send(f'{i}/'.encode() + buffer.tobytes())
        time.sleep(TIME_BETWEEN_FRAMES)
for cap in caps:
    ap.release()
cv2.destroyAllWindows()
socket.close()
