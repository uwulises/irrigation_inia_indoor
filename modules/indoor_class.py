import time
import sys
import os
#append phidget library folder
sys.path.insert(0, os.path.abspath('../lib'))
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *





class Simple_Phidget:
    def __init__(self, valve0_state=False, valve1_state=False):
        self.valve0_state = valve0_state
        self.valve1_state = valve1_state
        #Create your Phidget channels
        self.relay_out0 = DigitalOutput()
        self.relay_out1 = DigitalOutput()
        #Set addressing parameters to specify which channel to open (if any)
        self.relay_out0.setChannel(0)
        self.relay_out1.setChannel(1)
        #Open your Phidgets and wait for attachment
        self.relay_out0.openWaitForAttachment(5000)
        self.relay_out1.openWaitForAttachment(5000)
        

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

    def begin(self):
        self.valve_0(False)
        self.valve_1(False)
        print("BEGIN")
        time.sleep(2)

        

    