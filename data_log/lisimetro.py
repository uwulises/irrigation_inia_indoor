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
        load_cell.send_command("MEAS\n")
        time.sleep(20)
        # Read a line from the serial port
        #Decode this line and take each value [b'SumaV1V2V3V4,19347.48,6381.76,5840.10,3131.46,3994.16\r\n']
        msg = load_cell.read()
        print(msg)
        if len(msg) == 6:
            #decode
            msg = msg.decode("utf-8")
            #split the string
            msg = msg.split(",")
            measure = {"Peso total":msg[1],"valor1":msg[2],"valor2":msg[3],"valor3":msg[4],"valor4":msg[5]}
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