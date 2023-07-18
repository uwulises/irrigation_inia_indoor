#This class only print stuff

import time
import random

   
class sensor:
    def __init__(self):
        self.status = 0

    def getVoltage(self):
        return random.random()

    def close(self):
        self.status = 0
        return 0

class Simple_Phidget:
    def __init__(self, valve0_state=False, valve1_state=False):
        self.valve0_state = valve0_state
        self.valve1_state = valve1_state

        #Sensores
        self.moist0 = sensor()
        self.moist1 = sensor()
        self.flow0 = sensor()
        self.flow1 = sensor()
        self.thermopile = sensor()
        self.anemometer = sensor()
        
    def valve_0(self, valve0_state):
        if valve0_state:
            self.valve0_state=True

        else:
            self.valve0_state=False


    def valve_1(self, valve1_state):
        if valve1_state:
            self.valve1_state=True

        else:
            self.valve1_state=False


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
