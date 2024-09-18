import numpy
import sig_gen # go find the correct way to import this code, it was done in my other files
import oscilloscope # same thing, you may need to adapt my code to talk to the oscilloscope

### WARNING ###
# this file was written by chris and never tested or run
# though this should be a good foundation for the final script
# please note that all voltages, currents, and voltage and current setpoints
# may have their sign wrong!  plus or minus!
# it is your job to make sure that what I have written is correct

# this file assumes that positive current is discharging the cell
# and that negative current is charging the cell


# in this file of !!UNTESTED!! code, im going to call functions for the sig_gen class that may not be implemented
# go implement them according to the programming manual of the signal generator
# let me know if you need help (you probably will)
sig_gen.off()

## first make sure cell has been replenished since last test
## thus we begin by charging the cell

## since we only have access to current control
## and cannot dynamically set the voltage limit since the BOP is analog
## we need to write our own charging controller
## rats

desired_OCV = 3.7 # V (open circuit voltage)

# when we reach this charge current, we can consider the cell to be charged
stopping_current = -0.1 # A

# given cell voltage
# return charge current in amps
# negative current means charging
# this function will also discharge the cell if it is higher than the desired voltage
# but this will bias the cell in the wrong direction and should be avoided (ask chris if this doesnt make sense)
def do_control_law(cell_v):
    max_charging_current = 5 # A
    p = 1 # P controller, may need to make higher

    charging_current = p * (cell_v - desired_OCV) # this will produce a negative current for charging

    # cap upper and lower limits of control signal
    capped_charging_current = min(max_charging_current, max(-max_charging_current, charging_current))

    return capped_charing_current

cell_v = osc.get_v()

# make sure the cell is not already charged
if cell_v > desired_OCV:
    print("the attached cell has too high a voltage")
    print(f"{cell_v} V")
    print(f"this function attempted to charge to {desired_OCV} V")
    print("exiting now")
    quit()

# compute desired charging current
desired_current = do_control_law(cell_v)

# while there is still a non negligible current flowing (charging current is negative):
# this check should cause a cell that is higher than the desired voltage to not get charged
while (desired_current < stopping_current):
    sig_gen.set_DC_mode()
    sig_gen.set_voltage(desired_current / 2) # divide approx by 2A/V
    time.sleep(.5)

    # read voltage and update
    cell_v = osc.get_v()
    desired_current = do_control_law(cell_v)


# once the while loop exits above, the cell should be charged

## begin EIS
sig_gem.set_to_sinusoid_mode()

start_freq = 1/10 # Hz
end_freq = 100 # Hz
number_of_points = 30
m = 2 #A/V
b = 0 #A

# where we will store our measurements
database = {}

# apply y=mx+b offset to desired current to get corrected output
# where x is desired current of the BOP
# and y is the voltage level we command of the signal generator
def get_corrected_signal(desired_current):
    return (desired_current - b) / m

for test_current in [1, 3, 5]: #amps
    # find corrected upper and lower levels for sig gen
    sinusoid_min = 0
    sinusoid_max = test_current
    corrected_sinusoid_min = get_corrected_signal(sinusoid_min)
    corrected_sinusoid_max = get_corrected_signal(sinusoid_max)

    # i dont know if these should be flipped, just make sure we are only discharging during EIS
    sig_gen.set_high_level(corrected_sinusoid_max)
    sig_gen.set_low_level(corrected_sinusoid_min)

    for frequency in np.logspace(start_freq, end_freq, num=number_of_points):
        sig_gen.set_freq(frequency)
        sig_gen.on()
        time.sleep(1) # wait a bit for cell dynamics to settle, oscilloscope to perform measurements, etc
        real, imaginary = obtain_measurements() # obtain complex impedance from measurements
        sig_gen.off()
        time.sleep(1) # wait again since we are turning off, though turning off may not be necessary

        # store data in dictionary, indexed by current and frequency (the 2d "array" of sweeps we are performing)
        database[(test_current, frequency)] = (real, imaginary)

        # this for loop will pulse the cell on and off with frequencies, which could be slow
        # you could also keep the signal generator on, and just update the frequency
        # doing that and tuning the waiting time for settling can make the test go faster
        # this is better because the cell's state of charge should change as minimally as possible through a test

# store database
# use the python pickle library to write it to a file for later processing

        
