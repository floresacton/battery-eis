import time
from KP184.kp184 import KP184

port = "/dev/ttyUSB0"

device_addrs = [2,3,4,5]
#device_addrs = [1]
#device_addrs = [2]
kps = []
for n in device_addrs:
    kps.append(KP184(port, n))

for kp in kps:
    kp.writeLoadOnOff(0)
    kp.writeMode("CC")


time.sleep(1)

while True:
    for kp in kps:
        kp.writeLoadOnOff(1)
    time.sleep(1)
    for kp in kps:
        kp.writeLoadOnOff(0)
    time.sleep(1)
