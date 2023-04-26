from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()
Phidget.begin()

Hora_actual = time.strftime("%H:%M:%S")
i = 0 
tiempo_prueba = 60*7
Humedad = float(Phidget.moist_sensor())
Caudal = float(Phidget.flow_0())

with open("datos_riego_prueba.txt", "a") as f:

    lado = "derecho"
    f.write("\nEL programa de riego de pureba hace inicio a las: {} \n \n".format(Hora_actual))
    f.write("Iniciando riego de prueba en lado {} \n".format(lado))
    f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
    f.write("Datos iniciales de riego: Humedad: {} Caudal: {}\n".format(Humedad, Caudal))
    f.write("Abriendo Válvula de lado {} \n \n".format(lado))
    time.sleep(5)
    Phidget.valve_0(True)

while i < tiempo_prueba:
    with open("calculos_humedad_caudal.txt", "a") as f:
        Humedad = float(Phidget.moist_sensor())
        Caudal = float(Phidget.flow_0())
        Hora_actual = time.strftime("%H:%M:%S")
        print("Hora: {}  Humedad: {} Caudal: {}\n".format(Hora_actual, Humedad, Caudal))
        f.write("Hora: {}  Humedad: {} Caudal: {}\n".format(Hora_actual, Humedad, Caudal))
        time.sleep(5)
        i = i+5

with open("datos_riego_prueba.txt", "a") as f:

    f.write("\nCerrando Válvula de lado {} \n ".format(lado))
    Phidget.valve_0(False)

    f.write("Finalizando riego de prueba en lado {} \n".format(lado))
    
    Hora_actual = time.strftime("%H:%M:%S")
    f.write("Hora de finalización de riego: {} \n".format(Hora_actual))