##test my_examples trig_functions

"""
This is a sample "example" script for SciPy's LU solver.

Example scripts are intended to provide useful starting points
for similar applications.

An example script is generally not as richly documented 
as a tutorial script because examples are adaptations of
real-world applications while tutorials are put together
primarily for an instructive purpose.

Here, we are solving a least-squares problem that results from
searching for the best-fit line through y=sin(2 * pi * x) from 0 to 1.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as spla


# Least-squares problem setup

num_points = 100

x = np.linspace(0., 1., num_points)
y = np.sin(2. * np.pi * x)

lsq_mtx = np.empty((num_points, 2))
lsq_mtx[:, 0] = x
lsq_mtx[:, 1] = 1.

lsq_rhs = y


# Assembly of the normal equations

mtx = lsq_mtx.T @ lsq_mtx
rhs = lsq_mtx.T @ lsq_rhs


# Apply SciPy's LU solver to the normal equations

lu, piv = spla.lu_factor(mtx)
sol = spla.lu_solve((lu, piv), rhs)


# Plot the quadratic function and the linear fit

plt.plot(x, y, label='Quadratic function')
plt.plot(x, lsq_mtx @ sol, label='Linear fit')
plt.legend()
plt.show()