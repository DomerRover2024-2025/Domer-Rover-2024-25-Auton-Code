# This is the server side of a client-server model.
# This will be receiving requests from the base station.

###################
##### IMPORTS #####
###################

import serial
import cv2
import sys
import struct
import numpy as np
import concurrent.futures
from message import Message
from scheduler import Scheduler
from collections import deque
from datetime import datetime
#np.set_printoptions(threshold=sys.maxsize)

MSG_LOG = "messages_rover.log"
# !TODO to be replaced by a message manager
messages_to_process = deque()

def main():
    #port = "/dev/cu.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM4"
    port = "/dev/ttyTHS1"
    baud = 57600
    timeout = 0.1
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    topics = {
        "status": 5,
        "image": 3,
        "position": 1
    }

    # temporary. to be replaced by a message handler class
    scheduler = Scheduler(ser=ser, topics=topics)

    executor = concurrent.futures.ThreadPoolExecutor(3)
    future_scheduler = executor.submit(scheduler.send_messages)
    future_msg_process = executor.submit(process_messages)
    print("entering while loop")
    while True:

        ##### READ: SERIAL PORT #####
        b_input = ser.read(1)
        if len(b_input) != 0:
            #print(b_input )
            potential_message = Message(new=False)
            b_input += ser.read(1)
            potential_message.set_msg_id(struct.unpack(">H", b_input)[0])
            b_input = ser.read(1)
            potential_message.set_purpose(b_input)
            b_input = ser.read(1)
            potential_message.number = struct.unpack(">B", b_input)[0]
            b_input = ser.read(struct.calcsize(">L"))
            potential_message.set_size(b_input)
            payload = b''
            # print(potential_message.size_of_payload)
            while len(payload) < potential_message.size_of_payload:
                payload += ser.read(potential_message.size_of_payload - len(payload))
            # print(len(payload))
            potential_message.set_payload(payload)
            potential_message.checksum = ser.read(1)
            
            # print(potential_message)
            print(potential_message.get_as_bytes())
            # print("Payload decoded: ", potential_message.get_payload().decode())
        

            # TODO replace with a message manager
            messages_to_process.append(potential_message)
            #print(f"Message added: {potential_message.get_as_bytes()}")

            #payload_ack = "msg received! :)"
            #msg_ack = Message(purpose=0, payload=payload_ack.encode())
            #scheduler.add_single_message("position", msg_ack)
    
        ##### READ: IMU? #####

        ##### READ: CAMERA? #####
        should_capture_image = False
        if should_capture_image:
            _, buffer = capture_image()
            scheduler.add_list_of_messages("image", Message.message_split(big_payload=buffer, purpose_for_all=2))

        ##### READ: ARM? #####

def save_and_output_image(buffer : bytearray, type : str) -> bool:
    try:
        image = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        cv2.imwrite(f"{type}/{datetime.now()}.jpg", frame)
        cv2.imshow(f'{type}', frame)
    #print("Image received and shown.")
        cv2.waitKey(1)
        return True
    except:
        return False

def capture_image() -> tuple[int, bytearray]:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        #print("Failed to capture image.")
        return 0, None

    # with open("temp2.txt", 'bw') as f:
    #     f.write(frame)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    size_of_data = len(buffer)
    #size_packed = struct.pack(">L", size_of_data)
    return size_of_data, buffer

def process_messages() -> None:

    port_arduino = "/dev/ttyACM0"
    #arduino_ser : serial.Serial = serial.Serial(port_arduino)
    print("thread activated :)")

    while True:
        if len(messages_to_process) == 0:
            continue
        print("Processing message", len(messages_to_process))
        curr_msg : Message = messages_to_process.popleft()
        Message.log_message(curr_msg, MSG_LOG)
        if curr_msg.purpose == 1: # indicates DRIVING
            print("driving message")
            payload = curr_msg.get_payload()
            print(len(payload))
            lspeed = struct.unpack(">f", payload[0:4])[0]
            rspeed = struct.unpack(">f", payload[4:8])[0]
            speed_scalar = struct.unpack(">f", payload[8:12])[0]
            cam_left = struct.unpack(">B", payload[12:13])[0]
            cam_right = struct.unpack(">B", payload[13:14])[0]
            button_x = struct.unpack(">B", payload[14:15])[0]
            button_y = struct.unpack(">B", payload[15:16])[0]

            print(f"{lspeed} {rspeed}")

            #arduino_ser.write(msg.encode())
        if curr_msg.purpose == 0: # indicates DEBUGGING
            print("debugging message")
            payload = curr_msg.get_payload()
            print(payload.decode())

    arduino_ser.close()



if __name__ == "__main__":
    main()
