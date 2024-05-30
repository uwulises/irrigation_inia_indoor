import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from serial_control import SerialControl
import time
import json
# Create an instance of the SerialControl class
load_cell = SerialControl(port="/dev/ttyUSB1", baudrate=9600)

# Open the serial port
load_cell.open_serial()

try:
    while True:
        load_cell.send_command("MEAS\n")
        time.sleep(5)
        # Read a line from the serial port
        line = load_cell.read()
        msg = line.split(",")
        measure = {"Peso total":msg[0],"valor1":msg[1],"valor2":msg[2],"valor3":msg[3],"valor4":msg[4]}
        #save data message as json, or edit the file
        with open('lisimetro.json', 'w') as f:
            json.dump(measure, f)
        #close the file
        f.close()
        print(msg)
        msg = ""
        time.sleep(60)
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    load_cell.close_serial()
    print("Serial port closed.")