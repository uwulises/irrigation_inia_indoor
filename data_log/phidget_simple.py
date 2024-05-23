import time
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import DigitalOutput
from Phidget22.Devices.VoltageInput import VoltageInput

'''
Clase de PhidgetInterfaceKit 8/8/8 w/6 Port Hub, de forma simplificada se utilizan
dos (2) reles como actuadores para valvulas de apertura de flujo
dos (2) entradas de voltaje analogo para sensado de humedad de suelo
dos (2) entradas de voltaje analogo para sensado de caudal
una (1) entrada de voltaje analogo para sensado de temperatura
una (1) entrada de voltaje analogo para sensado de velocidad del viento
una (1) entrada de voltaje analogo para sensado de radiacion solar (0-2V)
'''
class SimplePhidget:
    def __init__(self, valve0_state=False, valve1_state=False):
        self.valve0_state = valve0_state
        self.valve1_state = valve1_state
        
        #Create your Phidget channels
        
        #Actuadores digitales
        self.relay_out0 = DigitalOutput()
        self.relay_out1 = DigitalOutput()

        #Sensores
        self.moist0 = VoltageInput()
        self.moist1 = VoltageInput()
        self.flow0 = VoltageInput()
        self.flow1 = VoltageInput()
        self.thermopile = VoltageInput()
        self.anemometer = VoltageInput()
        self.pyr20 = VoltageInput()
        
        #Canal de actuadores
        self.relay_out0.setChannel(0) #Rele 0 en Digital Output 0
        self.relay_out1.setChannel(1) #Rele 1 en Digital Output 1

        #Canal de sensores            
        self.flow0.setChannel(1) #Sensor de flujo 0 en Analog Input 1
        self.flow1.setChannel(2) #Sensor de flujo 1 en Analog Input 2
        self.thermopile.setChannel(3) #Piranometro en Analog Input 3
        self.anemometer.setChannel(4) #Anemometro en Analog Input 4
        self.pyr20.setChannel(5) #Sensor de radiacion solar en Analog Input 5
        self.moist0.setChannel(6) #Sensor humedad en Analog Input 6
        self.moist1.setChannel(7) #Sensor humedad en Analog Input 7

        #Open your Phidgets and wait for attachment
        self.relay_out0.openWaitForAttachment(5000)
        self.relay_out1.openWaitForAttachment(5000)
        self.moist0.openWaitForAttachment(5000)
        self.moist1.openWaitForAttachment(5000)
        self.flow0.openWaitForAttachment(5000)
        self.flow1.openWaitForAttachment(5000)
        self.thermopile.openWaitForAttachment(5000)
        self.anemometer.openWaitForAttachment(5000)
        self.pyr20.openWaitForAttachment(5000)

    def valve_0(self, valve0_state):
        if valve0_state:
            self.valve0_state=True
            self.relay_out0.setDutyCycle(1)

        else:
            self.valve0_state=False
            self.relay_out0.setDutyCycle(0)

    def valve_1(self, valve1_state):
        if valve1_state:
            self.valve1_state=True
            self.relay_out1.setDutyCycle(1)
        else:
            self.valve1_state=False
            self.relay_out1.setDutyCycle(0)

    def moist_sensor0(self):
        return self.moist0.getVoltage()
    
    def moist_sensor1(self):
        return self.moist1.getVoltage()

    def flow_0(self):
        return self.flow0.getVoltage()

    def flow_1(self):
        return self.flow1.getVoltage()

    def thermopile_sensor(self):
        return self.thermopile.getVoltage()

    def anemometer_sensor(self):
        return self.anemometer.getVoltage()
    
    def pyr20_sensor(self):
        return self.pyr20.getVoltage()

    def begin(self):
        self.valve_0(False)
        self.valve_1(False)
        print("Valvulas Cerradas para comenzar")
        time.sleep(2)

    def stop(self):
        self.moist0.close()
        self.moist1.close()
        self.flow0.close()
        self.flow1.close()
        self.relay_out0.close()
        self.relay_out1.close()
        self.thermopile.close()
        self.anemometer.close()
        self.pyr20.close()
