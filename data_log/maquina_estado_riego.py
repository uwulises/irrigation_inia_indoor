import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "/log"))
# Importacion de request para conteo de tiempo/fecha
# Time zone request worldtime api
import time
from time_zone_request import call_datetime, check_log_time_variable, check_irrigation_time
# Funciones para crear y agregar informacion en .csv y .xlsx
from logger import add_status_log_entry, get_tiempo_actual_csv, add_entry, get_actual_time
#from agrometer_evap_request import init_state_entry
# Clase de PhidgetInterfaceKit 8/8/8 w/6 Port Hub
# Objeto Phidget cuenta con acciones I/O
from phidget_simple import SimplePhidget
import json
# Valores corte para humedad, revisar en el lugar
HUMEDAD_MINIMA = 0.1
# Evapotranspiracion maxima para riego
EVAPOTRANSPIRACION_MINIMA = 0.5
# Variable de evapotranspiracion acumulada
EVAPOTRANSPIRACION_ACUMULADA = 0
TIEMPO_RIEGO = 310 #segundos
# Variable de ultima fecha y hora de registro de riego

# Variable para evitar riego si ya se realizo hace poco tiempo


# Creacion de objeto phidget
Phidget = SimplePhidget() # Inicializacion minima

'''Maquina de estado
Revisa el estado de humedad en cada lado del invernadero
Revisa el paso del tiempo real (desde la raspberry)
Revisa el estado de la evapotranspiracion

Si pasa un tiempo >10min se revisa la humedad, evapotranspiracion
Cuando la condicion de humedad minima se cumple y/o la de evapotranspiracion, se ejecutan 30seg de riego continuo
y se loggea la informacion de los sensores durante el riego y la humedad final del sensor.
Si la condicion no se cumple se loggea informacion del estado de los sensores con el texto: EsperandoRiego

Una vez al dia se calcula la nueva evapotranspiracion acumulada y se reinicia el valor de la evapotranspiracion diaria
'''


class StateMachine:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def run(self):
        while True:
            try:
                if self.state:
                    self.state.execute()
                else:
                    print("None state")
                    time.sleep(10)
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                #print("Restarting the state machine...")
                self.state = InitState()  # Reset the state machine to initial state
                # # write a text file with the error and the time
                # with open('log/error_log.txt', 'a') as file:
                #     file.write(
                #         f"Error occurred: {str(e)} at {call_datetime()[0]}\n")
                #     # close the file
                #     file.close()


class State:
    def __init__(self, name):
        self.name = name

    def execute(self):
        pass


class InitState(State):
    def __init__(self):
        super().__init__('Init')

    def execute(self):
        global year_month_day
        print("Iniciando sistema de riego.")
        time.sleep(1)  # Espera de inicializacion
        init_time = ''
        #print("Llamada a hora local")
        init_call_time = call_datetime()
        init_time = init_call_time[0]
        year_month_day = init_call_time[1]
        Phidget.begin() # Inicializacion de phidget
        estado_valvula_0 = Phidget.valve0_state
        estado_valvula_1 = Phidget.valve1_state
        estado_humedad_0 = round(Phidget.moist_sensor0(), 3)
        estado_humedad_1 = round(Phidget.moist_sensor1(), 3)
        radiation = round(Phidget.pyr20_sensor(), 2)
        #load json data.json to get humedad y temperatura
        #{"Humedad":data[-2],"Temperatura":data[-1]}
        with open('atmos.json') as json_file:
            data = json.load(json_file)
            humedad = data["Humedad"]
            temperatura = data["Temperatura"]

        with open('lisimetro.json') as json2_file:
            lisimetro_meas = json.load(json2_file)
            suma_total=lisimetro_meas["Peso total"]
            
        json_file.close()
        json2_file.close()
        Phidget.stop()
        # log inicial del estado de sensores y actuadores
        #add_status_log_entry(AAAA_MM_DD=year_month_day, State='Iniciando', tiempo_inicio=init_time, tiempo_actual=init_time, tiempo_termino=init_time,
         #                   valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=radiation, evapo_t_acum=EVAPOTRANSPIRACION_ACUMULADA, humedad=humedad, temperatura=temperatura, lisimetro=suma_total)
        add_entry(AAAA_MM_DD=year_month_day, State='Iniciando', tiempo_inicio=init_time, tiempo_actual=init_time, tiempo_termino=init_time,
                            valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=radiation, evapo_t_acum=EVAPOTRANSPIRACION_ACUMULADA, humedad=humedad, temperatura=temperatura, lisimetro=suma_total)
        # ingreso al estado de espera de riego
        state_machine.set_state(WaitingState())


class WaitingState(State):
    def __init__(self):
        super().__init__('Waiting')

    def execute(self):
        global year_month_day
        #print("Esperando para regar, por evapotranspiracion o humedad")
        # Revisa cada 60seg el estado de los sensores de humedad
        time.sleep(60)
        # Si pasan >10min, check -> True
        if check_log_time_variable(get_actual_time()):
        #if check_log_time_variable(get_tiempo_actual_csv(year_month_day)):
            Phidget.begin()
            estado_valvula_0 = Phidget.valve0_state
            estado_valvula_1 = Phidget.valve1_state
            estado_humedad_0 = round(Phidget.moist_sensor0(), 3)
            estado_humedad_1 = round(Phidget.moist_sensor1(), 3)
            estado_radiacion = round(Phidget.pyr20_sensor(), 3)
            with open('atmos.json') as json_file:
                data = json.load(json_file)
                humedad = data["Humedad"]
                temperatura = data["Temperatura"]
            json_file.close()
            with open('lisimetro.json') as json2_file:
                lisimetro_meas = json.load(json2_file)
                suma_total=lisimetro_meas["Peso total"]
            json2_file.close()
            Phidget.stop()
            # Si la condicion de humedad se cumple ingresa a estado de riego
            if (estado_humedad_0 < HUMEDAD_MINIMA and estado_humedad_0 > 0.0):
                state_machine.set_state(ActiveState())
            
            elif check_irrigation_time():
                state_machine.set_state(ActiveState())

            else:
                call_time = call_datetime()
                actual_time = call_time[0]
                year_month_day = call_time[1]
                #add_status_log_entry(AAAA_MM_DD=year_month_day, State='EsperandoRiego', tiempo_actual=actual_time, valve0_status=estado_valvula_0,
                 #                    valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=estado_radiacion, humedad=humedad, temperatura=temperatura,lisimetro=suma_total)
                add_entry(AAAA_MM_DD=year_month_day, State='EsperandoRiego', tiempo_actual=actual_time, valve0_status=estado_valvula_0,
                                     valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=estado_radiacion, humedad=humedad, temperatura=temperatura,lisimetro=suma_total)

class ActiveState(State):
    def __init__(self):
        super().__init__('Active')

    def execute(self):
        global year_month_day
        print("Regando.")
        time.sleep(1)  # Wait for 1 second
        call_time = call_datetime()
        before_irrigation_time = call_time[0]
        year_month_day = call_time[1]
        timer = time.time()
        Phidget.begin() # Inicializacion de phidget
        #metodo para valvula 0 (por calendario)
        while (time.time() - timer < TIEMPO_RIEGO):
            Phidget.valve_0(True)
            #calculate the total water added in 30 seconds by the flow sensor
            caudal_0 = round(Phidget.flow_0(), 3)
        print("Finalizando riego")
        estado_valvula_0 = Phidget.valve0_state
        estado_valvula_1 = Phidget.valve1_state

        Phidget.valve_1(False)
        Phidget.valve_0(False)
        # caudal_0 = round(Phidget.flow_0(), 2)
        # caudal_1 = round(Phidget.flow_1(), 2)
        estado_humedad_0 = round(Phidget.moist_sensor0(), 3)
        estado_humedad_1 = round(Phidget.moist_sensor1(), 3)
        after_irrigation = call_datetime()[0]
        estado_radiacion = round(Phidget.pyr20_sensor(), 3)
        Phidget.stop()
        #add_status_log_entry(AAAA_MM_DD=year_month_day, State='Regando', tiempo_inicio=before_irrigation_time, tiempo_actual=call_datetime()[
        #                     0], tiempo_termino=after_irrigation, valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensor_caudal0_value=caudal_0, sensor_caudal1_value=caudal_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=estado_radiacion)
        add_entry(AAAA_MM_DD=year_month_day, State='Regando', tiempo_inicio=before_irrigation_time, tiempo_actual=call_datetime()[
                             0], tiempo_termino=after_irrigation, valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensor_caudal0_value=caudal_0, sensor_caudal1_value=caudal_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1, radiation_voltage=estado_radiacion)
        state_machine.set_state(WaitingState())


# Create an instance of the state machine
state_machine = StateMachine()

# Create instances of the states
init_state = InitState()
waiting_state = WaitingState()
active_state = ActiveState()

# Set the initial state
state_machine.set_state(init_state)

# Run the state machine
state_machine.run()
