# This is the one being "logged into"

import serial
import subprocess
import os

#port = "/dev/cu.usbserial-BG00HO5R"
port = "/dev/cu.usbserial-B001VC58"
#port = "COM4"
baud = 57600
timeout = 5
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

ser.reset_input_buffer()
ser.reset_output_buffer()

reading = False

while True:
    if not reading:
        #print(f"{os.getcwd()} % \n")
        ser.write(f"{os.getcwd()} % \n".encode())
        reading = True
    request = ser.readline()
    if request != b'':
        reading = False
        args = str(request).strip().split()
        process = subprocess.run(args, capture_output=True)
        if process.stdout:
            ser.write(process.stdout)
        if process.stderr:
            ser.write(process.stderr)
        ser.write(b'\n')

ser.close()