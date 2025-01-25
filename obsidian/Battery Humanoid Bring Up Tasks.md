Computer Assembly
- Make spine v3 bodges to enable ethernet connection
	- Find spine v3 design files, i cant find them anywhere
- Flash spinev3 microcontrollers
	- Assuming firmware is with design files, i cant find the firmware
- Configure upxtreme
	- Install operating system
	- Install robot software etc
	- imu communications setup?

Hip motors (2x)
- Glue magnets
- Strip insulation
- Flash latest firmware
- Zero motors

Arms and Legs
- To keep things simple, i think we should transplant arms and legs from current humanoid

Controls and modeling
- account for increased torso height in URDF
- mass and inertial properties change due to inclusion of battery mass

Rc receiver
- configure TX to connect to receiver

Internal harness
- Need to find autosport connector pinout that we use
- Spine board CAN to autosport connectors
- battery breakout board motor power to autosport connectors
- computer and motor enable switches to battery breakout board
- imu to up extreme
- battery breakout board to up extreme input power jack
- spine board to rc receiver
- battery breakout board computer power to up extreme

Assembly
- Assemble all working torso components


