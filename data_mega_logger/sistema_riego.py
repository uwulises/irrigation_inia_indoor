import serial
import json
import datetime
import os
import time
'''Mensaje serial para riego "REG_S00_L0000_T0000\n"
    Considera lado 0 y 1, litros o tiempo de riego'''

LISIMETRO_MINIMO_GR = 18700
HUMEDAD_SUELO_MINIMA = 90.0
CAPACIDAD_CAMPO_0 = 224.0
CAPACIDAD_CAMPO_1 = 192.0
CAPACIDAD_CAMPO_2 = 224.0
VPMP0=CAPACIDAD_CAMPO_0/2
VPMP1=CAPACIDAD_CAMPO_1/2
VPMP2=CAPACIDAD_CAMPO_2/2
S_PORT= '/dev/ttyACM0'
TIEMPO_RIEGO_LISIMETRO = 308 #600g

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
    moist_0_level= int(100*(1-(CAPACIDAD_CAMPO_2-moisture_level0)/(CAPACIDAD_CAMPO_2-VPMP2)))
    #moist_1_level= 100*(1-(CAPACIDAD_CAMPO_1-moisture_level1)/(CAPACIDAD_CAMPO_1-VPMP1))
    print("moist_0_level: ", moist_0_level)
    if moist_0_level < HUMEDAD_SUELO_MINIMA:
        limit_0 = CAPACIDAD_CAMPO_0
        msg = "HUM_S00_" + "L" + str(limit_0).zfill(4) + "\n"
        #print("msg: ",msg)
        ser.write(msg.encode())
    # elif moist_1_level < HUMEDAD_SUELO_MINIMA:
    #     limit_1 = CAPACIDAD_CAMPO_1
    #     msg = "HUM_S01_" + "L" + str(limit_1).zfill(4) + "\n"
    #     ser.write(msg.encode())
    msg=""

'''#Revisa si hay mas de 400g de diferencia y debe reponer hasta 19300g
    El riego es de 3 min 48s a eficiencia de 90%
    Riega ensayo T1
    "REG_S01_L0000_T0000\n" '''

def check_lisimetro(lisimetro):
    global ser
    if (LISIMETRO_MINIMO_GR-lisimetro) > 400:
        tiempo = TIEMPO_RIEGO_LISIMETRO
        #zfill 4 digits for recarga_litros
        recarga = f"T{str(tiempo).zfill(4)}\n"
        msg = "REG_S01_L0000_" + recarga
        ser.write(msg.encode())
    msg=""

# Initialize serial connection
try:
    ser = serial.Serial(S_PORT, 9600, timeout=305,write_timeout=5) 
except serial.SerialException as e:
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

while True:
    try:
        data = ser.readline().decode('utf-8').strip()
        print("data: ",data)
        if not data:
            continue  # Skip empty lines
        elif data.startswith('{') and data.endswith('}'):
            try:
                # Parse the JSON data
                data_dict = json.loads(data)
                print("data income: ",data_dict)
            except json.JSONDecodeError as e:
                print(e)
                continue  # Skip invalid JSON

            # Add timestamp
            data_dict['timestamp'] = datetime.datetime.now().isoformat(timespec='seconds')

            # Load existing data from JSON file
            try:
                with open(json_file_path, 'r') as loadfile:
                    data_load = json.load(loadfile)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(e)
                data_load = []

            # Append the new data
            data_load.append(data_dict)

            # Write the updated data back to the JSON file
            with open(json_file_path, 'w') as dumpfile:
                json.dump(data_load, dumpfile, indent=4)
            dumpfile.close()
            moisture_level0 = int(data_dict['Sensor humedad suelo 0'])
            moisture_level1 = int(data_dict['Sensor humedad suelo 1'])
            lisimetro = int(data_dict['Lisimetro'])
            check_moisture_level(moisture_level0, moisture_level1)
            check_lisimetro(lisimetro)

    except Exception as e:
        print(e)
        time.sleep(2)
        pass
