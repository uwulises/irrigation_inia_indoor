from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()

def main():
    Phidget.begin()
    time.sleep(2)
    print("Estado valvulas")
    print(Phidget.valve0_state)
    print(Phidget.valve1_state)
    time.sleep(1)
    print("Encendiendo valvulas")
    Phidget.valve_1(True)
    Phidget.valve_0(True)
    time.sleep(4)
    print("Apagando valvulas")
    Phidget.valve_1(False)
    Phidget.valve_0(False)
    time.sleep(10)
main()



