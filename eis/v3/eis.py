import math
import time

from colorama import Fore, Style, init
from tools.gen import Gen
from tools.scope import Scope

# test every 2^n freq
freq_exp2_start = 4 # 16Hz
freq_exp2_end = 13 # 8192Hz
freq_exp2_step = 1 # x2 Hz

# offset in V
offset_start = 0
offset_end = 1
offset_step = 0.01

# constant delay
propagation_delay = 1
# delay by x periods
period_delays = 20

# visible in width
periods_visible = 5

# (channel, probe attenuation)
scope_config = [(1, 10), (2, 10), (4, 1)]

##### end config #####

init(autoreset=True)

print(Fore.CYAN + Style.BRIGHT + "Test Configuration")

# Frequency range in Hz
freq_range_start = math.pow(2, freq_exp2_start)
freq_range_end = math.pow(2, freq_exp2_end)
print(Fore.YELLOW + f"Frequency Range: {freq_range_start:.1f} Hz to {freq_range_end:.1f} Hz")

# Offset voltage range
print(Fore.GREEN + f"Offset Voltage Range: {offset_start} V to {offset_end} V, step {offset_step} V")

# Propagation delay and period delay
print(Fore.MAGENTA + f"Propagation Delay: {propagation_delay} seconds")
print(Fore.MAGENTA + f"Period Delays: {period_delays} periods")

# Periods visible on the scope
print(Fore.BLUE + f"Periods Visible: {periods_visible}")

# Scope configuration: channel and probe attenuation
print(Fore.CYAN + "Scope Configuration:")
for channel, attenuation in scope_config:
    print(Fore.RED + f"  Channel {channel}: Probe Attenuation = {attenuation}x")

##### end log ######

# connect to gen and scope
gen = Gen("USB::62700::4355::SDG1XDDQ7R3310::INSTR")
scope = Scope("USB::62700::4119::SDS08A0X804131::INSTR")

# reset gen and scope
gen.set_enable(1, 0)
gen.set_enable(2, 0)
gen.set_enable(3, 0)
scope.reset()

# setup channels
for schan in scope_config:
    scope.channel_set(schan[0], "SWIT", "ON")
    scope.channel_set(schan[0], "BWL", "20M")
    scope.channel_set(schan[0], "PROB", f"VAL,{'{:.2E}'.format(schan[1])}")

# setup waveform/aquire
scope.aquire_set("MDEP", "1M")
scope.waveform_set("WIDT", "WORD") 
scope.waveform_set("STAR", "0")
# scope.waveform_set("INT", "10")
# scope.waveform_set("POIN", "10000")

# setup gen
gen.set_mode(1, "SINE")
# +-(amplitude)A for opamp
gen.set_amplitude(1, 15)

##### end setup #####

freq_exp2_test = freq_exp2_start
freq_test = math.pow(2, freq_exp2_test)
offset_test = offset_start

def setup_freq():
    # set scope horizontal scale for fixed number of waveforms
    gen.set_freq(1, freq_test)
    pass

def setup_offset():
    gen.set_offset(1, offset_test)
    #TODO scale scope to read

#### data format ####
# inside test folder in data
# test.info -> contains info on test
# test_freqID_offset_ID.csv -> contains raw test data


def log_result():
    chan_data = []
    for schan in scope_config:
        scope.waveform_set("SOUR", f"C{schan[0]}")
        header = scope.waveform_preamble()
        chan_data.append((header, scope.waveform_data(header)))

    # for each chan
    # (x)_time, (x)_voltage

    #TODO write to csv file

while freq_exp2_test < freq_exp2_end:
    setup_freq()

    while offset_test < offset_end:
        setup_offset()

        gen.set_enable(1, 1)

        time.sleep(propagation_delay)
        time.sleep(1/freq_test*period_delays)

        gen.set_enable(1, 0)

        log_result()

        offset_test += offset_step

    freq_exp2_test += freq_exp2_step
    freq_test = math.pow(2, freq_exp2_test)
