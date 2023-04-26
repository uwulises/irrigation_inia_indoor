from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()
Phidget.begin()

Hora_actual = time.strftime("%H:%M:%S")
Caudal_i = float(Phidget.flow_1())
Caudal_d = float(Phidget.flow_0())
Humedad = float(Phidget.moist_sensor())

tiempo_prueba = 20
i = 0 


with open("datos_riego_prueba_valvulas.txt", "a") as f:

    lado = "izquierdo"
    f.write("EL programa de riego de prueba hace inicio a las: {} \n".format(Hora_actual))
    f.write("Condiciones iniciales: Humedad: {} Caudal izq: {} Caudal der: {}\n \n".format(Humedad, Caudal_i, Caudal_d))
    f.write("Iniciando riego de prueba en lado {} por {} segundos \n".format(lado, tiempo_prueba))
    f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
    f.write("Abriendo Válvula de lado {} \n \n".format(lado))
    time.sleep(5)
    Phidget.valve_1(True)

    while i < tiempo_prueba:
        Hora_actual = time.strftime("%H:%M:%S")
        Caudal_i = float(Phidget.flow_1())
        Caudal_d = float(Phidget.flow_0())
        Humedad = float(Phidget.moist_sensor())
        f.write("Hora: {}, Caudal izq: {}, Caudal der: {} Humedad: {}\n".format(Hora_actual, Caudal_i, Caudal_d, Humedad))
        time.sleep(1)
        i = i+1


    f.write(" \n Cerrando Válvula de lado {} \n".format(lado))
    Phidget.valve_1(False)

    f.write("Finalizando riego de prueba en lado {} \n".format(lado))
    
    Hora_actual = time.strftime("%H:%M:%S")
    f.write("Hora de finalización de riego: {} \n".format(Hora_actual))
    i = 0
    lado = "derecho"
    f.write("Iniciando riego de prueba en lado {} por {} segundos \n".format(lado, tiempo_prueba))
    f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
    f.write("Abriendo Válvula de lado {} \n \n".format(lado))
    time.sleep(20)
    Phidget.valve_0(True)

    while i < tiempo_prueba:
        Hora_actual = time.strftime("%H:%M:%S")
        Caudal_i = float(Phidget.flow_1())
        Caudal_d = float(Phidget.flow_0())
        Humedad = float(Phidget.moist_sensor())
        f.write("Hora: {}, Caudal izq: {}, Caudal der: {} Humedad: {}\n".format(Hora_actual, Caudal_i, Caudal_d, Humedad))
        time.sleep(1)
        i = i+1

    f.write(" \n Cerrando Válvula de lado {} \n".format(lado))
    Phidget.valve_0(False)

    f.write("Finalizando riego de prueba en lado {} \n".format(lado))
    Hora_actual = time.strftime("%H:%M:%S")
    f.write("Hora de finalización de riego: {} \n".format(Hora_actual))
