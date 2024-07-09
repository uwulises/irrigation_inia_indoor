import serial
import json

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust baud rate according to your Arduino code

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        data = line.split(",")
        if len(data) == 9:
            humedad = round(float(data[-2]),2)
            temperatura = (round(float(data[-1]),2)-32)*5/9
            registro={"Humedad":humedad,"Temperatura":temperatura}
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