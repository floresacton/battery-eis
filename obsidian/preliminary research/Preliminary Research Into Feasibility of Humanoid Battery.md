Begin with the goal of presenting to Sangbae and others a potential battery project for my MEng thesis, examining the feasability of designing a battery that fits roughly within the chest of the humanoid and handle the expected load cases of humanoid locomotion including an incredibly power demanding back flip.  Other considerations of a successful battery will include guarantees about the long term health of the battery, the safety of the systems to be put in place to monitor and regulate the battery, as well as special considerations for a pack that would use lipo pouch cells, the most promising avenue to accomplish these design requirements.  Other novel methods such as a li ion cylindrical cell / super capacitor hybrid to meet peak power requirements will be explored.

Cylindrical li ion cells are the most popular packaging for lithium based batteries.  They offer many advantages such as the numerous number of options for consumers due to the maturity of cylindrical cell technology, low cost to manufacture, and safety.  Pouch based cells offer advantages such as improved packing density, reduced weight, and drastically lower internal impedances which allow them to output much higher power per unit weight or volume compared to cylindrical cells.  This makes pouch cells the optimal choice for performance batteries.  Despite this, we still see cylindrical cells predominantly used in generic battery applications due to the nature of current high power battery applications such as electric vehicles.  

Often times the main design consideration for EV's is to fit as much energy as possible into batteries to maximize milage for consumers.  A consequence of this is that these batteries are often packaged in enormous quantities, reducing the individual power requirements of each cell.  Although pouch cells work at higher powers compared to li ion, this benefit is often unrealized due to the reduced power requirements per cell in consumer electric vehicle applications.  This might work for EV's but might not for specialized applications such as robotics which might demand extreme powers for extremely short bursts of time, on the order of 100ms to 1s.  In addition, mobile and highly dynamic robotic systems suffer greatly from weight.  In these scenarios it might make sense to use pouch cell technology to meet these requirements.

---

show how current drill batteries are insufficient for rigorous use
unknown bms cutoffs
high impedance causing sag, motors incapable of full speed




---
When considering cylinrical li ion cells, we can look to Molicel for the highest performing consumer cells.  Molicel has recently taken the consumer battery marker by storm, somehow beating large name manufacturers in their ability to make the highest power cells at very large energy densities.  I would like to learn more about this company and their methods, but it seems most battery technology and knowledge nowadays is locked behind closed doors due to fierce competition and the incredible rate at which the technology becomes obsolete.  Their cells are optimized for extreme power density without really compromising energy density.  Their most recent cell, the P45B outshines even the cells which put them on center stage, the P26A and the P42A.  The P45B is advertised to have a 15mΩ DCIR and measured by mooch to have a 10mΩ DCIR.  This is the best stuff on the market.

![[P45B.jpg]]
<div style="text-align: center;"> Datasheet of P45B li ion cell </div>


![[mooch.jpeg]]
<div style="text-align: center;"> Battery mooch test results for P45B</div>

---

When packaging these batteries into the humanoid, we must consider the sizing constraints of the chest cavity of the humanoid itself.  A spacefill was made to determine the largest number of cells that are capable of fitting inside the humanoid.  Given the 2170 geometry, the largest number of cells capable of fitting inside the humanoid is 50.

![[batspacefill.png]]
![[batspacefillhumanoid.png]]

Given that we would like the pack voltage to max out at around 60V, this would make a 15s pack ideal.  This means that a 15s3p pack would be the largest number of cells we can fit in parallel, making the size of the pack 45 cells instead of 50.  This would also give some space to integrate accompanying control electronics, so we will settle with 45 cells.

Using an estimate for the P45B's DCIR, we can run a spice simulation to see how well it would perform under a strenuous load case.  Something to note is that we are only going to be using the battery's DCIR in this spice simulation model, ignoring the second order and time dependent effects present in all electrochemical cells.  To understand more about these effects, check out this node: [[Measuring the Parameters of an Electrochemical Cell]].  Excluding these higher order effects will hurt the battery's apparent performance as they primarily function to sustain the battery's output voltage under load.  This could be an area that I could explore in the future, using advanced methods like EIS to better model potential batteries for the humanoid to estimate their performance during high power maneuvers.  For now, omitting these higher order effects will give a lower bound on the battery's performance.  More testing will reveal these parameters and make my simulations better reflect reality.

Given a 15s3p config, the equivalent DCIR of the pack would be 50mΩ assuming each cell has only 10mΩ DCIR.  Using a nominal cell voltage of 3.6v, we will have a resting voltage of 54V.  The expected power draw from the battery during a front flip was simulated in Elijah's MEng thesis, and is shown in the graph below:

![[batgraph.png]]

We can estimate the power demand of the larger spike on the right to be triangular and symmetric, with the peak being at 7kW.  The duration of the triangle wave is approximately 150ms.  We can model this power in LTSpice and run the battery 