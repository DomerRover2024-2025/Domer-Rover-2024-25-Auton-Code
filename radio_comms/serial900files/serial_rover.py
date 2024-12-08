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
import time
np.set_printoptions(threshold=sys.maxsize)

#####################
##### FUNCTIONS #####
#####################

# function to capture image
# returns its size and the bytearray representing the image
def capture_image() -> tuple[int, bytearray]:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        #print("Failed to capture image.")
        return 0, None

    with open("temp2.txt", 'bw') as f:
        f.write(frame)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
    encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    size_of_data = len(buffer)
    #size_packed = struct.pack(">L", size_of_data)
    return size_of_data, buffer


# function to keep sending images through the thread executor
keep_sending_images = True
def send_images(ser: serial.Serial) -> None:
    while keep_sending_images:
        size_of_image, buffer = capture_image()

        packed_size = struct.pack(">L", size_of_image)
        ser.write(packed_size)
        if size_of_image == 0:
            return
        ser.write(buffer)
        time.sleep(1)
        
################
##### MAIN #####
################

if __name__ == "__main__":
    #port = "/dev/cu.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM4"
    port = "ttyTCU0"
    baud = 57600
    timeout = 3
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    awaiting_request = True

    # the main control
    while True:
        if awaiting_request:
            print("Awaiting request.")
            awaiting_request = False
        # continue reading for a byte which determines current control
        request = ser.read(1)

        # if nothing received, ask again
        if len(request) == 0:
            continue

        # unpack to see what the original number was
        request = struct.unpack(">B", request)

        ###### end connection ######
        if request[0] == 0:
            print("Request to quit received.")
            exit_success = 1 # hardcode a success right now
            ser.write(struct.pack(">B", exit_success))
            if exit_success == 1:
                break

        ##### ask for a photo #####
        elif request[0] == 1:
            print("Request for image received.")
            
            # take photo and get size
            size_of_image, buffer = capture_image()

            with open("temp1.txt", 'bw') as f:
                f.write(buffer)

            # if the size is 0, the image failed
            if size_of_image == 0:
                print("Image capture failed.")
                ser.write(struct.pack(">L", size_of_image))
                continue

            print(f"Size of image calculated as {size_of_image}. Sending.")
            ser.write(struct.pack(">L", size_of_image))
            b_output = b''
            # read acknowledgment from user
            while len(b_output) == 0:
                b_output = ser.read(1)

            # if acknowledgement received
            if struct.unpack(">B", b_output)[0] != 1:
                print("Size was not acknowledged.")
                break
            
            print("Size was acknowledged.")
            
            # send the image over
            print("Image sending.")
            ser.write(buffer)
            print("Image sent.")

        # interactive mode
        elif request[0] == 2:
            # do the controller connection
            print("Receiving status update on controller...")

            # keep reading if the controller connected
            # !TODO: currently not very useful
            did_controller_connect = b''
            while len(did_controller_connect) == 0:
                did_controller_connect = ser.read(1)

            did_controller_connect = struct.unpack(">B", did_controller_connect)[0]

            # if the controller did not connect, stop
            if not did_controller_connect:
                print("Controller failed to connect. exiting.")
                continue

            print("Controller connected. Receiving inputs.")

            # set up thread to send photos at the same time
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            keep_sending_images = True
            future = executor.submit(send_images, ser)

            # read the controls and output that through a function
            try:
                while True:
                    can_read = ser.read(struct.calcsize(">B"))[0]

                    if can_read == 0:
                        break

                    #!TODO: This doesn't work. the ints/floats are ordered strangely in sean's code
                    first_float_output = ser.read(struct.calcsize(">f"))
                    if not len(first_float_output):
                        continue
                    second_float_output = ser.read(struct.calcsize(">f"))
                    int_output = ser.read(56)
                    floats = []
                    floats.append(struct.unpack(">f", first_float_output))
                    floats.append(struct.unpack(">f", second_float_output))
                    ints = np.frombuffer(int_output, dtype=np.uint32)
                    curr_value = floats + ints
                    
                    if False:
                    #if curr_value == 1_000:
                        print("Exiting interactive mode.")
                        keep_sending_images = False
                        future.cancel()
                        executor.shutdown()
                        break
                    #send_images(ser)

                    # TODO function to output controls through or something
                    print(curr_value)
            except Exception as e:
                print(e)
            finally:
                keep_sending_images = False
                future.cancel()
                executor.shutdown()

            print("Exiting interactive mode.")

        ##### receive a word to autonomously do the arm control with        
        elif request[0] == 3:
            print("Receiving word to input.")
            b_read_output = b''
            while len(b_read_output) == 0:
                b_read_output = ser.readline()

            word = b_read_output.decode()
            print(f"Word received: {word[:-1]}")

        ##### heartbeat mode: send over GNSS coordinates
        elif request[0] == 4:
            print("Activating heartbeat mode. Sending coordinates...")
            ser.timeout = 1.0
            while True:
                # read if it should stop
                should_end = ser.read(1)
                if len(should_end) != 0:
                    break

                # !TODO: actually receive the coordinates somehow
                try:
                    # temp coords for x, y
                    coord_x = "3.141592654"
                    coord_y = "2.718281828"

                # if the coordinate grabbing fails
                except:
                    coord_x = "-1"
                    coord_y = "-1"

                coord_string = f"{coord_x} {coord_y}\n"
                ser.write(coord_string.encode())

            print("Quitting heartbeat mode.")

        awaiting_request = True
        request = b''           

    ser.close()
    #executor.shutdown()
