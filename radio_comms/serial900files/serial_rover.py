# This is the server side of a client-server model.
# This will be receiving requests from the base station.

import serial
import cv2
import sys
import struct
import numpy as np
import concurrent.futures
import time
#np.set_printoptions(threshold=sys.maxsize)

# function to capture image
# returns its size and the bytearray representing the image
def capture_image() -> tuple[int, bytearray]:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        #print("Failed to capture image.")
        return 0, None

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
    encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
    size_of_data = len(buffer)
    #size_packed = struct.pack("=L", size_of_data)
    return size_of_data, buffer

keep_sending_images = True

def send_images(ser: serial.Serial) -> None:
    while keep_sending_images:
        size_of_image, buffer = capture_image()

        packed_size = struct.pack("=L", size_of_image)
        ser.write(packed_size)
        if not size_of_image:
            return
        ser.write(buffer)
        time.sleep(1)
        


if __name__ == "__main__":
    #port = "/dev/cu.usbserial-BG00HO5R"
    port = "/dev/cu.usbserial-B001VC58"
    #port = "COM4"
    baud = 57600
    timeout = 3
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    #executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    awaiting_request = True

    while True:
        if awaiting_request:
            print("Awaiting request.")
            awaiting_request = False
        request = ser.read(1)

        # if nothing received, ask again
        if len(request) == 0:
            continue

        request = struct.unpack("=B", request)

        # quit the connection
        if request[0] == 0:
            print("Request to quit received.")
            exit_success = 1 # hardcode a success right now
            ser.write(struct.pack("=B", exit_success))
            if exit_success == 1:
                break

        # ask for a photo
        elif request[0] == 1:
            print("Request for image received.")
            
            size_of_image, buffer = capture_image()

            if size_of_image == 0:
                print("Image capture failed.")
                ser.write(struct.pack("=L", size_of_image))
                continue

            #print(size_of_data, sys.getsizeof(buffer))
            print("Size of image calculating. Sending.")
            ser.write(struct.pack("=L", size_of_image))

            while True:
                b_output = ser.read(1)
                if b_output != b'':
                    if struct.unpack("=B", b_output)[0] == 1:
                        print("Size was acknowledged.")
                        break
            print("Image sending.")
            #with open("temp.txt", "w") as f:
            #    f.write(str(buffer))
            ser.write(buffer)
        
        # interactive mode
        elif request[0] == 2:
            # do the controller connection
            print("Receiving status update on controller...")
            while True:
                did_controller_connect = ser.read(1)
                if len(did_controller_connect):
                    break
            did_controller_connect = struct.unpack("=B", did_controller_connect)[0]

            # if the controller did not connect, stop
            if not did_controller_connect:
                print("Controller failed to connect. exiting.")
                continue

            keep_sending_images = True
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

            try:
                future = executor.submit(send_images, ser)
            except:
                print("Some issue with the executor")

            print("Controller connected. Receiving inputs.")

            while True:
                current_output = ser.read(struct.calcsize("=B"))
                if not len(current_output):
                    continue

                curr_value = struct.unpack("=B", current_output)[0]
                if curr_value == 0:
                    print("Exiting interactive mode.")
                    keep_sending_images = False
                    future.cancel()
                    executor.shutdown()
                    break
                #send_images(ser)

                print(curr_value)
        awaiting_request = True
        request = b''           

    ser.close()
    #executor.shutdown()