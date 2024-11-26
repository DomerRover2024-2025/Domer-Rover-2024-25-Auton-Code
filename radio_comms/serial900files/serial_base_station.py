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

#p.set_printoptions(threshold=sys.maxsize)

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
    #info_file = open("some_info.txt", 'w')
    while keep_reading_images:

        size_of_image = ser.read(struct.calcsize("=L"))
        #print(size_of_image)
        if len(size_of_image) != struct.calcsize("=L"):
            #print("it no work !")
            continue
        
        size_of_image = struct.unpack("=L", size_of_image)[0]

        if size_of_image == 0:
            #print("Image capturing failed. Returning to menu.")
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
            #info_file.write(f'.{size_of_image - len(b_output)}.')
            #print(len(b_output))

        #info_file.write("captured image\n")
        success = save_and_output_image(b_output=b_output)
        #if success:
            #info_file.write("ok")
        #else:
            #info_file.write("no")
        #info_file.write("-------\n")
        #time.sleep(1)
    #info_file.close()
    #ser.reset_output_buffer()

def flush_whats_coming_in(ser: serial.Serial) -> int:
    count : int = 0
    while True:
        output = ser.read(1)
        if not len(output): break
        count += len(output)
    return count

if __name__ == "__main__":
    #port = "/dev/cu.usbserial-BG00HO5R"
    port = "COM3"
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
        
        if request == 10:
            with open("remaining_content.txt", 'bw') as f:
                while True:
                    output = ser.read(1)
                    if not len(output): break
                    f.write(output)
            continue
        
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
            
            joysticks, text_print, screen = joystickDriving.init()

            ser.write(struct.pack("=B", controller_connected))
            if not controller_connected:
                print("Controller not responding. Exiting interactive mode, sending update.")
                continue

            print("Controller responded.")

            print("Enter int to represent control input:")

            run = joystickDriving.run(joysticks, text_print, screen)

            image_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            keep_reading_images = True
            try:
                future = image_executor.submit(read_images, ser)
            except:
                print("Some issue with executor")

            while True:
                #current_control = input(">> ")
                current_control = next(run)[3]
                if not len(current_control):
                    print("Please enter a number.", file=sys.stderr)
                    continue
                try:
                    int_curr_control = int(current_control)
                except ValueError as v:
                    print(f"{v}: please enter an integer in [0, 255].", file=sys.stderr)
                    continue
                if int(current_control) > 255 or int(current_control) < 0:
                    print("Controls must be between 0 and 255.", file=sys.stderr)
                    continue
                ser.write(struct.pack("=B", int(current_control)))

                # on exit:
                if int(current_control) == 0:
                    keep_reading_images = False
                    print("cancelling future")
                    future.cancel()
                    print("shutting down executor")
                    image_executor.shutdown()
                    print("outwaiting: ", ser.out_waiting)
                    print("inwaiting: ", ser.in_waiting)
                    data_lost = flush_whats_coming_in(ser)
                    print("data lost: ", data_lost)
                    break
                #read_images(ser)

            print("Quitting interactive mode.")
                

    ser.close()
    cv2.destroyAllWindows()