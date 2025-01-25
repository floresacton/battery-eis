complete EIS procedure
you dont have to follow all these steps if you are testing your code to get it to work.  however if using a real cell and allowing it to operate autonomously, make sure you take everything here into account

before sweeps:
1) turn on devices
2) obtain current control bias and gain offsets (y=mx+b calibration for input analog signal) (you can assume b=0A and m=2A/V in the ideal case for the beginning, but these need to be found eventually)
3) turn on water cooling loop (25C or 77F)
4) begin measuring temperature of cell jig
5) ensure that system works as expected before cell is inserted with prior testing
	1) make sure python code can never error out (otherwise sig gen will be stuck on!)
	2) make sure the cell can never be overcharged (this is the most likely way we will have a battery fire)
	3) make sure that the cell can not be over discharged
	4) make sure the cell voltage does not leave the range [2.5V, 4.2V], which includes being at 2.6V nominally but drawing current with a load sinusoid that would bring the voltage to below 2.5V temporarily.  This should be easier than you think because the cell's impedance is largest at zero frequency, so if the cell does not over / under volt during very low frequencies (or DC which is zero frequency), the voltage drop due to the applied signal will tend to decrease with frequency.
6) insert cell into jig

during sweeps:
1) I have written a python file that should be a good starting point for EIS

after sweeps:
	make sure to turn off signal generator, then remove cell before turning off the equipment since I dont know how the BOP will handle a battery attached while the device is turned off.  Dont want to find out!  Turn off the water cooling as well.
