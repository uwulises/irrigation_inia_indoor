# Importacion de request para conteo de tiempo/fecha
# Time zone request worldtime api
import time
from time_zone_request import call_datetime, check_log_time_variable
# Funciones para crear y agregar informacion en .csv y .xlsx
from logger import add_status_log_entry, get_tiempo_actual_csv
# Clase de PhidgetInterfaceKit 8/8/8 w/6 Port Hub
# Objeto Phidget cuenta con acciones I/O
from phidget_simple import SimplePhidget
import time
import numpy as np
# Creacion de objeto phidget
# Phidget = SimplePhidget()
# Phidget.begin()  # Inicializacion minima

# Valores corte para humedad, revisar en el lugar
HUMEDAD_MINIMA = 1.25
# Evapotranspiracion maxima para riego
EVAPOTRANSPIRACION_MINIMA = 0.5
# Variable de evapotranspiracion acumulada
EVAPOTRANSPIRACION_ACUMULADA = 0
# 013DECAGON VP-4  38910433-01-127
# Variable de ultima fecha y hora de registro de riego

# Variable para evitar riego si ya se realizo hace poco tiempo


def evapotranspiracion():
    # Sensor de temperatura, humedad, radiación y viento
    # Calculo de evapotranspiracion
    # create an array with 4 values, temperature, humidity, radiation and wind speed
    acumulate_array = np.array([0.0, 0.0, 0.0, 0.0])
    # call sensors

    return
