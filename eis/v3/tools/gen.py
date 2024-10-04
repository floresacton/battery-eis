import time

import usbtmc


class Gen:
    def __init__(self, addr):
        self.gen = usbtmc.Instrument(addr)

    def set_enable(self, chan, state):
        self.gen.write(f"C{chan}:OUTP {"ON" if state else "OFF"}")

    def set_mode(self, chan, mode):
        # SINE, DC
        self.gen.write(f"C{chan}:BSWV WVTP, {mode}")

    def set_freq(self, chan, freq):
        self.gen.write(f"C{chan}:BSWV FRQ, {float(freq):.9}")

    def set_amplitude(self, chan, amplitude):
        # amplitude in volts
        self.gen.write(f"C{chan}:BSWV AMP, {float(amplitude):.5}")

    def set_offset(self, chan, offset):
        self.gen.write(f"C{chan}:BSWV OFST, {float(offset):.4}")