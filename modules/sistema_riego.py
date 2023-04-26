import sys
sys.path.append('/home/inia/.local/lib/python3.9/site-packages')

from indoor_class import Simple_Phidget
import time

Phidget = Simple_Phidget()

Hora_actual = time.strftime("%H:%M:%S")

hora_riego_1 = "09:30:00"
hora_riego_2 = "16:30:00"
tiempo_riego = 60*7
humedad_bajo = 3.16
humedad_alto = 3.172

Phidget.begin()

inicio = True
se_paso_el_riego_1 = False
se_paso_el_riego_2 = False

with open("datos_riego.txt", "a") as f:

    f.write("\nEL programa hace inicio a las: {} \n \n".format(Hora_actual))

while inicio == True:

    with open("datos_riego.txt", "a") as f:
        
        Humedad = float(Phidget.moist_sensor())
        Hora_actual = time.strftime("%H:%M:%S")

        if Humedad < humedad_bajo:

            i = 0
            lado = "izquierdo"
            f.write("Iniciando riego en lado {} \n".format(lado))
            f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
            f.write("Abriendo Válvula de lado {} \n \n".format(lado))
            Phidget.valve_1(True)

            while Humedad < humedad_alto:
                        
                Hora_actual = time.strftime("%H:%M:%S")
                Caudal = float(Phidget.flow_1())
                Humedad = float(Phidget.moist_sensor())
                f.write("Hora: {}, Caudal: {}, Humedad: {}\n".format(Hora_actual, Caudal, Humedad))
                
                if Hora_actual == hora_riego_1:
                    se_paso_el_riego_1 = True
                if Hora_actual == hora_riego_2:
                    se_paso_el_riego_2 = True

                time.sleep(1)
                i = i + 1

            Hora_actual = time.strftime("%H:%M:%S")
            f.write(" \nFinalizando riego en lado {} \n".format(lado))
            f.write("Hora de finalización de riego: {}, se regó durante {} segundos\n".format(Hora_actual, i))
            f.write("Cerrando Válvula de lado {} \n \n".format(lado))
            Phidget.valve_1(False)

        if Hora_actual == hora_riego_1 or se_paso_el_riego_1 == True:
            lado = "derecho"
            i = 0
            f.write("Iniciando riego en lado {} \n".format(lado))
            f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
            f.write("Abriendo Válvula de lado {} \n".format(lado))
            Phidget.valve_0(True)

            while i < tiempo_riego:

                Hora_actual = time.strftime("%H:%M:%S")
                Caudal = float(Phidget.flow_0())
                f.write("Hora: {}, Caudal: {}\n".format(Hora_actual, Caudal))
                time.sleep(1)
                i = i + 1

            Hora_actual = time.strftime("%H:%M:%S")
            f.write("\nFinalizando riego en lado {} \n".format(lado))
            f.write("Hora de finalización de riego: {} \n".format(Hora_actual))
            f.write("Cerrando Válvula de lado {} \n\n".format(lado))
            Phidget.valve_0(False)

            se_paso_el_riego_1 = False

        if Hora_actual == hora_riego_2 or se_paso_el_riego_2 == True:
            lado = "derecho"
            i = 0
            f.write("Iniciando riego en lado {} \n".format(lado))
            f.write("Hora de inicio de riego: {} \n".format(Hora_actual))
            f.write("Abriendo Válvula de lado {} \n".format(lado))
            Phidget.valve_0(True)

            while i < tiempo_riego:

                Hora_actual = time.strftime("%H:%M:%S")
                Caudal = float(Phidget.flow_0())
                f.write("Hora: {}, Caudal: {}\n".format(Hora_actual, Caudal))
                time.sleep(1)
                i = i + 1

            Hora_actual = time.strftime("%H:%M:%S")
            f.write("\nFinalizando riego en lado {} \n".format(lado))
            f.write("Hora de finalización de riego: {} \n".format(Hora_actual))
            f.write("Cerrando Válvula de lado {} \n\n".format(lado))
            Phidget.valve_0(False)
            
            se_paso_el_riego_2 = False

        time.sleep(1)
