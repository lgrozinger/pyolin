import numpy
from math import log10 as log

def hill_lambda(ymin, ymax, k, n):
    return lambda x : ymin + (ymax - ymin) / (1 + (x / k)**n)

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
        return numpy.array(numpy.log(ys) - numpy.log(predicted))

    return loss

def au_to_rpu(au_median, af_median, standard_median):
    return (au_median - af_median) / (standard_median - af_median)

def c(au_median, af_median, standard_median):
    return (au_median - af_median) / (au_median * (standard_median - af_median))

def score(gateA, gateB, offset=0.0):
    ml = log((gateB.il - offset) / gateA.ol) if gateB.il > offset else - log(1 + gateA.ol)
    mh = log(gateA.oh / (gateB.ih - offset))
    return min(ml, mh)
