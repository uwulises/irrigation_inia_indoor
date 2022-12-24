import time
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import DigitalOutput
from Phidget22.Devices.VoltageInput import VoltageInput


class Simple_Phidget:
    def __init__(self, valve0_state=False, valve1_state=False):
        self.valve0_state = valve0_state
        self.valve1_state = valve1_state
        
        #Create your Phidget channels
        
        #Actuadores digitales
        self.relay_out0 = DigitalOutput()
        self.relay_out1 = DigitalOutput()

        #Sensores
        self.moist0 = VoltageInput()
        self.flow0 = VoltageInput()
        self.flow1 = VoltageInput()
        self.thermopile = VoltageInput()
        self.anemometer = VoltageInput()
        
        #Canal de actuadores
        self.relay_out0.setChannel(0) #Rele 0 en Digital Output 0
        self.relay_out1.setChannel(1) #Rele 1 en Digital Output 1

        #Canal de sensores            
        self.flow0.setChannel(1) #Sensor de flujo 0 en Analog Input 1
        self.flow1.setChannel(2) #Sensor de flujo 1 en Analog Input 2
        self.thermopile.setChannel(3) #Piranometro en Analog Input 3
        self.anemometer.setChannel(4) #Anemometro en Analog Input 4
        self.moist0.setChannel(7) #Sensor humedad en Analog Input 7

        #Open your Phidgets and wait for attachment
        self.relay_out0.openWaitForAttachment(5000)
        self.relay_out1.openWaitForAttachment(5000)
        self.moist0.openWaitForAttachment(5000)
        self.flow0.openWaitForAttachment(5000)
        self.flow1.openWaitForAttachment(5000)
        self.thermopile.openWaitForAttachment(5000)
        self.anemometer.openWaitForAttachment(5000)

    def valve_0(self, valve0_state):
        if valve0_state:
            self.valve0_state=True
            self.relay_out0.setDutyCycle(0)

        else:
            self.valve0_state=False
            self.relay_out0.setDutyCycle(1)

    def valve_1(self, valve1_state):
        if valve1_state:
            self.valve1_state=True
            self.relay_out1.setDutyCycle(0)
        else:
            self.valve1_state=False
            self.relay_out1.setDutyCycle(1)

    def moist_sensor(self):
        return self.moist0.getVoltage()

    def flow_0(self):
        return self.flow0.getVoltage()

    def flow_1(self):
        return self.flow1.getVoltage()

    def thermopile_sensor(self):
        return self.thermopile.getVoltage()

    def anemometer_sensor(self):
        return self.anemometer.getVoltage()

    def begin(self):
        self.valve_0(False)
        self.valve_1(False)
        print("Valvulas Cerradas para comenzar")
        time.sleep(2)

    def stop(self):
        self.moist0.close()
        self.flow0.close()
        self.flow1.close()
        self.relay_out0.close()
        self.relay_out1.close()
        self.thermopile.close()
        self.anemometer.close()
