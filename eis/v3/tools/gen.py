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

    def set_freq(self, freq, chan):
        self.gen.write(f"C{chan}:BSWV FRQ, {freq}")

    def set_amplitude(self, chan, amplitude):
        # amp in volts
        self.gen.write(f"C{chan}:BSWV AMP, {amplitude}")

    def set_offset(self, chan, offset):
        self.gen.write(f"C{chan}:BSWV OFST, {offset}")