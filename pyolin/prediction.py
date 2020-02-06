from pyolin.utils import hill_derivative
from pyolin.utils import normalise

import numpy
from numpy.linalg import norm
from numpy import array
from numpy import exp
from math import log as ln

from similaritymeasures import frechet_dist


def max_y_displacement(A, B):
    """
    Calculates the maximum absolute distance between corresponding y
    values of A and B.
    """
    a = A.points[:, 1]
    b = B.points[:, 1]
    return max(abs(a - b))


def y_displacement_prediction(A, B, reference):
    """
    Prediction by tracing ±max_y_displacement from reference.
    """
    distance = max_y_displacement(A, B)
    x = B.points[:, 0]
    upper_curve = numpy.array([x, reference.points[:, 1] + distance]).T
    lower_curve = numpy.array([x, reference.points[:, 1] - distance]).T
    return upper_curve, lower_curve


def logy_displacement_prediction(A, B, reference):
    """
    Prediction by tracing ±max_y_displacement from reference.
    """
    upper_curve, lower_curve = y_displacement_prediction(A.log(), B.log(), reference.log())
    return exp(upper_curve), exp(lower_curve)


def max_euclidean_distance(A, B):
    """
    Calculates the maximum euclidean distance between the
    corresponding points of A and B.
    """
    a = A.points
    b = B.points
    return max(numpy.sqrt(numpy.sum((a - b)**2, axis=1)))


def euclidean_prediction(A, B, reference):
    """
    Prediction by tracing the normal to the reference curve at
    ±max_euclidean_distance.
    """
    distance = max_euclidean_distance(A, B)
    return boundary_curves(reference, distance)


def log_euclidean_prediction(A, B, reference):
    """
    Prediction by tracing the normal to the reference curve at
    ±max_euclidean_distance. First, log-transforming the data.
    """
    Alog = A.log()
    Blog = B.log()
    reflog = reference.log()

    distance = max_euclidean_distance(Alog, Blog)
    upper_curve, lower_curve = boundary_curves(reflog, distance)
    return exp(upper_curve), exp(lower_curve)


# prediction
def prediction(A, B, reference):
    """
    The prediction algorithm:

    1. Compute the log transformed curves for the gates.
    2. Compute An and Bn, the normalised hill functions for A and B.
    3. Compute the frechet distance between An and Bn.
    4. Obtain the upper and lower bound curves for the log transformed
    normalised reference curve.
    5. Scale the bounds back to linear unnormalised space by
    renormalising to a scaled ymin and ymax interval.
    """
    An = A.log().normal(lower=(1.0, 1.0), upper=(2.0, 2.0))
    Bn = B.log().normal(lower=(1.0, 1.0), upper=(2.0, 2.0))
    refn = reference.log().normal(lower=(1.0, 1.0), upper=(2.0, 2.0))

    leash = frechet_dist(An.points, Bn.points)

    scaled_ymin = ln(reference.ymin * B.ymin / A.ymin)
    scaled_ymax = ln(reference.ymax * B.ymax / A.ymax)

    upper_curve, lower_curve = boundary_curves(refn, leash)
    upper_curve = array([upper_curve[:, 0], normalise(upper_curve[:, 1], scaled_ymin, scaled_ymax)]).T
    lower_curve = array([lower_curve[:, 0], normalise(lower_curve[:, 1], scaled_ymin, scaled_ymax)]).T

    upper_curve = array([upper_curve[:, 0], exp(upper_curve[:, 1])]).T
    lower_curve = array([lower_curve[:, 0], exp(lower_curve[:, 1])]).T
    return upper_curve, lower_curve


def boundary_curves(gate, leash_length):
    curve = gate.points
    ub = []
    lb = []
    f = gate.hill_function
    dydx = hill_derivative(gate.K, gate.n)
    for x, y in curve:
        normal_vector = numpy.array([-dydx(x), 1])
        normal_vector = normal_vector / norm(normal_vector)
        leash_vector = normal_vector * leash_length

        ub_x = x + leash_vector[0]
        ub_y = f(x) + leash_vector[1]
        ub.append([ub_x, ub_y])

        lb_x = x - leash_vector[0]
        lb_y = f(x) - leash_vector[1]
        lb.append([lb_x, lb_y])

    return numpy.array(ub), numpy.array(lb)
