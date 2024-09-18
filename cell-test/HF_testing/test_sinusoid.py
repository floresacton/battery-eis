import pyvisa
import time
import numpy as np
import csv


print("Found Resources:")

rm = pyvisa.ResourceManager()
eth_resource = "TCPIP::10.42.0.78::INSTR"
try:
    dev = rm.open_resource(eth_resource)
    print(eth_resource)
except:
    resources = rm.list_resources()
    for res in resources:
        print(res)
    dev = rm.open_resource(resources[0])


print()
print("==========================")
print("=======Initialized========")
print("==========================")
print()


filename = "output.csv"
f = open(filename, 'w')
csvwriter = csv.writer(f)
csvwriter.writerow(['T', 'V', 'I'])

max_I = 1
freq = 3
omega = freq * 2 * np.pi
def sinusoid(t):
    return max_I/2 * np.sin(omega * t) + max_I/2


t0 = time.time()
dev.write(":INP 1")

t_stop = 10
t = time.time() - t0
while t < t_stop:
    y = sinusoid(t)
    y_str = str(y)[0:5]
    dev.write(":CURR " + y_str)
#    time.sleep(.01)

#    V = float(dev.query("MEAS:VOLT?"))
#    I = float(dev.query("MEAS:CURR?"))
    V = 0
    I = 0

    #csvwriter.writerow([t, V, I])

    t = time.time() - t0


dev.write(":INP 0")

f.close()
    
import plot_data
