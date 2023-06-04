import numpy as np
import scipy.linalg as spla
import lsdo_test as lt


##test all_tests
def test_1x1():
    mtx = np.ones((1, 1))
    rhs = np.ones(1)

    lu, piv = spla.lu_factor(mtx)
    sol = spla.lu_solve((lu, piv), rhs)

    assert lt.equal(sol, 1.0, tol=1e-3)

##test all_tests
def test_2x2():
    mtx = np.array([[1., 2.], [3., 4.]])
    rhs = np.array([2., 5.])

    lu, piv = spla.lu_factor(mtx)
    sol = spla.lu_solve((lu, piv), rhs)

    assert lt.elementwise_equal(sol, [1.0, 0.5], tol=1e-3)