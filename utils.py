import numpy as np

def unit_gaussian(x,mu,sigma):
    inv_cov = np.linalg.inv(sigma)
    exponent = np.exp((-0.5)*np.dot(np.dot((x - mu),inv_cov),(x - mu).T))
    z = 1/(((2*np.pi))*(np.linalg.det(sigma)**0.5))
    return z*exponent