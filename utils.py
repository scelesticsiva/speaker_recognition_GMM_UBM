import numpy as np

def unit_gaussian(x,mu,sigma):
    inv_cov = np.linalg.inv(sigma)
    exponent = np.exp((-0.5)*np.dot(np.dot((x - mu),inv_cov),(x - mu).T))
    z = 1/(((2*np.pi))*(np.linalg.det(sigma)**0.5))
    return z*exponent
    
def calculate_likelihood(N,K,data,mu_k,cov_k,pi_k):
    log_likelihood = 0
    for n in range(N):
        temp = 0
        for k in range(K):
            #temp += pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
            temp += pi_k[k] * (unit_gaussian(data[n],mu_k[k],cov_k[k]))
        log_likelihood += np.log(temp)
    return log_likelihood