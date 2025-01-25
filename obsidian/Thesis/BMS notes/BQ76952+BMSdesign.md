Need to document what is required of BMS design because there are too many things to remember.

Design considerations:
	1) System current consumption
	2) Shunt resistor sizing calculation
	3) Interface selection / isolation
	4) Wakeup sequence (if necessary)
	5) High side switches, pre(dis)charge and passives
	6) Multi board layout and connection between them
	7) Appropriate safety, protection, and redundancy
	8) User control / ease of monitoring or use
	9) Power nets / split grounds / net ties where necessary
	10) External connection to humanoid harnessing
	11) Vertical height constraints
	12) The connector
	13) ensure charge pump cap big enough for switches
	14) button controlled hardware reset / ability to put device in HDQ mode for external programming

BQ76952 state machine:
![[Pasted image 20240202164600.png]]
To exit shutdown if ever entered and STM32 unpowered, physical onboard switch to pulldown TS2 to repower STM32 and enter NORMAL mode.


1) System current consumption
48 cells x 3.6V x 4.2Ah x 50% SOC storage = 363 Wh

**BMS consumption:**
I_Normal = 286 uA -> 16mW -> 22k hours -> 2.5 years until death by negligence

I_sleep = 41 uA -> 2.3mW -> 153k hours -> 17.5 years until death by negligence

I_deepsleep = 10.7 uA -> 600uW -> 586k hours -> 67 years

I_shutdown = 3 uA -> 16uW -> 2.09m hours -> 238 years

Cannot stay in NORMAL mode continuously, must be in at least SLEEP or lower to minimize power.  SLEEP is enough, but DEEPSLEEP ensures that DSG and CHG remain off which is good if battery remains plugged in while in humanoid.  DEEPSLEEP still allows REG1 to be enabled to power STM32, which it can wake with ALERT or can be woken by LV SWITCH or HV SWITCH

**STM32 consumption:**
STM32 can be in NORMAL, SLEEP, STOP, OR STANDBY mode.  Only STANDBY mode is capable of achieving low enough power consumption (in the case of the F446 like on powerboard), with a maximum expected current of 8uA.  Waking from STANDBY can be done by interrupt on wakeup pin, or by use of internal RTC to wake periodically.  Good because we can wake STM32 with HV SWITCH and LV SWITCH using a pin interrupt.
https://controllerstech.com/low-power-modes-in-stm32/

STM32 also should not exceed 45mA of current, max of REG1.  Limit clock freq to meet power requirement.



