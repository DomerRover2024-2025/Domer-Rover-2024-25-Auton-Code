# This is the "one performing the ssh-ing"

import serial

#port = "/dev/cu.usbserial-BG00HO5R"
port = "COM3"
baud = 57600
timeout = 15
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

reading = True

while (True):
    # reading the next command
    if reading:
        if ser.in_waiting != 0:
            output = ser.read(ser.in_waiting)
            reading = False
    request = input(str(output))
    ser.write(bytes(request))
    reading = True
    while reading:
        if ser.in_waiting != 0:
            output = ser.read(ser.in_waiting)
            reading = False
    print(str(output))
    reading = True

ser.close()





cv2.destroyAllWindows()