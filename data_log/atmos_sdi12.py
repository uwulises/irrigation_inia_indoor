import serial

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        # Print the received line
        print(line.split(","))
        
        line = ""
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    ser.close()
    print("Serial port closed.")