from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()

def main():
    i=0
    while i<60:
        print(Phidget.moist_sensor())
        time.sleep(0.5)
        i=i+1
    Phidget.stop()
    print("STOP")
main()