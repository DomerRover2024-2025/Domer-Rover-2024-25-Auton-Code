import cv2
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)

cap = cv2.VideoCapture(0)

HOST = "*"
PORT = 12346
QUALITY = 50

print("Looking for server...")

socket.bind(f"tcp://{HOST}:{PORT}")
print("waiting to send info")

#socket.send(b"WHY WONT YOU WORK")

while True:
    ret, frame = cap.read()
    #data = pickle.dumps(frame)
    #print("Sending request {0}".format(message))
    if ret:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY]
        encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    #message = buffer.tobytes()
        socket.send(buffer)
    #time.sleep(1)
cap.release()
cv2.destroyAllWindows()
socket.close()
