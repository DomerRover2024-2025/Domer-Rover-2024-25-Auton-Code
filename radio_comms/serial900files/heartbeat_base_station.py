import serial
import struct


# specify port, baud, timeout, and create serial object
port = "/dev/cu.usbserial-BG00HO5R"
baud = 57600
timeout = 5
ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

# should receive a heartbeat every second
try:
    while True:
        output = ser.read(1)
        if output != b'':
            real_output = struct.unpack("B", output)
            print(real_output[0])
        
        #     print(output, "Heartbeat received.")
        # else:
        #     print("Lost the rover. Continuing to receive messages...")
except:
    ser.close()