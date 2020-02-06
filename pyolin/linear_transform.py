import numpy

from scipy.optimize import minimize


def optim_matrix(A, B):

    X = A.points.T
    Y = B.points.T
    init_p = numpy.random.random(4)

    def f(p):
        Z = numpy.array(p)
        Z.shape = (2, 2)
        y = numpy.dot(Z, X)

        return numpy.linalg.norm(y - Y)

    return minimize(f, init_p)


def linear_transform_prediction(A, B, reference):
    solution = optim_matrix(A, B)

    if solution.success:
        Z = solution.x
        Z.shape = (2, 2)
        guess_points = numpy.dot(Z, reference.points.T)
        return guess_points
    else:
        print(f"Linear transform for {A.name} to {B.name} could not be found.")


def loglinear_transform_prediction(A, B, reference):
    solution = optim_matrix(A.log(), B.log())

    if solution.success:
        Z = solution.x
        Z.shape = (2, 2)
        guess_points = numpy.dot(Z, reference.log().points.T)
        return numpy.exp(guess_points)
    else:
        print(f"Linear transform for {A.name} to {B.name} could not be found.")

        
