import usbtmc


class Supply():

    def __init__(self, addr):
        self.supply = usbtmc.Instrument(addr)

    def set_enable(self, chan, state):
        self.supply.write(f"OUTP CH{chan},{'ON' if state else 'OFF'}")
    
    def set_voltage(self, chan, voltage):
        self.supply.write(f"CH{chan}:VOLT {voltage:.6}")
    
    def set_current(self, chan, current):
        self.supply.write(f"CH{chan}:CURR {current:.6}")

    def get_voltage(self, chan):
        # return setpoint
        return self.supply.ask(f"CH{chan}:VOLT?")

    def get_current(self, chan):
        # return setpoint
        return self.supply.ask(f"CH{chan}:CURR?")
    
    def measure_voltage(self, chan):
        return self.supply.ask(f"MEAS:VOLT? CH{chan}")

    def measure_current(self, chan):
        return self.supply.ask(f"MEAS:CURR? CH{chan}")

    def measure_power(self, chan):
        return self.supply.ask(f"MEAS:POWE? CH{chan}")