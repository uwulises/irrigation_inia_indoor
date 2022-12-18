from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()

def main():
    Phidget.begin()
    print("Abriendo valvulas")    
    Phidget.valve_1(True)
    Phidget.valve_0(True)
    time.sleep(2)
    print("Cerrando valvulas")
    Phidget.valve_1(False)
    Phidget.valve_0(False)
    time.sleep(2)
    print("Calling moist sensor")
    i=0
    while i<20:
        print("Moist 0 sensor value: {}".format(Phidget.moist_sensor()))
        print("Flow 0 sensor value: {}".format(Phidget.flow_0()))
        print("Flow 1 sensor value: {}".format(Phidget.flow_1()))
        print("Estado valvula 0 (False close; True open): {}".format(Phidget.valve0_state))
        print("Estado valvula 0 (False close; True open): {}".format(Phidget.valve1_state))
        time.sleep(0.2)
        i=i+1
    Phidget.stop()
    print("STOP")
main()



