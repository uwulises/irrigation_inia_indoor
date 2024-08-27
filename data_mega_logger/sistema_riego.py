#take the json from arduino and save it as json with timestamp
import serial
import json
import datetime
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    data = ser.readline().decode('utf-8')
    #look for json format
    data = json.loads(data)
    #isoformat()
    data['timestamp'] = datetime.datetime.now().isoformat(timespec='seconds')

    with open('registros.json', 'r') as loadfile:
        data_load = json.load(loadfile)
    
    data_load.append(data)
    with open('registros.json', 'w') as dumpfile:
        json.dump(data_load, dumpfile, indent=4)
    dumpfile.close()