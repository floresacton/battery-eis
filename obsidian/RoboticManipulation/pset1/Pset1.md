1.1) 
	a. 0.9
	b. alpha
	c. 1.0

2.2)
	a. Done
	b. Torque_commanded is the sum of tau_no_ff and tau_ff.  We use tau_ff to counteract the forces that we know will be present for a given context, such as gravity, in order to effectively remove external influence on the plant.  Tau_no_ff is usually given by a controller which is correcting small errors from the measured position due to imperfections in our system model.  The controller will usually perform better without the presence of a constant force, such as in the case of a P controller.

Survey: ManipulationStation