# This is the client side of a client-server model.
# This will be sending requests to the rover.

import serial
import numpy as np
import cv2
import time
import struct
import sys
import joystickDriving
import concurrent.futures

np.set_printoptions(threshold=sys.maxsize)

def print_options() -> None:
    print("(0) to quit")
    print("(1) for photo")
    print("(2) for interactive mode")

def save_and_output_image(b_output : bytearray) -> bool:
    try:
        image = np.frombuffer(b_output, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        currtime = time.time()
        cv2.imwrite(f"photos/{currtime}.jpg", frame)
        cv2.imshow('frame', frame)
    #print("Image received and shown.")
        cv2.waitKey(1)
        return True
    except:
        return False
    
keep_reading_images = True
def read_images(ser : serial.Serial):
    while keep_reading_images:
        size_of_image = ser.read(struct.calcsize("=L"))
        if len(size_of_image) != struct.calcsize("=L"):
            continue
        size_of_image = struct.unpack("=L", size_of_image)[0]
            # print("size of image:", size_of_image)
            # print("Size received. Sending acknowledgement.")
            # ser.write(struct.pack("=B", 1))
            # break
        if size_of_image == 0:
            #print("Image capturing failed. Returning to menu.")
            continue
        b_output = b''

        prev_output = -1

        while len(b_output) < size_of_image or prev_output != len(b_output):
            b_output += ser.read(10_000)
            prev_output = len(b_output)
        
        success = save_and_output_image(b_output=b_output)
        #time.sleep(1)

if __name__ == "__main__":
    #port = "/dev/cu.usbserial-BG00HO5R"
    port = "COM4"
    baud = 57600
    timeout = 3
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    MAXBYTES = 70_000
    while True:
        print_options()
        request = input(">> ")
        request = int(request)
        ser.write(struct.pack("=B", request))

        if request == 0: # end connection
            print("Request to quit sent.")

            ack = struct.unpack("=B", ser.read(1))
            if ack[0] == 1: # successful connection break
                print("Request successful.")
                break
            else:
                print("Request unsuccessful.")

        if request == 1: # photo
            while True:
                size_of_image = ser.read(struct.calcsize("=L"))
                if len(size_of_image) == struct.calcsize("=L"):
                    size_of_image = struct.unpack("=L", size_of_image)[0]
                    print("size of image:", size_of_image)
                    print("Size received. Sending acknowledgement.")
                    ser.write(struct.pack("=B", 1))
                    break
            if size_of_image == 0:
                print("Image capturing failed. Returning to menu.")
                continue
            b_output = b''
            #prev_len = -1
            time.sleep(1)
            while len(b_output) < size_of_image:
                b_output += ser.read(10_000)

            success = save_and_output_image(b_output=b_output)
            if not success:
                print("Image failed to be read/shown.")
            else:
                print("Image successfully saved and shown.")

        # interactive, controller mode
        if request == 2:
            print("Entering interactive mode. Connecting to controller...")
            # send controller connected
            controller_connected = True
            #joysticks, text_print, screen = joystickDriving.init()

            ser.write(struct.pack("=B", controller_connected))
            if not controller_connected:
                print("Controller not responding. Exiting interactive mode, sending update.")
                continue

            print("Controller responded.")

            print("Enter int to represent control input:")

            #run = joystickDriving.run(joysticks, text_print, screen)
            image_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            keep_reading_images = True
            try:
                future = image_executor.submit(read_images, ser)
            except:
                print("Some issue with executor")

            while True:
                current_control = input(">> ")
                #current_control = next(run)
                try:
                    int_curr_control = int(current_control)
                except ValueError as v:
                    print(f"{v}: please enter an integer in [0, 255].", file=sys.stderr)
                if int(current_control) > 255 or int(current_control) < 0:
                    print("Controls must be between 0 and 255.", file=sys.stderr)
                    continue
                ser.write(struct.pack("=B", int(current_control)))
                if int(current_control) == 0:
                    keep_reading_images = False
                    print("cancelling future")
                    future.cancel()
                    print("shutting down executor")
                    image_executor.shutdown()
                    print("breaking loop")
                    break
                #read_images(ser)

            print("Quitting interactive mode.")
                

    ser.close()
    cv2.destroyAllWindows()