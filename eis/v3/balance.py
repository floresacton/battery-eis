import time

from colorama import Fore, Style, init

from tools.load import Load
from tools.supply import Supply

init(autoreset=True)

load = Load("TCPIP::10.42.0.78::INSTR")
supply = Supply("USB0::62700::5168::SPD3XHBX1R3110::INSTR")

# disable supply and load
supply.set_enable(1, 0)
load.set_enable(0)
time.sleep(0.5)

discharge_current = 5
charge_current = 3

# nominal 3.71V - 3.72V
discharge_voltage = 3.52
charge_voltage = 3.8

# discharge below thresh
load.set_mode("CURR")
load.set_current(discharge_current)
load.set_enable(1)

time.sleep(1)

while load.measure_voltage() > discharge_voltage:
    time.sleep(0.1)

load.set_enable(0)

print(Fore.GREEN + "Finished Discharging")

# charge above threshold
supply.set_voltage(1, 4.2)
supply.set_current(1, charge_current)
supply.set_enable(1, 1)

time.sleep(1)

while supply.measure_voltage(1) < charge_voltage:
    time.sleep(0.1)

supply.set_enable(1, 0)

print(Fore.GREEN + "Finished Charging")
