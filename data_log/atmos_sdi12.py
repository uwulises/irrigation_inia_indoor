import serial
import json

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        data = line.split(",")
        #wait for this message ['-------------------------------------------------------------------------------']
        if len(data) == 9:
            #take the last value of the list
            #print("Humedad",data[-2])
            #print("Temperatura °F",data[-1])
            registro={"Humedad":data[-2],"Temperatura":data[-1]}
            #save data as json, or edit the file
            with open('atmos.json', 'w') as f:
                json.dump(registro, f)
            #close the file
            f.close()
        data = ""
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    ser.close()
    print("Serial port closed.")