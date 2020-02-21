import numpy
from math import log10 as log
from math import isnan

import similaritymeasures as sm


def normalise(iterable, a, b):
    "Normalise the values of iterable in [a, b]"
    xmin = min(iterable)
    xmax = max(iterable)

    def transform(x):
        return a + (b - a) * (x - xmin) / (xmax - xmin)

    return [transform(x) for x in iterable]


def hill_lambda(ymin, ymax, k, n):
    def h(x):
        return ymin + (ymax - ymin) / (1 + pow(x / k, n))

    return h


def hill_derivative(k, n):
    return lambda x: - n * (x / k)**(n - 1) / k / (1 + (x / k)**n)**2


def log_residuals(xs, ys, ymin, ymax):
    def loss(p):
        hill = hill_lambda(ymin, ymax, *p)
        predicted = numpy.array([hill(x) + 1 for x in xs])
        actual = numpy.array([y + 1 for y in ys])
        return numpy.log(actual) - numpy.log(predicted)

    return loss


def residuals(xs, ys, ymin, ymax):
    def loss(p):
        hill = hill_lambda(ymin, ymax, *p)
        predicted = numpy.array([hill(x) for x in xs])
        # if any(map(isnan, predicted)):
        #     print("NaN detected:")
        #     print(predicted)
        #     print(ymin, ymax, *p)
        return numpy.array(ys - predicted)

    return loss


def au_to_rpu(au_median, af_median, standard_median):
    return (au_median - af_median) / (standard_median - af_median)


def c(au_median, af_median, standard_median):
    return (au_median - af_median) / (au_median * (standard_median - af_median))


def score(gateA, gateB, offset=0.0):
    ml = log((gateB.il - offset) / gateA.ol) if gateB.il >= offset else - log(1 + gateA.ol)
    mh = log(gateA.oh / (gateB.ih - offset)) if gateB.ih >= offset else - log(1 + gateA.oh)
    return min(ml, mh)


def shape_agreement(gateA, gateB):
    pA = gateA.params
    pB = gateB.params
    δA = hill_derivative(pA["K"], pA["n"])
    δB = hill_derivative(pB["K"], pB["n"])

    xs = gateA.xs
    ysa = [δA(x) for x in xs]
    ysb = [δB(x) for x in xs]

    return sum(map(lambda a, b: (a - b)**2, ysa, ysb))


def similarity(gateA, gateB):
    a_range = log(gateA.params["ymax"]) - log(gateA.params["ymin"])
    b_range = log(gateB.params["ymax"]) - log(gateB.params["ymin"])
    print(a_range)
    print(b_range)

    a_log_normal_ys = map(lambda y: y / a_range, map(log, gateA.ys))
    b_log_normal_ys = map(lambda y: y / b_range, map(log, gateB.ys))
    a_curve = numpy.array([[x, y] for (x, y) in zip(gateA.xs, a_log_normal_ys)])
    b_curve = numpy.array([[x, y] for (x, y) in zip(gateB.xs, b_log_normal_ys)])
    print(a_curve)
    print(b_curve)

    return sm.frechet_dist(a_curve, b_curve)
