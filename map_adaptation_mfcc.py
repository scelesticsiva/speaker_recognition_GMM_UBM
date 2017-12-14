#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:56:58 2017

@author: siva
"""

#MAP ADAPTATION
import numpy as np
import csv
from scipy.stats import multivariate_normal

#constants
D = 13
K = 1024
N = 100
RELEVANCE_FACTOR = 4
LIKELIHOOD_THRESHOLD = 0.01
MAX_ITERATIONS = 100

#file names
MAP_ADAPTATION_FILE = "map_adapted_file_40000"

#parameter initialization
z_n_k = np.zeros((N,K))
mu_k = np.zeros((K,D))
mu_new = np.zeros((K,D))
n_k = np.zeros((K,1))
pi_k = np.zeros((K,1))
cov_k = np.zeros((K,D,D))
data = np.zeros((N,D))


#loading the parameter data
with open("mean_40000.csv") as f_mean:
    reader_m = csv.reader(f_mean)
    for i,each in enumerate(reader_m):
        mu_k[i,:] = list(map(float,each))            
cov_k = np.load("cov_40000.npy")    
with open("pi_40000.csv") as f_pi:
    reader_pi = csv.reader(f_pi)
    for k,each in enumerate(reader_pi):
        pi_k[k,:] = float(each[0])

with open("mfcc_coefficients_test.csv") as f_data:
    reader_data = csv.reader(f_data)
    for i,each_data in enumerate(reader_data):
        if i == N:
           break
        data[i,:] = list(map(float,each_data))
    

#actual MAP adaptation
old_likelihood = 99999
new_likelihood = 0
likelihood_list = []
iterations = 0
final_dict = {}
while(abs(old_likelihood - new_likelihood) > LIKELIHOOD_THRESHOLD and iterations < MAX_ITERATIONS):
    iterations += 1
    old_likelihood = new_likelihood
    print("epoch:",iterations)
    num = np.zeros((K,1))
    for n in range(N):
        for k in range(K):
            num[k] = pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
        z_n_k[n] = np.reshape(num/np.sum(num),(K,))
        
    n_k = np.sum(z_n_k,axis = 0)
    n_k += 1e-10

    for i in range(K):
        temp = np.zeros((1,D))
        for n in range(N):
            temp += z_n_k[n][i]*data[n,:]
        mu_new[i] = (1/n_k[i])*temp

    adaptation_coefficient = n_k/(n_k + RELEVANCE_FACTOR)
    for k in range(K):
        mu_k[k] = (adaptation_coefficient[k] * mu_new[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])
    log_likelihood = 0
    for n in range(N):
        temp = 0
        for k in range(K):
            temp += pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
        log_likelihood += np.log(temp)
    new_likelihood = log_likelihood
    likelihood_list.append(log_likelihood)
    
    print(log_likelihood)
    break
    print("************************")
 
#saving the final adapted mean
final_dict = {"mean":mu_k,"cov":cov_k,"pi":pi_k,"likelihood":np.array(likelihood_list)}
np.save(MAP_ADAPTATION_FILE,final_dict)
    