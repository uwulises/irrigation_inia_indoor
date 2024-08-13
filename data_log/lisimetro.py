import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../serial"))
from serial_control import SerialControl
import time
import json
# Create an instance of the SerialControl class
load_cell = SerialControl(port="/dev/ttyUSB1", baudrate=9600)

# Open the serial port
load_cell.open_serial()

try:
    while True:
        # Read a line from the serial port
        peso = load_cell.read_lisimetro()
        registro={"Peso total":peso}
        with open('lisimetro.json', 'w') as f:
            json.dump(registro, f)
        #close the file
        f.close()
        registro = ""
        
except KeyboardInterrupt:
    # If user interrupts, close the serial port
    load_cell.close_serial()
    print("Serial port closed.")