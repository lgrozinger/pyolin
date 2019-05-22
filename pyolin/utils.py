def hill_lambda(ymin, ymax, k, n):
    return lambda x : ymin + (ymax - ymin) / (1 + (x / k)^n)
