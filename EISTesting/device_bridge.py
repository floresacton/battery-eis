import time
import usbtmc

class SigGen:
    sig_gen = None

    def __init__(self):
        print("Connecting signal generator....")
        retries = 10
        while retries > 0:
            try:
                addr = "USB::62700::4355::SDG1XDDQ7R3310::INSTR"
                sig_gen = usbtmc.Instrument(addr)
                print(f"selected dev {addr}")
                self.sig_gen = sig_gen

                self.sig_gen.write("C1:OUTP OFF")
                self.sig_gen.write("C2:OUTP OFF")

                self.sig_gen.write("C1:BSWV WVTP, SINE")
                self.sig_gen.write("C1:BSWV FRQ, 1000")
                self.sig_gen.write("C1:BSWV AMP, .002")

                self.sig_gen.write("C2:BSWV WVTP, SINE")
                self.sig_gen.write("C2:BSWV FRQ, 1000")
                self.sig_gen.write("C2:BSWV AMP, .002")

                return

            except:
                retries -= 1
                time.sleep(.5)
        raise(Exception(f"Failed to connect to signal generator at addr {dev_addr}"))

    def on(self, channel=1):
        if channel == 1:
            self.sig_gen.write("C1:OUTP ON")
        elif channel == 2:
            self.sig_gen.write("C2:OUTP ON")

    def off(self, channel=1):
        if channel == 1:
            self.sig_gen.write("C1:OUTP OFF")
        elif channel == 2:
            self.sig_gen.write("C2:OUTP OFF")

    def set_freq(self, freq, channel=1):
        if channel == 1:
            self.sig_gen.write(f"C1:BSWV FRQ, {freq}")
        elif channel == 2:
            self.sig_gen.write(f"C2:BSWV FRQ, {freq}")

    def set_amp(self, amp, channel=1):
        # amp in volts
        if channel == 1:
            self.sig_gen.write(f"C1:BSWV AMP, {amp}")
        elif channel == 2:
            self.sig_gen.write(f"C2:BSWV AMP, {amp}")
   
    def set_DC_mode(self, channel=1):
        if channel == 1:
            self.sig_gen.write("C1:BSWV WVTP, DC")
        elif channel == 2:
            self.sig_gen.write("C2:BSWV WVTP, DC")

    def set_sine_mode(self, channel=1):
        if channel == 1:
            self.sig_gen.write("C1:BSWV WVTP, SINE")
        elif channel == 2:
            self.sig_gen.write("C2:BSWV WVTP, SINE:")

    def set_voltage(self, offset, channel=1):
        if channel == 1:
            self.sig_gen.write(f"C1:BSWV OFST, {offset}")
        elif channel == 2:
            self.sig_gen.write(f"C2:BSWV OFST, {offset}")


if __name__ == "__main__":
    sg = SigGen()


class Scope:

    def __init__(self):
        print("Connecting to Oscilloscope...")
        retries = 10
        while retries > 0:
            try:
                addrs = usbtmc.list_resources()
                osc_addr = "USB::1689::932::C030786::INSTR"
                assert osc_addr in addrs, "no scope"
                osc = usbtmc.Instrument(osc_addr)
                print("USBTMC list resources: ", end='')
                print(addrs)
                print("OSC address: ", end='')
                print(osc_addr)
                print(osc.ask("*IDN?"))

                return

            except:
                retries -= 1
                time.sleep(.5)
        raise(Exception(f"Failed to connect to signal generator at addr {dev_addr}"))

#    def on(self, channel=1):
#        if channel == 1:
#            self.sig_gen.write("C1:OUTP ON")
#        elif channel == 2:
#            self.sig_gen.write("C2:OUTP ON")
#
#    def off(self, channel=1):
#        if channel == 1:
#            self.sig_gen.write("C1:OUTP OFF")
#        elif channel == 2:
#            self.sig_gen.write("C2:OUTP OFF")
#
#    def set_freq(self, freq, channel=1):
#        if channel == 1:
#            self.sig_gen.write(f"C1:BSWV FRQ, {freq}")
#        elif channel == 2:
#            self.sig_gen.write(f"C2:BSWV FRQ, {freq}")
#
#    def set_amp(self, amp, channel=1):
#        # amp in volts
#        if channel == 1:
#            self.sig_gen.write(f"C1:BSWV AMP, {amp}")
#        elif channel == 2:
#            self.sig_gen.write(f"C2:BSWV AMP, {amp}")
#


