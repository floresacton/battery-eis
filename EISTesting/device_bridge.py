import time
import usbtmc

class SigGen:
    sig_gen = None

    def __init__(self):
        print("Connecting signal generator")
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

if __name__ == "__main__":
    sg = SigGen()
