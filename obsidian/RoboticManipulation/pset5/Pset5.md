5.6) a) The green block is falling past the red block because the simulated contact forces are updating too slowly.  The time it takes for the green block to deeply penetrate the red block is larger than the simulation timestep.  This leads to contact forces that do not well represent the dynamics we expect.
d) μ_1 must be greater than tan(a) while μ_2 must be less than tan(a).  This does not depend on either of the masses.

6.1) a) I would constrain the X and Y directions and the rotation about y.  X needs to be constrained otherwise the gripper won't close exactly on the center of the handle.  Y needs to be constrained so we don't hit the door or miss the handle.  Z can be left relatively unconstrained since the handle can be gripped equally along this length.  Rotation about Y should also be constrained because we want the gripper to actuate opposite the surface normals to grip well.  Small angles in X and Z should still grip the handle.

b)

Minimize over decision variables {q} the quantity of ||q - q_nom||^2, subject to:

(p_WH['x'] - f_p(q)['x'])^2 <= tolerance^2
(p_WH['y'] - f_p(q)['y'])^2 <= tolerance^2

(R_WH['y'] - f_R(q)['y'])^2 <= tolerance^2

6.2) b) If there is no path to the goal, RRT will never give any warning because all it can do is search for the path or return an answer, which it never will.  If there is a path to the goal, RRT will find it in the limit as iterations approaches infinity.  This is because for there to be a path to the goal, there exist some probability that RRT samples a point along this path that is in reach of the tree for every iteration.  With enough iterations and progress towards the goal, RRT will reach it.

6.3) 
a) 10 and 15
b) qnear is the parent with the standard RRT algorithm.  The parent that encodes the smallest distance from qstart is qstart.

survey
B is for Basis
