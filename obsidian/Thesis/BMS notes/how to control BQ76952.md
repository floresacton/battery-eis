Use partially autonomous control
let IC enable protections
let stm32 clear error flags to reenable system

to clear OCD error, manual says to charge for minimum of recovery charging current for recovery charging time.  found  out that you can rewrite OCD threshold to reset the error

if humanoid has over/under current/voltage error, want humanoid motor power switch to reset the battery

DFETOFF command to stop discharge
CFETOFF command to stop charge
ALLFETON to turn fets back on
have stm32 have the discharge fets always enabled for now to let IC control battery


