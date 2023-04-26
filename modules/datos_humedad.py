from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()
Phidget.begin()

inicio = True 


while inicio == True:
    with open("datos_humedad_prueba.txt", "a") as f:
        Humedad = float(Phidget.moist_sensor())
        Hora_actual = time.strftime("%H:%M:%S")
        print("Hora: {}  Humedad: {}\n".format(Hora_actual, Humedad))
        f.write("Hora: {}  Humedad: {}\n".format(Hora_actual, Humedad))
        time.sleep(5)
