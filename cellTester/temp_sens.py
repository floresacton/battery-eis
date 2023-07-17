import os
import glob
import time
 
# reading from temp sensor is slow, updates at what seems to be 1Hz
# need to make reading temp happen separately from main program to avoid blocking for temp measurement
# when implemented, have temp_bridge write to a file that can be read by main program

class temp_sensor:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
         
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
     
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
     
    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

ts = temp_sensor()

output_file = "current.temperature"
print("running")
while True:
    t = ts.read_temp()

    f = open(output_file, 'w')
    f.write(str(t))
    f.write('\n')
    f.write(str(time.time()))
    f.close()
