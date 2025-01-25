Bodges necessary:

include pulldown resistor from RST pin of BQ to ground

replace resistor to gate of bjt for buzzer from 10k to 360

replace digital isolator with [[SI8641]] and remove 0 ohm resistors for external UART comms, this BMS will be CAN instead

short Vccuv on powerboard gate driver to HV- on the next pin

make b+ div enable bjt driven stronger (need to do this still)

when plugging in header, tilt it so that the temp sensing and more importantly B- is plugged in first to avoid blowing up the bq76952.  Seems like BQ needs B- plugged in first to avoid blowup.

Hindsights:

why didnt i have an analog high speed shutoff circuit for voltage too? thats the important one

why didnt I have the STM discharge the gate of the fet also controlled by BQ76952?  no need for another gate driver and set of switches if I am only going to turn off with high speed



