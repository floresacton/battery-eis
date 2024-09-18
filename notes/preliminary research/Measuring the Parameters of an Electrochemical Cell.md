A battery model is important for understanding how a battery performs under load.  A full model will characherize the source and impedance of a battery cell.  Modeling of a battery's internal parameters usually falls onto collecting empirical data of batches of cells.  We can find the relations between capacity, impedance, SOC, temperature, and cycle count by actually collecting data with real world equipment.  Modeling the impedance of a battery cell relies on data collection but can be done using equivalent circuit models that approximates the internal dynamics of a battery cell.  One such model that is popular and fairly accurate is the Randles model.  The Randles model quantifies the electrolyte resistance, the charge transfer resistance, and the capacitance of the double layer capacitor, each of which roughly corresponds to a physical process in the electrochemistry of an electrochemical cell.  More on this below.


![[Randles Model.png]]
<div style="text-align: center;"> Simple Randles Model for the internal impedance of an electrochemical cell.  The diffusion resistance does exist in a cell, though is usually much smaller than the charge transfer resistance and can either be omitted or included in the charge transfer resistance.</div>

One can find the DC internal resistance of a battery, by applying a large DC load that exceeds the time constant of the internal RC circuitry.  Typical pulse lengths are between 1 and 10 seconds to allow all second order and above effects to reach equilibrium.  This will not reveal the entire dynamics of a battery cell, and other methods must be used to extract values for the other internal components of a battery cell.  In order to back out the components in the Randles model, one must consider the transients of the battery under test.  Injection of AC frequencies alongside careful measurements of the current waveform can help reveal the internals of the battery cell.  

![[origin-lissajous-figure.jpg]]
<div style="text-align: center;"> Example of a Lissajous figure of the injection of frequencies about an operating point, that is around the battery voltage.  A resultant ovular shape will appear.  The shape and orientation of the oval is capable of revealing the internal impedance of a battery.  This method of impedance measurment is outdated, but shows how we can use a input signal to observe a response from the battery.  We opt for more precise measurements nowadays utilizing advancements in digital electronics.</div>

By measuring the corresponding current waveform which will be of a given magnitude and phase for a particular frequency, we can plot the impedance of the battery for every input frequency on a Nyquist plot.

![[empirical_Nyquist.png]]
<div style="text-align: center;"> An example of the Nyquist plot for a healthy cell.  As you can see, frequency has a large impact on both the resistance and reactance components of impedance.  Each sample plotted in this plot is a measurement taken at a particular frequency.  As frequency increases, the overall impedance of the cell decreases.</div>

The resistance of the electrolyte, Rel, and the resistance of the charge transfer, Rct, correspond to different components in the Randles model.  Rel is the resistance of the electrolyte between the electrodes, manifesting as the movement of lithium ions traveling between the electrodes.  Rct is the charge transfer resistance, the resistance at the boundary between the electrode and the electrolyte.  This is where the electrochemical reaction occurs, and assosicated with it is a certain kinetic speed of the reaction.  This is why we can consider the resistance to act at a single point, something not normal for uniformly resistive materials.  The charge transfer parameter, gives this plot its peculiar shape with its pole at around 1-10 Hz.

![[Nyquist_Randles_model.png]]

![[Nyquist_charge_transfer.png]]

The largest impedance will be seen when operating at DC when the double layer capacitor is fully charged and does not pass any current.  As the frequency increases and we move over to the left, the kink in the curve shows the higher order effects of the warburg impedance (not modeled in the simplified Randles model) having a large impact at relatively low frequencies.

In order to back out the parameters of the Randles model (or really any model we choose to use), a nonlinear least squares (NLLS) algorithm can be used.  We begin with estimates for each of the component values in our RLC network and use them as the parameters to be optimized by NLLS.  NLLS will minimize the difference in impedance between the model and the empirical data collected across all frequencies.  https://en.wikipedia.org/wiki/Non-linear_least_squares

More advanced methods exist and are being actively researched.  https://arxiv.org/pdf/1906.04150.pdf

---

Besides modeling the internal impedance of the battery, we can also consider the internal ideal voltage source which drives the Randles model.  Although a voltage source does not change votlage with current demanded, the voltage of a battery under no load definitely does not stay constant.  The most obvious scenario is the SOC of the battery decreasing as energy is depleted.  This source also depletes more rapidly with damage and wear.  This is a function of cycle count, temperature of the battery under high power, the rapidity of charges and discharges, at what SOC the battery is stored, and many other factors which we can not model very well.

![[IRvsCycle.png]] 
<div style="text-align: center;"> We can see the effects of cycling on a cell's stored charge.  We also notive resistance deceptively does not change due to the fact that these measurements were taken as DCIR.  Isolating the charge transfer resistance using EIS is a better method of determining battery degradation using only impedance.</div>








