import csv
import math
import sys
import time

import numpy as np
from colorama import Fore, Style, init

from tools.fitter import sine_fit
from tools.gen import Gen
from tools.plotter import plot
from tools.scope import Scope

# test ferquencies
freq_exp2_start = np.log2(10)
freq_exp2_end = np.log2(8000)
freq_exp2_step = (freq_exp2_end-freq_exp2_start)/10

# offset in amps inclusive
offset_start = 0
offset_end = 0
offset_step = 1

# nominal testing voltage
# cell_voltage = 3.5
cell_voltage = 0

# current amplitude
current_amplitude = 5

# visible in width
periods_visible = 5

# number of bops activated
active_bops = 1

# bop center voltage offset
bop_offset = -0.262
# bop amplitude output scaling
bop_gain = 1.045

# resistances to calculate ranges
# in order from bops
neg_wire_resistance = 0.14
shunt_resistance = 0.00996
shunt_wire_resistance = 0.065

cell_resistance = 0.008 # cells is ~0.01

# constant delay
constant_delay = 1
# delay by x periods
period_delays = 15

# number of points to sample
sample_points = 10000

# save variables
save_points = False
save_sine_fit = False

nyquist_file = "nyquist.csv"

# (channel, probe attenuation)
scope_config = [(1, 1), (2, 1), (3, 1), (4, 1)]

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

scope.channel_set(1, "SCAL", f"{0.02*current_amplitude:.2E}")
scope.channel_set(2, "SCAL", f"{0.02*current_amplitude:.2E}")
scope.channel_set(3, "SCAL", f"{0.02*current_amplitude:.2E}")
scope.channel_set(4, "SCAL", f"{0.02*current_amplitude:.2E}")

# setup trigger
scope.trigger_set_level(0)
scope.trigger_set_mode("NORM")

# setup waveform/aquire
scope.aquire_set("MDEP", "1M")
scope.waveform_set("WIDT", "WORD") 
scope.waveform_set("STAR", "0")

# setup gen
gen.set_mode(1, "SINE")
# +-(amplitude)A for opamp
gen.set_amplitude(1, current_amplitude*bop_gain)
gen.set_offset(1, bop_offset)
gen.set_enable(1, 1)

##### end setup #####
with open('data/'+nyquist_file, 'w') as file:
    file.write('freq,resistance,theta\n')

##### end config logging #####
print(Fore.GREEN + f"Finished Initialization")

test_index = 0
freq_exp2_test = freq_exp2_start
freq_test = math.pow(2, freq_exp2_test)
offset_test = offset_start
waveform_interval = 0

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

    global waveform_interval
    waveform_interval = total_points/sample_points
    scope.waveform_set("INT", waveform_interval)

def setup_offset():
    gen.set_offset(1, bop_offset+offset_test/active_bops)

    center_current = 2*offset_test
    scope.channel_set(1, "OFFS", f"{center_current*(neg_wire_resistance):.2E}")
    scope.channel_set(2, "OFFS", f"{center_current*(neg_wire_resistance+shunt_resistance):.2E}")
    scope.channel_set(3, "OFFS", f"{center_current*(neg_wire_resistance+shunt_resistance+shunt_wire_resistance):.2E}")
    scope.channel_set(4, "OFFS", f"{center_current*(neg_wire_resistance+shunt_resistance+shunt_wire_resistance+cell_resistance)-cell_voltage:.2E}")

#### data format ####
# inside test folder in data
# test.info -> contains info on test
# test_freqID_offset_ID.csv -> contains raw test data

def log_result():
    data = []
    for chan in [1,2,3,4]:
        scope.waveform_set("SOUR", f"C{chan}")
        header = scope.waveform_preamble()
        data.append(scope.waveform_data(header, waveform_interval))

    # pretty sure the times are the same
    current = data[0].copy()
    current[:, 1] = data[1][:, 1] - data[0][:, 1]

    voltage = data[2].copy()
    voltage[:, 1] = data[3][:, 1] - data[2][:, 1]

    current_fit = sine_fit(current, freq_test)
    voltage_fit = sine_fit(voltage, freq_test)

    camp, cphi, coffset = current_fit
    vamp, vphi, voffset = voltage_fit

    dangle = cphi-vphi
    resistance = (vamp/camp)*shunt_resistance

    with open('data/'+nyquist_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([freq_test, resistance, dangle])


while freq_exp2_test <= freq_exp2_end:
    setup_freq()

    while offset_test <= offset_end:
        setup_offset()
        print(Fore.MAGENTA + f"Running Test: Freq - {freq_test}, Offset - {offset_test}")

        scope.trigger_run()
        gen.set_offset(1, bop_offset)

        time.sleep(constant_delay)
        time.sleep(1/freq_test*period_delays)

        scope.trigger_stop()

        log_result()

        offset_test += offset_step

    offset_test = offset_start
    freq_exp2_test += freq_exp2_step
    freq_test = math.pow(2, freq_exp2_test)
    test_index += 1

# disable wavegen
gen.set_mode(1, "DC")
gen.set_offset(1, bop_offset)