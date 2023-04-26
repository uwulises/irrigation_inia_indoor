from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()
Phidget.begin()

Hora_actual = time.strftime("%H:%M:%S")
i = 0
a = True
humedad_cambio= 3.196

while a ==True:
    variable = False
    Humedad = float(Phidget.moist_sensor())
    if Humedad <= humedad_cambio:
        print("\n Humedad baja, abriendo válvulas \n")
        time.sleep(1)
        Phidget.valve_0(True)
        Phidget.valve_1(True)
        while Humedad <= humedad_cambio:
            Humedad = float(Phidget.moist_sensor())
            Hora_actual = time.strftime("%H:%M:%S")
            print("Hora: {} Humedad: {}\n".format(Hora_actual, Humedad))
            time.sleep(1)    
    if Humedad > humedad_cambio:
        print("\n Humedad alta, cerrando válvulas \n")
        time.sleep(1)
        Phidget.valve_0(False)
        Phidget.valve_1(False)
        while Humedad > humedad_cambio:
            Humedad = float(Phidget.moist_sensor())
            Hora_actual = time.strftime("%H:%M:%S")
            print("Hora: {} Humedad: {}\n".format(Hora_actual, Humedad))
            time.sleep(1)          

