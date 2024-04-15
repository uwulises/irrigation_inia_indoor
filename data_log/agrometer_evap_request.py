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
Phidget = SimplePhidget()
Phidget.begin()  # Inicializacion minima

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


def init_state_entry():
    global year_month_day
    print("Iniciando sistema de riego.")
    time.sleep(1)  # Espera de inicializacion
    init_time = ''
    print("Llamada a hora local")
    init_call_time = call_datetime()
    init_time = init_call_time[0]
    year_month_day = init_call_time[1]
    estado_valvula_0 = Phidget.valve0_state
    estado_valvula_1 = Phidget.valve1_state
    estado_humedad_0 = round(Phidget.moist_sensor0(), 2)
    estado_humedad_1 = round(Phidget.moist_sensor1(), 2)
    radiation = round(Phidget.pyr20_sensor(), 2)
    # log inicial del estado de sensores y actuadores
    add_status_log_entry(AAAA_MM_DD=year_month_day, State='Iniciando', tiempo_inicio=init_time, tiempo_actual=init_time, tiempo_termino=init_time,
                         valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=radiation, evapo_t_acum=EVAPOTRANSPIRACION_ACUMULADA)
