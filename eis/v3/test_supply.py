import time

from tools.supply import Supply

supply = Supply("USB0::62700::5168::SPD3XHBX1R3110::INSTR")
supply.set_enable(1, 0)
supply.set_voltage(1, 1.4)
supply.set_current(1, 2.3)
# print(supply.measure_voltage(1))
# print(supply.measure_current(1))
# print(supply.measure_power(1))
