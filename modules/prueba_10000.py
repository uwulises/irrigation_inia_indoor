from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()
Phidget.begin()

inicio = True
humedad_baja = 3.2173
humedad_alta = 

while inicio == True
    

print("Abriendo valvulas")    
Phidget.valve_1(True)
Phidget.valve_0(True)
time.sleep(10)

print("Cerrando valvulas")
Phidget.valve_1(False)
Phidget.valve_0(False)
time.sleep(10)