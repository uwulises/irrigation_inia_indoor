import time
from time_zone_request import call_datetime, check_log_time_variable
from logger import add_status_log_entry, get_tiempo_actual_csv

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
        add_status_log_entry(State= 'Iniciando',tiempo_inicio=init_time, tiempo_actual= init_time , tiempo_termino=init_time)
        state_machine.set_state(WaitingState())


class WaitingState(State):
    def __init__(self):
        super().__init__('Waiting')

    def execute(self):
        print("Esperando para regar, por evapotranspiracion o humedad")
        time.sleep(10)  # Wait for 10 seconds
        
        while check_log_time_variable(get_tiempo_actual_csv()):
            
            add_status_log_entry(State= 'EsperandoRiego', tiempo_actual=call_datetime()[0])
            state_machine.set_state(ActiveState())
        

class ActiveState(State):
    def __init__(self):
        super().__init__('Active')

    def execute(self):
        print("Regando.")
        time.sleep(1)  # Wait for 1 second
        before_irrigation = call_datetime()[0]
        timer = time.time()
        while (time.time() - timer < 30.0):
            print("Regando {}".format(time.time() - timer))
            

        after_irrigation = call_datetime()[0]  
        add_status_log_entry(State= 'Regando', tiempo_inicio=before_irrigation,tiempo_actual=call_datetime()[0], tiempo_termino=after_irrigation)
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
