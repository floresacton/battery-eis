import usbtmc
import time

addrs = usbtmc.list_resources()
addr = "USB::1689::932::C030786::INSTR"
print(addrs)
print(addr)
assert addr in addrs, "no scope"

osc = usbtmc.Instrument(addr)
print(osc.ask("*IDN?"))


# meas 1, CH1 Amp
osc.write("MEASUrement:MEAS1:STATE ON")
osc.write("MEASUrement:MEAS1:SOURCE1 CH1")
osc.write("MEASUrement:MEAS1:TYPE AMPLITUDE")

# meas 2, CH2 Amp
osc.write("MEASUrement:MEAS2:STATE ON")
osc.write("MEASUrement:MEAS2:SOURCE1 CH2")
osc.write("MEASUrement:MEAS2:TYPE AMPLITUDE")

# meas 3, CH1 -> CH2 Phase Shift
osc.write("MEASUrement:MEAS3:STATE ON")
osc.write("MEASUrement:MEAS3:SOURCE1 CH1")
osc.write("MEASUrement:MEAS3:SOURCE2 CH2")
osc.write("MEASUrement:MEAS3:TYPE PHASE")

# meas 4, CH1 Mean
osc.write("MEASUrement:MEAS4:STATE ON")
osc.write("MEASUrement:MEAS4:SOURCE1 CH1")
osc.write("MEASUrement:MEAS4:TYPE MEAN")


# FilterVu
osc.write("DISPLAY:GLITCH OFF")
freqs = osc.ask("FILTERVU:FREQUENCY:AVAILABLE?").split(",")
freqs = [int(f) for f in freqs]
lowest = min(freqs)
freqs = osc.write(f"FILTERVU:FREQUENCY {lowest}")
freq = osc.ask("FILTERVU:FREQUENCY?")


# delay for update
time.sleep(1)
print("CH1 AMP?", osc.ask("MEASUrement:MEAS1:VALUE?"))
print("CH2 AMP?", osc.ask("MEASUrement:MEAS2:VALUE?"))
print("CH1->CH2 Phase?", osc.ask("MEASUrement:MEAS3:VALUE?"))
print("CH1 Mean?", osc.ask("MEASUrement:MEAS4:VALUE?"))

