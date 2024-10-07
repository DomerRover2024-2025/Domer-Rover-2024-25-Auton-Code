import cv2
import zmq
import pickle

context = zmq.Context()
socket = context.socket(zmq.PUB)

cap = cv2.VideoCapture(0)

print("Looking for server...")

socket.connect("tcp://localhost:12345")

print("connected to server!")

while True:
    try:
        ret, frame = cap.read()
        #data = pickle.dumps(frame)
        #print("Sending request {0}".format(message))
        encoded, buffer = cv2.imencode('.jpg', frame)
        socket.send(buffer)
        #received_message = socket.recv()
        #received_message = received_message.decode()
        #print("Received {0} from server".format(received_message))
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print("keyboard interruption")
        break
