import serial
import json
import datetime
import os
import time
#import logging
'''Mensaje serial para riego "REG_S00_L0000_T0000\n"
    Considera lado 0 y 1, litros o tiempo de riego'''

LISIMETRO_MINIMO_GR = 10
HUMEDAD_SUELO_MINIMA = 80
CAPACIDAD_CAMPO_0 = 224
CAPACIDAD_CAMPO_1 = 192
CAPACIDAD_CAMPO_2 = 224
VPMP0=CAPACIDAD_CAMPO_0/2
VPMP1=CAPACIDAD_CAMPO_1/2
VPMP2=CAPACIDAD_CAMPO_2/2
S_PORT= '/dev/ttyACM0'

def riego_manual(lado, tiempo, litros):
    global ser
    if lado == 0:
        msg = "REG_S00_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
        time.sleep(2)
    elif lado == 1:
        msg = "REG_S01_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
        time.sleep(2)
    elif lado == 2:
        msg = "REG_S11_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
        time.sleep(2)
    else:
        print("Lado no valido")

def check_moisture_level(moisture_level0, moisture_level1): 
    global ser
    moist_0_level= 100*(1-(CAPACIDAD_CAMPO_2-moisture_level0)/(CAPACIDAD_CAMPO_2-VPMP2))
    moist_1_level= 100*(1-(CAPACIDAD_CAMPO_1-moisture_level1)/(CAPACIDAD_CAMPO_1-VPMP1))
    if moist_0_level < HUMEDAD_SUELO_MINIMA and moist_1_level < HUMEDAD_SUELO_MINIMA:
        recarga_tiempo=102
        msg = "REG_S11_" + "L0000" + "_T" + str(recarga_tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
    elif moist_0_level < HUMEDAD_SUELO_MINIMA:
        recarga_tiempo=102
        msg = "REG_S00_" + "L0000" + "_T" + str(recarga_tiempo).zfill(4) + "\n"
        ser.write(msg.encode())    
    elif moist_1_level < HUMEDAD_SUELO_MINIMA:
        recarga_tiempo=102
        msg = "REG_S01_" + "L0000" + "_T" + str(recarga_tiempo).zfill(4) + "\n"
        ser.write(msg.encode())

def check_lisimetro(lisimetro):
    global ser
    if lisimetro < LISIMETRO_MINIMO_GR:
        recarga_litros=int(abs(lisimetro-LISIMETRO_MINIMO_GR)/1000)
        #zfill 4 digits for recarga_litros
        recarga = f"L{str(recarga_litros).zfill(4)}"
        msg = "REG_S00_" + recarga + "_T0000\n"
        ser.write(msg.encode())
    pass

# Setup logging
# logging.basicConfig(filename='serial_to_json.log', level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize serial connection
try:
    ser = serial.Serial(S_PORT, 9600, timeout=305)  # 5-minute timeout
   # logging.info("Serial connection established.")
except serial.SerialException as e:
    #logging.error(f"Failed to connect to serial port: {e}")
    #raise SystemExit(e)
    print(e)
    pass

# JSON file path
json_file_path = 'registros.json'

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump([], file)
    file.close()
    #logging.info(f"Created new JSON file: {json_file_path}")

while True:
    try:
        # Read serial data (wait up to 5 minutes for a message)
        data = ser.readline().decode('utf-8').strip()
        if not data:
            continue  # Skip empty lines

        try:
            # Parse the JSON data
            data_dict = json.loads(data)
        except json.JSONDecodeError as e:
           # logging.warning(f"Failed to decode JSON: {e}")
            print(e)
            continue  # Skip invalid JSON

        # Add timestamp
        data_dict['timestamp'] = datetime.datetime.now().isoformat(timespec='seconds')

        # Load existing data from JSON file
        try:
            with open(json_file_path, 'r') as loadfile:
                data_load = json.load(loadfile)
        except (json.JSONDecodeError, FileNotFoundError) as e:
           # logging.error(f"Error reading JSON file: {e}")
            print(e)
            data_load = []

        # Append the new data
        data_load.append(data_dict)

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as dumpfile:
            json.dump(data_load, dumpfile, indent=4)
        dumpfile.close()
        #logging.info(f"Data saved: {data_dict}")
        #take last moisture level and lisimetro value
        moisture_level0 = data_dict['moisture_level0']
        moisture_level1 = data_dict['moisture_level1']
        lisimetro = data_dict['lisimetro']
        check_moisture_level(moisture_level0, moisture_level1)

    except Exception as e:
        print(e)
        pass
      #  logging.error(f"An unexpected error occurred: {e}")
