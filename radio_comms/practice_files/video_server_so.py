import pickle
import socket
import struct
import numpy as np
import cv2

HOST = socket.gethostname()#'10.7.186.29'#socket.gethostname()
PORT = 50011

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
print(f'Connection at {addr} accepted')
data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED
#data_list = []
while True:

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED
    #print(msg_size)
    print(msg_size)
    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    #print("got image")

    frame_data = data[:msg_size]
    data = data[msg_size:]
    # frame_data = np.fromstring(frame_data)
    # frame = cv2.imdecode(frame_data, cv2.IMREAD_UNCHANGED)

    # Extract frame
    frame = pickle.loads(frame_data)

    # Display
    cv2.imshow('frame', frame)
    cv2.waitKey(5)