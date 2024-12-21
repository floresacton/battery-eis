import time

import pyvisa


class Load:
    def __init__(self, address):
        self.addr = address
        self.load = pyvisa.ResourceManager().open_resource(self.addr)

        # enable remote sensing
        self.load.write("SYST:SENS:STAT OFF")

        # configure load
        self.load.write(":SOUR:CURR:IRANG 30")
        self.load.write(":SOUR:CURR:VRANG 36")

        self.load.write("SOUR:CURR:SLEW:POS 2.5")
        self.load.write("SOUR:CURR:SLEW:NEG 2.5")

    def set_enable(self, state):
        self.load.write(f":INP {state}")
    
    # CURR or VOLT
    def set_mode(self, mode):
        self.load.write(f":SOUR:FUNC {mode}")

    def set_voltage(self, voltage):
        self.load.write(f":VOLT {voltage}")

    def set_current(self, current):
        self.load.write(f":CURR {current}")

    def measure_voltage(self):
        return float(self.load.query("MEAS:VOLT?"))

    def measure_current(self):
        return float(self.load.query("MEAS:CURR?"))