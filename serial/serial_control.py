from serial import Serial
import time

class SerialControl:

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.port = port
        self.serial = None
        self.baudrate = baudrate
    def open_serial(self):
        try:
            self.serial = Serial(
                self.port, self.baudrate, timeout=1, write_timeout=0.1)
            print("The port is available")
            serial_port = "Open"
            time.sleep(2)
        except self.serial.serialutil.SerialException:
            print("The port is at use")
            self.serial.close()
            self.serial.open()

    def close_serial(self):
        time.sleep(0.2)
        self.serial.close()
    def read(self):
        return self.serial.readlines().decode().strip()

    # Send a command to the Arduino
    def send_command(self, cmd=""):
        # Match case structure to send the right command to arduino
        msg= str(cmd)
        self.serial.write(msg.encode())