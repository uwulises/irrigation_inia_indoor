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

print("\n Esta es una prueba de error\nSe encenderán ambas válvulas y se irá cerrando la una u la otra para observar qué ocurre\n\n")

print("Datos iniciales, Caudal izq: {}, Caudal der: {}".format(Caudal_i, Caudal_d))

print("Abriendo válvulas \n\n")
time.sleep(3)
Phidget.valve_1(True)
Phidget.valve_0(True)
time.sleep(5)
print("Cerrando válvula derecha 20 segundos \n\n")
Phidget.valve_0(False)

while i < tiempo_prueba:
    Caudal_i = float(Phidget.flow_1())
    Caudal_d = float(Phidget.flow_0())
    i = i+1
    print("Segundo: {} Caudal izq: {} Caudal der: {}\n".format(i, Caudal_i, Caudal_d))
    time.sleep(1)
i = 0

print("n Abriendo válvula derecha y cerrando la izquierda por 20 segundos\n\n")
Phidget.valve_0(True)
Phidget.valve_1(False)

while i < tiempo_prueba:
    Caudal_i = float(Phidget.flow_1())
    Caudal_d = float(Phidget.flow_0())
    i = i+1
    print("Segundo: {} Caudal izq: {} Caudal der: {}\n".format(i, Caudal_i, Caudal_d))
    time.sleep(1)

i = 0
print("\nCerrando todo\n\n")
Phidget.valve_0(False)
Phidget.valve_1(False)