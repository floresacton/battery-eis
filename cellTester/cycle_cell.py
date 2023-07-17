import device_bridge
import time
import signal
import logging
import random
import csv
import os
import sys

logging.basicConfig(
    filename='info.log',
    format='%(lineno)d %(levelname)s %(asctime)s - %(message)s',
    level=logging.INFO)

'''
Need to measure IR as a function of:

current
SOC

discharge cell at different currents to get discharge curve
'''

def shutdown_handler(sig, frame):
    load.off()
    supply.off()
    # log error
    error_msg = f"\nEquipment turned off due to signal {sig}.  Exiting."
    logging.error(error_msg)
    print(error_msg)
    quit()

signal.signal(signal.SIGABRT, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

def get_temp():
    input_file = "current.temperature"
    f = open(input_file, 'r')
    lines = f.readlines()
    while len(lines) != 2:
        time.sleep(.005)
        lines = f.readlines()
    sens_temp = float(lines[0][:-1])
    sens_time = float(lines[1])
    if time.time() - sens_time > 2: # if more than 2 seconds out of date
        return None
    return sens_temp

def charge_cell(output_file, charge_current, V_target=4.2, mah_max=4200, shutoff_I=0.050, t_max=None):
    # charge cell until current is smaller than set value

    if t_max is None:
        # must be charged at at least 1C
        t_max = mah_max/1000 * 1.5 * 3600 / charge_current

    logging.info(f"Beginning charge process.\ncharge_current = {str(charge_current)}\nV_target = {str(V_target)}, shutoff_I = {str(shutoff_I)}\nt_max = {str(t_max)}\nmah_max = {str(mah_max)}")

    update_period = 500 / 1000
    # track mah
    total_mah = 0

    try:
        # init to charge
        supply.set_V(V_target)
        supply.set_I(charge_current)

        # enable supply
        supply.on()
    except:
        logging.error("Could not initialize supply.  Stopping.")
        quit()
    
    # prep csvfile with fields
    fields = ['Time', 'Voltage', 'Current', 'Total mAh', 'Temperature']
    with open(output_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(fields) 

    # Allow supply to turn on before checking end conditions
    time.sleep(2)

    # begin timers
    t0 = time.time()
    # used for timing updates
    last_update_time = t0

    while(True):

        # measure charge current
        try:
            I1, I2 = supply.meas_I()
        except:
            logging.error(f"Unable to measure supply current.  Attempting shutdown.")
            try: 
                supply.off()
            except:
                logging.critical(f"Could not shut down supply.")
            else:
                logging.info(f"Successfully shut down.")
            quit()
        
        # measure cell voltage
        try:
            V = load.meas_V()
        except:
            logging.error(f"Unable to measure cell voltage.  Attempting shutdown.")
            try: 
                supply.off()
            except:
                logging.critical(f"Could not shut down supply.")
            else:
                logging.info(f"Successfully shut down.")
            quit()

        # update total mah
        total_mah += (I1 + I2) * 1000 * update_period / 3600

        # get temp
        temp = get_temp()

        # write to csv
        with open(output_file, 'a') as csvfile:
            csvwriter = csv.writer(csvfile) 
            # write data 
            data = [time.time()-t0, V, (I1+I2), total_mah, temp]
            csvwriter.writerow(data)


        ## check for end conditions ##
        # time > t_max
        # total Q > 4.2Ah
        # I < I_shutoff
        try:
            if time.time() - t0 > t_max:
                logging.warn(f"Time Exceeded!  Total time: {time.time() - t0}.  Stopping now.")
                break

            if total_mah > mah_max:
                logging.warn(f"Total mah Exceeded! Total mah: {total_mah}.  Stopping now.")
                break

            if (I1+I2) < shutoff_I:
                logging.info(f"Current levels reached the stopping point.  Stopping now.")
                break
        except:
            logging.error("Could not check end conditions.  Attempting shutdown.")
            try: 
                supply.off()
            except:
                logging.critical(f"Could not shut down supply.")
            else:
                logging.info(f"Successfully shut down.")
            quit()
            
        # wait for update period to elapse
        while(time.time() - last_update_time < update_period):
            continue
        last_update_time = time.time()

    # disable supply
    try:
        supply.off()
    except:
        logging.critical(f"Could not shut down supply at conclusion of charge process.")

def discharge_cell(output_file, discharge_current, mah_max=4200, shutoff_V=3.00, t_max=None):
    # discharge cell until cell voltage is shutoff voltage

    if t_max is None:
        # must be discharged at at least 1C
        t_max = mah_max/1000 * 1.5 * 3600 / discharge_current

    logging.info(f"Beginning discharge process.\ndischarge_current = {str(discharge_current)}\nshutoff_V = {str(shutoff_V)}\nt_max = {str(t_max)}\nmah_max = {str(mah_max)}")

    update_period = 500 / 1000
    # track mah
    total_mah = 0

    try:
        # init to discharge
        load.set_I(discharge_current)

        # enable load
        load.on()
    except:
        logging.error("Could not initialize load.  Stopping.")
        quit()
    
    # prep csvfile with fields
    fields = ['Time', 'Voltage', 'Current', 'Total mAh', 'Temperature']
    with open(output_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(fields) 

    # Allow load to turn on before checking end conditions
    time.sleep(2)

    # begin timers
    t0 = time.time()
    # used for timing updates
    last_update_time = t0

    while(True):

        # measure load current
        try:
            I = load.meas_V()
        except:
            logging.error(f"Unable to measure load current.  Attempting shutdown.")
            try: 
                load.off()
            except:
                logging.critical(f"Could not shut down load.")
            else:
                logging.info(f"Successfully shut down.")
            quit()
        
        # measure cell voltage
        try:
            V = load.meas_V()
        except:
            logging.error(f"Unable to measure cell voltage.  Attempting shutdown.")
            try: 
                load.off()
            except:
                logging.critical(f"Could not shut down load.")
            else:
                logging.info(f"Successfully shut down.")
            quit()

        # update total mah
        total_mah += I * 1000 * update_period / 3600

        # get temp
        temp = get_temp()

        # write to csv
        with open(output_file, 'a') as csvfile:
            csvwriter = csv.writer(csvfile) 
            # write data 
            data = [time.time()-t0, V, I, total_mah, temp]
            csvwriter.writerow(data)


        ## check for end conditions ##
        # time > t_max
        # total Q > 4.2Ah
        # V < shutoff_V
        try:
            if time.time() - t0 > t_max:
                logging.warn(f"Time Exceeded!  Total time: {time.time() - t0}.  Stopping now.")
                break

            if total_mah > mah_max:
                logging.warn(f"Total mah Exceeded! Total mah: {total_mah}.  Stopping now.")
                break

            if V < shutoff_V:
                logging.info(f"Voltage levels reached the stopping point.  Stopping now.")
                break
        except:
            logging.error("Could not check end conditions.  Attempting shutdown.")
            try: 
                load.off()
            except:
                logging.critical(f"Could not shut down load.")
            else:
                logging.info(f"Successfully shut down.")
            quit()
            
        # wait for update period to elapse
        while(time.time() - last_update_time < update_period):
            continue
        last_update_time = time.time()

    # disable load
    try:
        load.off()
    except:
        logging.critical(f"Could not shut down load at conclusion of discharge process.")


def do_cycle():

    '''
    # get number of cycles
    # get cycle parameters
    cycle_count = sys.argv[2]
    charge_current = sys.argv[3]
    discharge_current = sys.argv[4]
    '''

    filenames= os.listdir("./celldata")
    directories= []
    for filename in filenames: # loop through all the files and folders
        if os.path.isdir(os.path.join(os.path.abspath("./celldata"), filename)): # check whether the current object is a folder or not
            directories.append(filename)

    print("Enter the number corresponding to the cell being tested")
    for i in range(len(directories)):
        print(i+1, ":", directories[i])
    
    while True:
        cell_idx = int(input())
        if cell_idx < 0 or cell_idx > len(directories):
            print("Invalid input, try again")
            continue
        break
        
    path = f"celldata/{directories[cell_idx-1]}/"
    timestr = time.strftime("%Y_%m_%d-%H_%M_%S")

    charge_file = path + f"{timestr}_charge.csv"
    discharge_file = path + f"{timestr}_discharge.csv"

    charge_cell(charge_file, 6)
    discharge_cell(discharge_file, 10)

if get_temp() is None:
    raise(Exception("Temperature sensor is not working.  Did you run temp_sens.py in the background?"))

load = device_bridge.Load()
supply = device_bridge.Supply()

do_cycle()
