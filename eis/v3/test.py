import time

from plotter import plot
from scope import Scope

# device ID: USB0::62700::4119::SDS08A0X804131::0::INSTR
scope = Scope("USB::62700::4119::SDS08A0X804131::INSTR")

# scope.reset()

# config channel 1
scope.channel_set(1, "SWIT", "ON")
scope.channel_set(1, "BWL", "20M")
scope.channel_set(1, "PROB", "DEF")
scope.channel_set(1, "PROB", "VAL,1.00E+01")

# config channel 2
scope.channel_set(2, "SWIT", "ON")
scope.channel_set(2, "BWL", "20M")
scope.channel_set(2, "PROB", "DEF")
scope.channel_set(2, "PROB", "VAL,1.00E+01")

# config acquire
# <5M can be done in one transfer
scope.aquire_set("MDEP", "1M")

# config waveform
scope.waveform_set("INT", "10") # return interval
scope.waveform_set("WIDT", "WORD") # send 16b per point
scope.waveform_set("STAR", "0") # start point
scope.waveform_set("POIN", "10000") # set points transfer

# grab waveform 1
scope.waveform_set("SOUR", "C1")
header1 = scope.waveform_preamble()
data1 = scope.waveform_data(header1)

time.sleep(0.1)
scope.trigger_run()
time.sleep(0.1)

scope.waveform_set("SOUR", "C2")
header2 = scope.waveform_preamble()
data2 = scope.waveform_data(header2)

plot(data1, data2)