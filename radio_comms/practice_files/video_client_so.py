import cv2
import numpy as np
import socket
import sys
import pickle
import struct

HOST = "10.7.90.102"
#HOST = socket.gethostname()
PORT = 50011
print(f"looking for {HOST}")
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((HOST, PORT))

while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)
    #data = cv2.imencode('.jpg', frame)[1]
    #data_array = np.array(data)
    #data = data_array.tobytes()
    # Send message length first
    message_size = struct.pack("L", len(data)) ### CHANGED

    # Then data
    clientsocket.sendall(message_size + data)