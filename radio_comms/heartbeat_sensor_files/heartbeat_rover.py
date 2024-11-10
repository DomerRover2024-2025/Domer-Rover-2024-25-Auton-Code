import serial
import time

port = "/dev/ttys047"
baud = 57600
timeout = 2
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

try:
    while True:
        ser.write(b"Heartbeat\r\n")
        time.sleep(2)
except:
    ser.close()