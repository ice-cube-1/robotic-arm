import serial
arduino = serial.Serial('/dev/ttyUSB0', baudrate=115200)
arduino.write(bytes(f"5200\n","utf-8"))
