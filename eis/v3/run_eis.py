import math
import sys
import time

from colorama import Fore, Style, init
from tools.gen import Gen
from tools.plotter import plot
from tools.scope import Scope

# test every 2^n freq
freq_exp2_start = 4 # 16Hz
freq_exp2_end = 13 # 8192Hz
freq_exp2_step = 2 # x4 Hz

# offset in V
offset_start = 0
offset_end = 4
offset_step = 1

# current amplitude
current_amplitude = 10

# constant delay
constant_delay = 0.25
# delay by x periods
period_delays = 15

# visible in width
periods_visible = 5

# number of points to sample
sample_points = 10000

# (channel, probe attenuation)
scope_config = [(1, 1), (2, 10), (3, 10)]

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
print(Fore.MAGENTA + f"Constant Delay: {constant_delay} seconds")
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

scope.channel_set(1, "SCAL", "1")
scope.channel_set(2, "SCAL", "0.05")
scope.channel_set(3, "SCAL", "0.1")

# setup trigger
scope.trigger_set_level(1)
scope.trigger_set_mode("NORM")

# setup waveform/aquire
scope.aquire_set("MDEP", "1M")
scope.waveform_set("WIDT", "WORD") 
scope.waveform_set("STAR", "0")

# setup gen
gen.set_mode(1, "SINE")
gen.set_mode(2, "SQUARE")
# +-(amplitude)A for opamp
gen.set_amplitude(1, current_amplitude)
gen.set_amplitude(2, 2)
gen.set_offset(2, 1)

##### end setup #####
print(Fore.GREEN + f"Finished Initialization")

freq_exp2_test = freq_exp2_start
freq_test = math.pow(2, freq_exp2_test)
offset_test = offset_start

def setup_freq():
    # set scope horizontal scale for "periods_visible" waveforms
    gen.set_freq(1, freq_test)
    gen.set_freq(2, freq_test)

    # set timebase to nearest interval
    scope.timebase_set(periods_visible/(freq_test*scope.hgrids))
    # run trigger to update points
    scope.trigger_run()

    # set proper point sample
    total_points = float(scope.aquire_get("POIN"))

    if (total_points < sample_points):
        print(Fore.RED + f"Not enough available points: {total_points:.2E}")
        sys.exit(1)

    scope.waveform_set("INT", total_points/sample_points)

def setup_offset():
    gen.set_offset(1, offset_test)

    #TODO scale scope to read

#### data format ####
# inside test folder in data
# test.info -> contains info on test
# test_freqID_offset_ID.csv -> contains raw test data

def log_result():
    data = []
    for schan in scope_config:
        scope.waveform_set("SOUR", f"C{schan[0]}")
        header = scope.waveform_preamble()
        data.append((header, scope.waveform_data(header)))

    # plot(data[0][1], data[1][1], data[2][1])

    #TODO write to csv file
    # for each chan
    # (x)_time, (x)_voltage


while freq_exp2_test < freq_exp2_end:
    setup_freq()

    while offset_test < offset_end:
        setup_offset()
        print(Fore.MAGENTA + f"Running Test: Freq - {freq_test}, Offset - {offset_test}")

        scope.trigger_run()
        gen.set_enable(1, 1)
        gen.set_enable(2, 1)

        time.sleep(constant_delay)
        time.sleep(1/freq_test*period_delays)

        scope.trigger_stop()
        gen.set_enable(1, 0)
        gen.set_enable(2, 0)

        log_result()

        offset_test += offset_step

    offset_test = offset_start
    freq_exp2_test += freq_exp2_step
    freq_test = math.pow(2, freq_exp2_test)

# disable wavegen
gen.set_enable(1, 0)
gen.set_enable(2, 0)
gen.set_enable(3, 0)