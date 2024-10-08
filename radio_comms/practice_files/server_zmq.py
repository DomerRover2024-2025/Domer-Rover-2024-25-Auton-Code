import zmq
import cv2
import pickle
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:12346")
#socket.setsockopt_string(zmq.SUBSCRIBE, unicode(''))
socket.subscribe("")
print("connection established")
#message = []
#index = 0
while True:
    #message.append(socket.recv())
    message = socket.recv()
    if not message:
        break
    #print("message received!")
    #print(message)
    image = np.frombuffer(message, dtype=np.uint8)
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