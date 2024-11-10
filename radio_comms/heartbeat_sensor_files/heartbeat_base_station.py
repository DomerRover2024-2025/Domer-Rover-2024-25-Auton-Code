import serial

# specify port, baud, timeout, and create serial object
port = "/dev/ttys047"
baud = 57600
timeout = 5
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

# should receive a heartbeat every second
try:
    while True:
        try:
            output = ser.readline()
            print(output)
            print("Heartbeat received.")
        except TimeoutError as e:
            print("Lost the rover. Continuing to receive messages...")
except:
    ser.close()