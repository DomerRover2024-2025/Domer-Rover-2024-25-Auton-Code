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
VID_WIDTH = 200
# !TODO to be replaced by a message manager
messages_to_process = deque()
scheduler = Scheduler(ser=None, topics=None)

def main():
    #port = "/dev/cu.usbserial-BG00HO5R"
    port = "/dev/tty.usbserial-B001VC58"
    #port = "COM4"
    #port = "/dev/ttyTHS1"
    baud = 57600
    timeout = 0.1
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    topics = {
        "status": 3,
        "vid_feed": 10,
        "position": 1,
        "hdp": 1,
        "ldp": 1
    }

    scheduler.ser = ser
    scheduler.set_topics(topics=topics)

    executor = concurrent.futures.ThreadPoolExecutor(3)
    future_scheduler = executor.submit(scheduler.send_messages)
    future_msg_process = executor.submit(process_messages)
    print("entering while loop")
    while True:

        ##### READ: SERIAL PORT #####
        b_input = ser.read(1)
        if len(b_input) != 0:

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

            while len(payload) < potential_message.size_of_payload:
                payload += ser.read(potential_message.size_of_payload - len(payload))

            potential_message.set_payload(payload)
            potential_message.checksum = ser.read(1)

            # TODO replace with a message manager
            messages_to_process.append(potential_message)
            print(f"Message added: {potential_message.get_as_bytes()}")

        ##### READ: CAMERA #####
        should_capture_image = False
        if should_capture_image:
            _, buffer = capture_image(90, resize_width=VID_WIDTH)
            if buffer == None:
                continue
            scheduler.add_list_of_messages("vid_feed", Message.message_split(big_payload=buffer, purpose_for_all=2))

def capture_image(quality : int, resize_width : int=None) -> tuple[int, bytearray]:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        #print("Failed to capture image.")
        return 0, None

    # with open("temp2.txt", 'bw') as f:
    #     f.write(frame)

    if resize_width:
        resize_factor = resize_width / frame.shape[1]
        frame = cv2.resize(frame, (resize_width, int(resize_factor * frame.shape[0])))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    size_of_data = len(buffer)
    #size_packed = struct.pack(">L", size_of_data)
    return size_of_data, buffer

def process_messages() -> None:

    print("thread activated :)")

    # rclpy.init(args=None)
    # #create node
    # talkerNode = TalkerNode()

    # TODO: TODO TODO FIX THIS when connected to the jetson
    #arduino = serial.Serial('/dev/ttyACM0')

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
            lspeed = struct.unpack(">h", payload[0:2])[0]
            rspeed = struct.unpack(">h", payload[2:4])[0]
            speed_scalar = struct.unpack(">f", payload[4:8])[0]
            cam_left = struct.unpack(">B", payload[8:9])[0]
            cam_right = struct.unpack(">B", payload[9:10])[0]
            button_x = struct.unpack(">B", payload[10:11])[0]
            button_y = struct.unpack(">B", payload[11:12])[0]
            # TODO TODO TODO TODO FIX THIS WHEN CONNECTED TO THE JETSON
            #arduino.write(f"{lspeed} {rspeed}\n".encode())
        
        if curr_msg.purpose == 4: # indicates TAKE ME A GOOD PHOTO
            length, buffer = capture_image(90)
            if buffer == None:
                error_str = "Error: could not capture a high definition photo."
                scheduler.add_single_message(Message(purpose=0, payload=error_str.encode()))
            msgs =  Message.message_split(big_payload=buffer.tobytes(), purpose_for_all=4)
            scheduler.add_list_of_messages("hdp", msgs)
            print("Message added of length ", len(buffer.tobytes()))
        
        if curr_msg.purpose == 6: # indicates TAKE ME A BAD PHOTO
            length, buffer = capture_image(90, resize_width=VID_WIDTH)
            if buffer == None:
                error_str = "Error: could not capture a high definition photo."
                scheduler.add_single_message(Message(purpose=0, payload=error_str.encode()))
            
            msgs =  Message.message_split(big_payload=buffer.tobytes(), purpose_for_all=6)
            scheduler.add_list_of_messages("ldp", msgs)
            print("Message added of length ", len(buffer.tobytes()))

            #arduino_ser.write(msg.encode())
        if curr_msg.purpose == 0: # indicates DEBUGGING to the rover
            print("debugging message")
            payload = curr_msg.get_payload()
            print(payload.decode())

    talkerNode.destroy_node()
    rclpy.shutdown()
    arduino.close()

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String
# #be able to write to the arduino serial port
# #create an instance of the serial, open up a serial.write, and then write whatever the message being published is
# class TalkerNode(Node):
#     def __init__(self):
#         super().__init__("talker_node")
#         # TODO change the topic here from 'motor_state'
#         self.publisher_ = self.create_publisher(String, 'motor_state', 10)
#         timer_period = 0.1
#         #self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.count = 0
#         self.serialPort = serial.Serial('/dev/ttyACM0')
#     def listener_callback(self, msg):
#         #msg = String()
#         #msg.data = f"Hello everyone {self.count}"
#         # self.publisher_.publish(msg.data)
#         self.count += 1
#         self.get_logger().info(f"Recieving {msg.data}")
#         # self.write(msg.data)
#      #def write(x):
#         self.serialPort.write(msg.data.encode())


if __name__ == "__main__":
    main()
