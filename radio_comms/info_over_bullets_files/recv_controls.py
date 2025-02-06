import zmq
import struct

##### CONSTANTS ######
HOST = "localhost"
PORT = 12347

# create subscribe socket
context = zmq.Context()
socket = context.socket(zmq.SUB)

# connect to the video publish socket
socket.connect(f"tcp://{HOST}:{PORT}")
socket.subscribe("") # subscribe to everything

print("connection open")

while True:
    # receive the message (an encoded image)
    payload = socket.recv()
    if not payload:
        break
    lspeed = struct.unpack(">h", payload[0:2])[0]
    rspeed = struct.unpack(">h", payload[2:4])[0]
    speed_scalar = struct.unpack(">f", payload[4:8])[0]
    cam_left = struct.unpack(">B", payload[8:9])[0]
    cam_right = struct.unpack(">B", payload[9:10])[0]
    button_x = struct.unpack(">B", payload[10:11])[0]
    button_y = struct.unpack(">B", payload[11:12])[0]

    msg = f"{lspeed} {rspeed}\n"
    print(msg)

socket.close()