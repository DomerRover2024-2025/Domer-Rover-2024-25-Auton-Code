import serial
import time

arduino = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    writeTimeout=2
)

# Loop
while True:
    try:
        command = str(input("Enter command: ")) + "["
        arduino.write(command.encode())
        data = arduino.readline()
        if data:
            print(data)
    except Exception as e:
        print(e)
        arduino.close()
