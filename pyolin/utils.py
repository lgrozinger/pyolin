import numpy
from math import log10 as log

import similaritymeasures as sm


def hill_lambda(ymin, ymax, k, n):
    return lambda x: ymin + (ymax - ymin) / (1 + (x / k)**n)


def hill_derivative(k, n):
    return lambda x: - n * (x / k)**(n - 1) / k / (1 + (x / k)**n)**2


def residuals(xs, ys, ymin, ymax):
    def loss(p):
        hill = hill_lambda(ymin, ymax, *p)
        predicted = numpy.array([hill(x) for x in xs])
        return numpy.array(ys - predicted)

    return loss


def log_residuals(xs, ys, ymin, ymax):
    def loss(p):
        hill = hill_lambda(ymin, ymax, *p)
        predicted = numpy.array([hill(x) for x in xs])
        return numpy.array(numpy.log(list(map(lambda x: x + 1, ys))) - numpy.log(predicted + 1))

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


# def y_agreement(gateA, gateB):
#     pA = gateA.params
#     pB = gateB.params

#     mina = pA["ymin"]
#     minb = pB["ymin"]

#     maxa = pA["ymax"]
#     maxb = pB["ymax"]

    


