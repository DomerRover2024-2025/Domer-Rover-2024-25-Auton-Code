import serial

port = "COM3"
baud = 57600
timeout = 3
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
output = ser.read()
print(str(output))
# ser.flushInput()
# ser.flushOutput()
try:
    while(True):
        pass
except KeyboardInterrupt:
    pass