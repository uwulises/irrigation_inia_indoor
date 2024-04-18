import serial

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        # Print the received line
        print(line.split(","))
        #wait for this message ['-------------------------------------------------------------------------------']
        if len(line.split(",")) == 9:
            #take the last value of the list
            print("Humedad",line.split(",")[-2])
            print("Temperatura °F",line.split(",")[-1])
        line = ""
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    ser.close()
    print("Serial port closed.")