from phidget_simple import SimplePhidget
import time

Phidget = SimplePhidget()

def main():
    Phidget.begin()
    print("Abriendo valvulas")    
    Phidget.valve_0(True)
    time.sleep(420)
    Phidget.valve_0(False)
    time.sleep(2)
    Phidget.stop()
    print("STOP")

main()