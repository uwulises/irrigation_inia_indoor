import serial
import json
import datetime
import os
import time
#import logging
'''Mensaje serial para riego "REG_S00_L0000_T0000\n"
    Considera lado 0 y 1, litros o tiempo de riego'''

S_PORT= '/dev/ttyACM0'

def riego_manual(lado, litros, tiempo):
    global ser
    if lado == 0:
        msg = "REG_S00_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
    elif lado == 1:
        msg = "REG_S01_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
    elif lado == 2:
        msg = "REG_S11_" + "L" + str(litros).zfill(4) + "_T" + str(tiempo).zfill(4) + "\n"
        ser.write(msg.encode())
    else:
        print("Lado no valido")

try:
    ser = serial.Serial(S_PORT, 9600,timeout=305,write_timeout=10)  # 5-minute timeout
    time.sleep(2)
    riego_manual(0,0,114)
# logging.info("Serial connection established.")
except serial.SerialException as e:
    #logging.error(f"Failed to connect to serial port: {e}")
    raise SystemExit(e)




