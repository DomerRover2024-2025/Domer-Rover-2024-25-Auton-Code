import serial
import time

#arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=5)

arduino = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    bytesyze=serial.EIGHTBITS,
    parity=serial.PERITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout=5,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    writeTimeout=2
)

while True:
    try:
        command = input("Enter number: ")
        command = command + "["
        arduino.write(command.encode())
        data = aruino.readline()
        if data:
            print(data)
        except Exception as e:
            print(e)
            arduino.close()
