import time
from time_zone_request import call_datetime, check_log_time_variable
from logger import add_status_log_entry, get_tiempo_actual_csv

#from phidget_simple import Simple_Phidget #RPI
from mock_class import Simple_Phidget #PC

#Valores corte
HUMEDAD_MINIMA = 3.13


Phidget = Simple_Phidget()
Phidget.begin()

class StateMachine:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def run(self):
        while True:
            if self.state is not None:
                self.state.execute()
            elif self.state is None:
                print("None state")
                time.sleep(10)
            else:
                break

class State:
    def __init__(self, name):
        self.name = name

    def execute(self):
        pass

class InitState(State):
    def __init__(self):
        super().__init__('Init')
        

    def execute(self):
        print("Iniciando sistema de riego.")
        time.sleep(1)  # Wait for 1 second
        init_time = ''
        init_time = call_datetime()[0]
        estado_valvula_0 = Phidget.valve0_state
        estado_valvula_1 = Phidget.valve1_state
        estado_humedad_0 = round(Phidget.moist_sensor(),2)
        estado_humedad_1 = round(Phidget.moist_sensor(),2)
        add_status_log_entry(State= 'Iniciando',tiempo_inicio=init_time, tiempo_actual= init_time , tiempo_termino=init_time, valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1)
        state_machine.set_state(WaitingState())


class WaitingState(State):
    def __init__(self):
        super().__init__('Waiting')

    def execute(self):
        print("Esperando para regar, por evapotranspiracion o humedad")
        time.sleep(60)  # Wait for 60 seconds
        estado_valvula_0 = Phidget.valve0_state
        estado_valvula_1 = Phidget.valve1_state
        estado_humedad_0 = round(Phidget.moist_sensor(),2)
        estado_humedad_1 = round(Phidget.moist_sensor(),2)
        
        if check_log_time_variable(get_tiempo_actual_csv()):
            if (estado_humedad_0 < HUMEDAD_MINIMA):
                state_machine.set_state(ActiveState())

            else:
                add_status_log_entry(State= 'EsperandoRiego', tiempo_actual=call_datetime()[0], valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1)


                
        

class ActiveState(State):
    def __init__(self):
        super().__init__('Active')

    def execute(self):
        print("Regando.")
        time.sleep(1)  # Wait for 1 second
        before_irrigation = call_datetime()[0]
        timer = time.time()
        
        
        while (time.time() - timer < 30.0):
            
            Phidget.valve_1(True)
            Phidget.valve_0(True)
        
        print("Finalizando riego")
        estado_valvula_0 = Phidget.valve0_state
        estado_valvula_1 = Phidget.valve1_state
        
        Phidget.valve_1(False)
        Phidget.valve_0(False)
            
        estado_humedad_0 = round(Phidget.moist_sensor(),2)
        estado_humedad_1 = round(Phidget.moist_sensor(),2)
        after_irrigation = call_datetime()[0]  
        add_status_log_entry(State= 'Regando', tiempo_inicio=before_irrigation,tiempo_actual=call_datetime()[0], tiempo_termino=after_irrigation, valve0_status=estado_valvula_0, valve1_status=estado_valvula_1, sensormoist0_value=estado_humedad_0, sensormoist1_value=estado_humedad_1)
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