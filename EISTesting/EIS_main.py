#                                     #
#          Battery EIS Code           #
#  Miguel Talamantez, Chris Evagora   #
#             April, 2024             #
#                                     #
#                                     #
#-------------------------------------#

#=====================================
# Imports
#=====================================
import device_bridge
import time
import usbtmc
import numpy

#=====================================
# Definitions/Variables 
#=====================================
database = {}
start_freq = 1/10 # Hz
end_freq = 100 # Hz
number_of_point = 30
m = 2 # A/V
b = 0 # A
desired_OCV = 3.7 # V (open circuit voltage)
stopping_current = -0.1 # A (assuming negative is charging)
max_charging_current = 5 # A (for do_control_law feedback)
min_charge_cell_voltage = 2.5 # V (minimum allowed cell voltage)
cell_V = 0  # V (only errors will show 0V)

#=====================================
# Initializations  
#=====================================
# ---------- SIG GEN Init -----------
print("---------------------------------")
print("Beginning Signal Generator Initialization...\n")
time.sleep(1)
SigGen = device_bridge.SigGen()



# ----------- OSC  Init -------------
print("---------------------------------")
print("Beginning Oscilloscope Initialization...\n")
time.sleep(1)
OscScope = device_bridge.Scope()


#=====================================
# Supporting Functions  
#=====================================

def do_control_law(cell_V):
    # This function is for feedback on the cell voltage. Since we're in CC-mode, 
    # we need to have this controller to know how much current to provide the
    # cell in case it's not charged.

    p = 1 # p controller, may need to make higher
    charging_current = p * (cell_V - desired_OCV)
    #This will produce a negative current for charging
    capped_charging_current = min(max_charging_current, max(-max_charging_current, charging_current))
    # cap upper and lower limits of control signal
    
    return capped_charging_current



#=====================================
# Cell Voltage Check  
#=====================================
print("---------------------------------")
print("Starting Cell Voltage Check... \n")
time.sleep(1)

# -- Make sure the cell is at the right voltage --

#cell_V = osc.get_v()
if cell_V > desired_OCV:
    print("The attached cell has too high a voltage:")
    print(f"{cell_V} V")
    print(f"This function attempted to charge to {desired_OCV} V")
    print("Exiting now")
    quit()

if cell_V < min_charge_cell_voltage:
    print("The attached cell is too low voltage to charge:")
    print(f"{cell_V} V")
    print(f"This function attempted to charge to {desired_OCV} V")
    print("Please use a different cell?")
    print("Exiting now")
    quit()


print("No voltage issues. Continuing.")
print("---------------------------------")

# -- Compute desired charging current --
#desired_current = do_control_law(cell_V)

while (desired_current < stopping_current):
    sig_gen.set_DC_mode()
    sig_gen.set_voltage(desired_current / 2) # divide approx by 2A/V
    time.sleep(0.5)

    #Read voltage and update
    cell_V = 






SigGen.on()
time.sleep(5)





print("\n")
print("===========================")
print("Shutting all devices off...")
print("===========================")
SigGen.off()

