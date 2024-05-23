import serial
import json
import time
# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB1', 9600)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        data = line.split(",")
        print(data)
        data = ""
        time.sleep(60)
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    ser.close()
    print("Serial port closed.")