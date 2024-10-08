import cv2
import zmq
import pickle
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)

cap = cv2.VideoCapture(0)

print("Looking for server...")

socket.bind("tcp://127.0.0.1:12346")
print("waiting to send info")

#socket.send(b"WHY WONT YOU WORK")

while True:
    ret, frame = cap.read()
    #data = pickle.dumps(frame)
    #print("Sending request {0}".format(message))
    if ret:
        #encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        encoded, buffer = cv2.imencode('.jpg', frame)
    #message = buffer.tobytes()
        socket.send(buffer)
    time.sleep(1)
    #cv2.imshow('frame', frame)
    #cv2.waitKey(1)
    #received_message = socket.recv()
    #received_message = clereceived_message.decode()
    #print("Received {0} from server".format(received_message))
    # except KeyboardInterrupt:
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     socket.close()
    #     print("\nkeyboard interruption\n")
    # #break
cap.release()
cv2.destroyAllWindows()
socket.close()
