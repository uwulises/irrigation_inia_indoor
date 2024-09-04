import serial
import json
import datetime
import os
import logging

'''Mensaje serial para riego "REG_S00_L0000_T0000\n"
    Considera lado 0 y 1, litros o tiempo de riego'''

LISIMETRO_MINIMO_GR = 10
HUMEDAD_MINIMA = 0.8
S_PORT= '/dev/ttyACM0'

def check_moisture_level(moisture_level0, moisture_level1):
    global ser    
    pass
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
logging.basicConfig(filename='serial_to_json.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize serial connection
try:
    ser = serial.Serial(S_PORT, 9600, timeout=305)  # 5-minute timeout
    logging.info("Serial connection established.")
except serial.SerialException as e:
    logging.error(f"Failed to connect to serial port: {e}")
    raise SystemExit(e)

# JSON file path
json_file_path = 'registros.json'

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump([], file)
    logging.info(f"Created new JSON file: {json_file_path}")

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
            logging.warning(f"Failed to decode JSON: {e}")
            continue  # Skip invalid JSON

        # Add timestamp
        data_dict['timestamp'] = datetime.datetime.now().isoformat(timespec='seconds')

        # Load existing data from JSON file
        try:
            with open(json_file_path, 'r') as loadfile:
                data_load = json.load(loadfile)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Error reading JSON file: {e}")
            data_load = []

        # Append the new data
        data_load.append(data_dict)

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as dumpfile:
            json.dump(data_load, dumpfile, indent=4)
        #logging.info(f"Data saved: {data_dict}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")