import serial
import time


# specify port, baud, timeout, and create serial object
port = "/dev/cu.usbserial-BG00HO5R"
#port = "/dev/cu.usbserial-B001VC58"
baud = 57600
timeout = 5
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

# should receive a heartbeat every second
try:
    while True:
        ser.write(b"What the hell\r\n")
        output = ser.readline()
        print(output)
        #time.sleep(1)
except:
    ser.close()