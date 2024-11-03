import serial

port = "/dev/cu.usbserial-B001VC58"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
ser.write(b'Hello world!')
ser.flushInput()
ser.flushOutput()
try:
    while(True):
        pass
except KeyboardInterrupt:
    pass