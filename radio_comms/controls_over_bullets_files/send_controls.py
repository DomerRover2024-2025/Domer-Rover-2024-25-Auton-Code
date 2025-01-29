import zmq
import time
import struct
import capture_controls

###### CONSTANTS ######
HOST = "*"
PORT = 12347

# create publish socket and video capture object
context = zmq.Context()
socket = context.socket(zmq.PUB)

capture_controls.pygame.init()
capture_controls.pygame.joystick.init()
gen = capture_controls.run({}, 1, False)

# bind the host and port
socket.bind(f"tcp://{HOST}:{PORT}")

while True:
    lspeed, rspeed, scalar, camleft, camright = next(gen)
    b_lspeed = struct.pack(">f", lspeed)
    b_rspeed = struct.pack(">f", rspeed)
    b_scalar = struct.pack(">f", scalar)
    b_camleft = struct.pack(">B", camleft)
    b_camright = struct.pack(">B", camright)
    payload = b_lspeed + b_rspeed + b_scalar + b_camleft + b_camright

    socket.send(payload)
    pass
socket.close()
