In order to find the internal parameters of the cell without expensive EIS equipment, I would like to investigate if some shortcuts can be made to back out the parameters given the simple Randles model is used to model the internal dynamics of the cell.

Normally, EIS testing of a battery cell gives a complex impedance for a range of frequencies, and a NLL squares algorithm is used to fit the behavior to any arbitrary model.  Since we are trying to fit the simple Randles model which is only a first order system, other methods can be explored to back out the internal parameters of the cell.

![[plan.jpg]]


A proposed switching DC load circuit can be used to generate the loads necessary to follow the three step process above.  The load will have an adjustable switching frequency from 1Hz all the way to 100kHz+, much outside any RC time constant that could be found in a lithium ion cell.  The load will also have a current sensor capable of up to 50A measurements and a gain of 0.24mV / A.  In order to measure the small voltage changes of the cell voltage under load (~1V max @ 40A for a cell like the 40T), an adjustable subtractor circuit is used to bring the cell voltage down closer to zero.  This would increase the signal to DC bias ratio and allow an oscilloscope to make more accurate measurements of the internal RC time constant.

Need https://www.amazon.com/Uxcell-a11051300ux0044-Current-Measuring-Resistor/dp/B00D754BYG/ref=sr_1_2?crid=FQZHJX6HFDON&keywords=shunt+resistor+50A&qid=1682576634&sprefix=shunt+resistor+50a%2Caps%2C75&sr=8-2


![[Square_EIS_circuit.png]]
https://www.analog.com/en/design-notes/monitoring-a-small-step-change-of-a-dc-voltage.html

