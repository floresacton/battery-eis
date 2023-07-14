import time
import pyvisa

ip_load = "10.42.0.78"

ip_supply = "10.42.0.46"

rm = pyvisa.ResourceManager()

def instr_address(ip):
    return f"TCPIP::{ip}::INSTR"

class Load:
    load = None

    def __init__(self):
        print("Connecting load")
        retries = 10
        while retries > 0:
            try:
                dev_addr = instr_address(ip_load)
                load = rm.open_resource(dev_addr)
                self.load = load

                self.load.write(":INP 0")

                # CC mode
                self.load.write(":SOURce:FUNCtion CURRent")

                # enable remote sensing
                self.load.write("SYSTem:SENSe:STATe ON")

                # configure load
                self.load.write(":SOURce:CURRent:VRANGe 36")
                self.load.write(":SOURce:CURRent:IRANGe 30")

                self.load.write("SOURce:CURRent:SLEW:POSitive 2.5")
                self.load.write("SOURce:CURRent:SLEW:NEGative 2.5")

                # zero
                self.set_I(0)

                return

            except:
                retries -= 1
                time.sleep(.5)
        raise(f"Failed to connect to DC load at addr {dev_addr}")

    def meas_V(self):
        return float(self.load.query("MEAS:VOLT?"))

    def meas_I(self):
        return float(self.load.query("MEAS:CURR?"))

    def set_I(self, I=0):
        self.load.write(f":CURR {I}")

    def on(self):
        self.load.write(":INP 1")

    def off(self):
        self.load.write(":INP 0")

class Supply:
    supply = None
    
    # empirically measured that CH2 lags behind CH1 by constant 34 mA
    ch2_offset_current = 0.034 # Amps 
    
    def __init__(self):
        print("Connecting supply")
        retries = 10
        while retries > 0:
            try:
                dev_addr = instr_address(ip_supply)
                supply = rm.open_resource(dev_addr)
                self.supply = supply

                # enable parallel supply mode
                self.supply.write("OUTPut:TRACK 2")

                # configure supply
                self.supply.write("OUTP CH1,OFF")
                self.supply.write("OUTP CH2,OFF")
                self.supply.write("OUTP CH3,OFF")

                # zero
                self.set_I(0)
                self.set_V(0)

                return
            except:
                retries -= 1
                time.sleep(.5)
        raise(f"Failed to connect to power supply at addr {dev_addr}")

    def on(self):
        self.supply.write("OUTP CH1,ON")
        self.supply.write("OUTP CH2,ON")

        # ch3 always disabled for cell testing
        self.supply.write("OUTP CH3,OFF")

    def off(self):
        self.supply.write("OUTP CH1,OFF")
        self.supply.write("OUTP CH2,OFF")
        self.supply.write("OUTP CH3,OFF")

    def set_V(self, V):
        self.supply.write(f"CH1:VOLT {V}")
        self.supply.write(f"CH2:VOLT {V}")
    
    def get_V_set(self):
        return float(self.supply.query("CH1:VOLTage?"))

    def set_I(self, I):
        self.supply.write(f"CH1:CURR {I/2}")
        self.supply.write(f"CH2:CURR {I/2}")
    
    def meas_V(self):
        V1 = float(self.supply.query("MEASure:VOLTage? CH1"))
        V2 = float(self.supply.query("MEASure:VOLTage? CH2"))
        return (V1, V2)

    def meas_I(self):
        I1 = float(self.supply.query("MEASure:CURRent? CH1"))
        I2 = float(self.supply.query("MEASure:CURRent? CH2"))
        return (I1, I2)




