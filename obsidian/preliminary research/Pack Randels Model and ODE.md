When modeling the battery pack using the simple randles model, we place many equivalent cell models in series and parallel to make an equivalent circuit model for the pack.
![[pack_randles_model.png]]

This is good, though to simplify calculations it would be nice if we could condense this model and not lose any information.  If we make the assumption that all cells have identical internal parameters r1, r2, and c, we can prove that we can replace the entire circuit of series and parallel randles models (the expanded model) with a single randles model (the simplified model).

We begin by finding the thevenin impedance of the expanded model by setting all sources to zero volts and measuring from V_bat to gnd.  We will find 15s/2p * Z where Z is the impedance of the cell level randles model.  We find that the resistances in the simplified randles model are scaled by 15/2 while the capacitor is scaled by 2/15.  This nice answer is very convenient because we now only have one unknown state variable which corresponds to the fact that this is a first order system.
![[randles_math.jpg]]

In order to apply this model to the optimization, we need to solve for the unknown state variable at each time step.  In this case we have an unknown internal voltage node V_x which not only depends on the system parameters and desired output power, but also the history of the system.  This manifests in the amount of charge stored in the double layer capacitance, Q.  What follows is a derivation for the output voltage Vo, the capacitor current Ic, and the discrete update made to charge Q for every step of Euler's method.  We set Q = 0 for time step 0.
![[ODE.jpg]]

![[pack_i.jpeg]]
And pack current can be calculated.

Although we now know how to translate a cell model into a pack equivalent model and integrate it through time with a changing power demand, some more work still needs to be done before it can be implemented into the optimization for the robot.   

In order to sufficiently model the battery dynamics we need to ensure that the time between updates is much less than the time constant of the randels model.  This is important to ensure the stability and correctness of Euler's method.  Considering that the Randels circuit model is a first order system we expect the battery to decay exponentially to steady state in response to a step change in load.  The robot optimization in our case uses a fixed time constant between points on the trajectory which may not be sized appropriately for the time constant of the battery dynamics.  Using a time step that is too large could lead to oscillations of the first order battery model about the steady state operating point or even instability, having the system variables go off to infinity.  It is therefore necessary to implement two different timescales for the battery dynamics to be well modeled in the general case.

A simple solution is to take an integer multiple of the number of points used in the main trajectory to be used for the battery dynamics.  The slower main trajectory will only update the power demanded every N steps and sample the battery voltage every N steps.  Constrain the battery model with the dynamic update equations every step of the high frequency timescale.

Another problem is that the function for CCV with the IR or Randles model could return imaginary numbers for sufficiently large output powers.  Knitro will make changes to the decision variables for every iteration, and may choose a power that returns an imaginary number.  To avoid complex values, an approximation for the function that is  

![[ccv_randles_approx.jpeg]]
![[linear_approx.png]]
https://www.desmos.com/calculator/arybtvphrv

After talking with Yanran, there are some other options to explore.
![[imaginary_elimination_options.png]]