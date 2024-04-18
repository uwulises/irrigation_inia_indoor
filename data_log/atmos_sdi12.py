import serial

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        # Print the received line
        print("Received:", line)
        print("largo mensaje: ", len(line))
        #example message
        #Received: 183173, 0, 1, 4, 515, 1.5660001000, 38.2000010000, 0.2340000100, 98.8000110000
        #if len is more than 70, then it is a valid message
        if len(line)==77 or len(line)==78:
            #take the last two values as float
            print(line.split(","))
            print(line.split(","))
            # You can add your own processing logic here
        line = ""
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    ser.close()
    print("Serial port closed.")