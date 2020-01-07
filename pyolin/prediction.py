from pyolin.utils import hill_derivative
from pyolin.utils import hill_lambda

from pyolin.analysis import frechet

import numpy
from numpy.linalg import norm

import matplotlib.pyplot as plt

def do_prediction(gateA, gateB, reference_gates, unknown_gates):
    for reference, actual in zip(reference_gates, unknown_gates):
        ub, lb = prediction(gateA, gateB, reference)
        axes = actual.rpuplot().axes[0]
        axes.plot([x for (x, y) in ub], [y for (x, y) in ub])
        axes.plot([x for (x, y) in lb], [y for (x, y) in lb])
        plt.show()
        plt.figure()


def prediction(from_gate, foreign_gate, reference_gate):
    """
    Based on the relationship between from_gate and foreign_gate,
    derive upper and lower bounds for the reference_gate in the
    foreign context.
    """
    leash = frechet(from_gate, foreign_gate)
    ub, lb = boundary_curves(reference_gate, leash)

    def scale_x(x):
        xmin = min(foreign_gate.rpu_in)
        xmax = max(foreign_gate.rpu_in)
        return x * (xmax - xmin) + xmin

    def scale_y(y):
        ymin = min(foreign_gate.rpu_out)
        ymax = max(foreign_gate.rpu_out)
        return y * (ymax - ymin) + ymin

    ub = [(scale_x(x), scale_y(y)) for (x, y) in ub]
    lb = [(scale_x(x), scale_y(y)) for (x, y) in lb]
    return ub, lb


def coerce_positive(x):
    result = x if x > 0.0 else 0.0
    return result


def boundary_curves(gate, leash_length):
    curve = gate.numpy_curve()
    ub = []
    lb = []
    f = gate.normalised_hill_function
    dydx = hill_derivative(gate.params["K"], gate.params["n"])
    for (x, y) in curve:
        normal_vector = numpy.array([-dydx(x), 1])
        normal_vector = normal_vector / norm(normal_vector)
        leash_vector = normal_vector * leash_length

        ub_x = x + leash_vector[0]
        ub_y = f(x) + leash_vector[1]
        ub.append((ub_x, ub_y))

        lb_x = x - leash_vector[0]
        lb_y = f(x) - leash_vector[1]
        lb.append((lb_x, lb_y))

    return ub, lb
