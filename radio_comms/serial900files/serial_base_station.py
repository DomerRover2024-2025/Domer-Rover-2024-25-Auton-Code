# This is the client side of a client-server model.
# This will be sending requests to the rover.

###################
##### IMPORTS #####
###################

import serial
import numpy as np
import cv2
import time
import struct
import sys
import joystickDriving
import concurrent.futures

#p.set_printoptions(threshold=sys.maxsize)

#####################
##### FUNCTIONS #####
#####################

def print_options() -> None:
    print("----------------")
    print("MENU OF CONTROLS")
    print("----------------")
    print("(0) to quit")
    print("(1) for photo")
    print("(2) for interactive mode")
    print("(3) for sending word to arm to type out")
    print("(4) Heartbeat mode: Receive coordinates")

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
        size_of_image = ser.read(struct.calcsize(">L"))
        if len(size_of_image) != struct.calcsize(">L"):
            continue
        
        size_of_image = struct.unpack(">L", size_of_image)[0]
        if size_of_image == 0:
            continue

        b_output = b''
        prev_output = -1
        while len(b_output) < size_of_image or prev_output != len(b_output):
            if size_of_image - len(b_output) < 5_000:
                addition = ser.read(size_of_image - len(b_output))
            else:
                addition = ser.read(5_000)
            b_output += addition
            prev_output = len(b_output)

        success = save_and_output_image(b_output=b_output)

def flush_whats_coming_in(ser: serial.Serial) -> int:
    count : int = 0
    while True:
        output = ser.read(1)
        if not len(output): break
        count += len(output)
    return count

################
##### MAIN #####
################

if __name__ == "__main__":
    port = "/dev/tty.usbserial-BG00HO5R"
    #port = "/dev/cu.usbserial-B001VC58"
    #port = "COM3"
    baud = 57600
    timeout = 3
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # the main control
    while True:
        print_options()
        request = input(">> ")
        request = int(request)
        
        # this request is for debugging, and prints the remaining contents
        # of the buffer into a file
        if request == 10:
            with open("remaining_content.txt", 'bw') as f:
                while True:
                    output = ser.read(1)
                    if not len(output): break
                    f.write(output)
            continue
        
        # otherwise it sends the request over to the client
        ser.write(struct.pack("=B", request))

        time.sleep(0.25)
        ###### end connection ######
        if request == 0: 
            print("Request to quit sent.")

            # read whether the server quit or not
            ack = struct.unpack("=B", ser.read(1))

            # if the return acknowledgment is 1, then request was successful
            if ack[0] == 1:
                print("Request successful.")
                break
            else:
                print("Request unsuccessful.")

        ##### ask for a photo #####
        elif request == 1:
            size_of_image = b''
            while len(size_of_image) != struct.calcsize(">L"):
                # read the size of the image from the server
                size_of_image += ser.read(struct.calcsize(">L"))

        # if actually grabbed a number the length of the size of the image,
        # unpack it and send an acknowledgment that it was received
            size_of_image = struct.unpack(">L", size_of_image)[0]
            print("size of image:", size_of_image)

            # if the size of the image is 0 interpret as a fail
            if size_of_image == 0:
                print("Image capturing failed. Returning to menu.")
                continue
    
            print("Size received. Sending acknowledgement.")
            ser.write(struct.pack("=B", 1))

            b_output = b''
            time.sleep(1)

            print("Reading image.")

            # keep reading until the entire image is read
            while len(b_output) < size_of_image:
                b_output += ser.read(8_192) # duplicate of 2

            print("Bytes equal to size of image read.")

            # save and output the image
            success = save_and_output_image(b_output=b_output)
            if not success:
                print("Image failed to be saved/shown.")
            else:
                print("Image successfully saved and shown.")

        ##### interactive, controller mode #####
        elif request == 2:
            print("Entering interactive mode. Connecting to controller...")
            
            # !TODO: fix this controller whatnot
            # send controller connected
            controller_connected = True
            
            joysticks = {}

            # send over that the controller connected
            ser.write(struct.pack("=B", controller_connected))

            # if the controller failed (also unnecessary right now)
            if not controller_connected:
                print("Controller not responding. Exiting interactive mode, sending update.")
                continue

            print("Controller responded.")
            print("Use the controller now:")

            # this is a generator to control the controller
            run = joystickDriving.run(joysticks)

            # set things up to receive photos at the same time
            image_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            keep_reading_images = True
            future = image_executor.submit(read_images, ser)

            try:
                good_control = 1
                while True:
                    #current_control = input(">> ")

                    # get the current controls, which is a 16-long array of
                    # mixed int and float values
                    try:
                        current_control = next(run)
                    except Exception as e:
                        print(e)
                        good_control = 0
                        # if not len(current_control):
                        #     print("Please enter a number.", file=sys.stderr)
                        #     continue
                        # try:
                        #     int_curr_control = int(cSurrent_control)
                        # except ValueError as v:
                        #     print(f"{v}: please enter an integer in [0, 255].", file=sys.stderr)
                        #     continue
                        # if int(current_control) > 255 or int(current_control) < 0:
                        #     print("Controls must be between 0 and 255.", file=sys.stderr)
                        #     continue
                    ser.write(struct.pack(">B", good_control))

                    # stop sending over anything if the controller failed or something along those lines
                    if good_control == 0:
                        break

                    #!TODO: This doesn't work. the ints/floats are ordered strangely in sean's code
                    float_controls = current_control[:2]
                    int_controls = current_control[2:]
                    ser.write(struct.pack(">f", float_controls[0]))
                    ser.write(struct.pack(">f", float_controls[1]))
                    ser.write(bytearray(int_controls))
                    #ser.write(struct.pack("=B", int(current_control)))

                    # on exit:
                    if False:
                    #if int(current_control) == 1_000:
                        break
            except Exception as e:
                print(e)
            finally:
                keep_reading_images = False
                print("cancelling future")
                future.cancel()
                print("shutting down executor")
                image_executor.shutdown()
                print("outwaiting: ", ser.out_waiting)
                print("inwaiting: ", ser.in_waiting)
                data_lost = flush_whats_coming_in(ser)
                print("data lost: ", data_lost)

                #read_images(ser)

            print("Quitting interactive mode.")

        ##### send arm a word to autonomously take care of
        elif request == 3:
            print("Input word to command arm: ")
            word = input(">> ")

            ser.write(f"{word}\n".encode())

            print("Sent word.")
        
        ##### heartbeat mode: simply receive the float coordinates
        elif request == 4:
            print("Activating heartbeat mode. ^C to quit.")
            print("Receiving coordinates...")
            try:
                while True:
                    coordinates = ser.readline()
                    if len(coordinates) == 0:
                        print("Rover could not be found.")
                        continue

                    coord_x, coord_y = coordinates.decode().split()

                    print(f"coord_x = {coord_x}, coord_y = {coord_y}")
            except KeyboardInterrupt:
                print("Exiting heartbeat mode.")
                ser.write(b"1")

                

    ser.close()
    cv2.destroyAllWindows()
