import device_bridge
import time

dev = device_bridge.SigGen()

dev.on()
time.sleep(1)
dev.off()
