#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 23:12:30 2018

@author: siva
"""

import numpy as np
import matplotlib.pyplot as plt
import random
#K-means

N = 300
K = 3
D = 2
MAX_ITERATIONS = 1000

def distance(point_1,point_2):
    return np.mean((point_1 - point_2)**2)
    
def plot(data,cluster_assignments,centroids):
    plt.figure()
    plt.scatter(data[cluster_assignments == 0,0],data[cluster_assignments == 0,1],c = "r")
    plt.scatter(data[cluster_assignments == 1,0],data[cluster_assignments == 1,1],c = "green")
    plt.scatter(data[cluster_assignments == 2,0],data[cluster_assignments == 2,1],c = "orange")
    plt.scatter(centroids[:,0],centroids[:,1],c = "y")
    plt.show()

data = np.random.multivariate_normal([5,5],[[1,0],[0,1]],100)
data = np.append(data,np.random.multivariate_normal([1,1],[[1,0],[0,1]],100),axis = 0)
data = np.append(data,np.random.multivariate_normal([-3,-3],[[1,0],[0,1]],100),axis = 0)
random.shuffle(data)
plt.scatter(data[:,0],data[:,1])

#initialization
for i in range(10):
    mean = np.zeros((K,D,D))
    cluster_assignments = np.zeros((N))
    centroid_distances = np.zeros((N,K))
    
    centroid_positions = np.random.randint(N,size = K)
    centroids = data[centroid_positions]
    prev_centroids = np.zeros(centroids.shape)
    print(centroids)
    itr = 0
    while not np.array_equal(centroids,prev_centroids) and itr <= MAX_ITERATIONS:
        for n in range(N):
            for k in range(K):
                centroid_distances[n,k] = distance(data[n,:],centroids[k,:])
            cluster_assignments[n] = np.argmin(centroid_distances[n,:])
        prev_centroids = centroids[:]
        for k in range(K):
            centroids[k,:] = np.mean(data[cluster_assignments == k])
        itr += 1
    plot(data,cluster_assignments,centroids)
                            



