import numpy as np


def equal(val1, val2, tol=1e-10):
    val1 = np.atleast_1d(val1)
    val2 = np.atleast_1d(val2)
    return np.linalg.norm(val1 - val2) < tol


def elementwise_equal(val1, val2, tol=1e-10):
    val1 = np.atleast_1d(val1)
    val2 = np.atleast_1d(val2)
    return np.all(np.abs(val1 - val2) < tol)