import zmq
import cv2
import pickle

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:12345")

print("waiting on receiving info...")

while True:
    message = socket.recv()
    #frame = pickle.loads(message)
    #return_val = message
    frame = cv2.imdecode(message, 1)

    cv2.imshow('frame',frame)
    cv2.waitKey(5)

    try:
        pass
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        print("keyboard interruption")
        break
    #print(message)
    #socket.send_string("Got your message!")