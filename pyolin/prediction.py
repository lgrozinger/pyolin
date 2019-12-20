from pyolin.utils import hill_derivative
from pyolin.utils import hill_lambda

import numpy
from numpy.linalg import norm


def boundary_curves(gate, leash_length):
    curve = gate.numpy_curve()
    ub = []
    lb = []
    f = gate.normalised_hill_function
    dydx = hill_derivative(gate.params["K"], gate.params["n"])
    for (x, y) in curve:
        normal_vector = numpy.array([-dydx(x), 1])
        print(norm(normal_vector))
        normal_vector = normal_vector / norm(normal_vector)
        print(norm(normal_vector))
        leash_vector = normal_vector * leash_length

        ub_x = x + leash_vector[0]
        ub_y = f(x) + leash_vector[1]
        ub.append((ub_x, ub_y))

        lb_x = x - leash_vector[0]
        lb_y = f(x) - leash_vector[1]
        lb.append((lb_x, lb_y))

    return ub, lb
        
