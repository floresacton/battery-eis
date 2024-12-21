import time

from tools.load import Load

load = Load("TCPIP::10.42.0.78::INSTR")
load.set_enable(0)
load.set_mode("CURR")
load.set_current(0.1)

load.set_enable(1)
print(load.measure_voltage())

time.sleep(2)

print(load.measure_current())
print(load.measure_voltage())

load.set_enable(0)
