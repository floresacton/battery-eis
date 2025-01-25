2.1)
	b. Adding a gearbox does two things to make the dynamics of the system less relevant in comparison to the motor dynamics.  The higher gear ratio gives more torque to the output which can give more control authority over a large heavy robot arm.  Despite this, more torque could also be achieved with higher gains (in code) and is not the main reason why the gearbox makes the system more stable.  The massive inertia, scaled by the square of the gearbox, makes the dynamics of the robot arm much less relevant to the overall inertia of the system.  Coupling this with the fact that the motor has a maximum output speed will make the system appear more like a first order system instead of a second order system which is much easier to make stable.
	
3.5)
	b. The jacobian is invertible only when q1 is not 0 or pi. In the case where q1 = 0, the matrix degenerates into [-2sin(q0), -sin(q0)](https://www.gradescope.com/courses/609893/assignments/3327549/submissions/194723180?view=files#Test%20forward%20kinematics) which has two column vectors along the same direction. When q1 = pi, the matrix becomes [0, sin(q0)](https://www.gradescope.com/courses/609893/assignments/3327549/submissions/194723180?view=files#Test%20forward%20kinematics) which has a zero column vector. In either case, the matrix is not full rank and therefore cannot immediately move in any arbitrary direction and is therefore singular.

3.6)
	a. (2x3)
	b. Any square Jacobian that is full rank will have an inverse that can be computed.  Any non square matrix or any square matrix that is not full rank can have a pseudo inverse computed.
	c. The ellipsoid will collapse to a line.

Survey:
Kuka iiwa Kinematics