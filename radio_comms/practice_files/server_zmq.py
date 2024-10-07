import zmq
import cv2
import pickle
import base64
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:12346")
#socket.setsockopt_string(zmq.SUBSCRIBE, unicode(''))

print("waiting on receiving info...")

while True:
    message = socket.recv()
    print("message received!")
    image = np.frombuffer(message, dtype=uint8)
    frame = cv2.imdecode(image, 1)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)


    # except KeyboardInterrupt:
    #     cv2.destroyAllWindows()
    #     print("\nkeyboard interruption\n")
    #     break
    #print(message)
    #socket.send_string("Got your message!")
cv2.destroyAllWindows()
socket.close()