from phidget_simple import SimplePhidget
import time

Phidget = SimplePhidget()

def main():
    Phidget.begin()
    print("Abriendo valvulas")    
    Phidget.valve_1(True)
    Phidget.valve_0(True)
    time.sleep(2)
    i=0
    while i<60:
        print("Moist 0 sensor value: {}".format(Phidget.moist_sensor0()))
        print("Moist 1 sensor value: {}".format(Phidget.moist_sensor1()))
        print("Flow 0 sensor value: {}".format(Phidget.flow_0()))
        print("Flow 1 sensor value: {}".format(Phidget.flow_1()))
        print("Estado valvula 0 (False close; True open): {}".format(Phidget.valve0_state))
        print("Estado valvula 1 (False close; True open): {}".format(Phidget.valve1_state))
        time.sleep(1)
        i=i+1
    
    Phidget.valve_1(False)
    Phidget.valve_0(False)
    time.sleep(2)

    Phidget.stop()
    print("STOP")


main()



