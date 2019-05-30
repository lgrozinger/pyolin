import numpy

def hill_lambda(ymin, ymax, k, n):
    return lambda x : ymin + (ymax - ymin) / (1 + (x / k)**n)

def residuals(xs, ys, ymin, ymax):
    def loss(p):
        hill = hill_lambda(ymin, ymax, *p)
        predicted = numpy.array([hill(x) for x in xs])
        return numpy.array(ys - predicted)

    return loss

def au_to_rpu(au_median, af_median, standard_median):
    return (au_median - af_median) / (standard_median - af_median)

def c(au_median, af_median, standard_median):
    return (au_median - af_median) / (au_median * (standard_median - af_median))
