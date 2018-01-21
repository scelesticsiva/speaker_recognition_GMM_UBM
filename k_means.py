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

N = 200
K = 2
D = 2

def distance(point_1,point_2):
    return np.sqrt(np.mean(point_1 - point_2)**2)
    
def plot(data,cluster_assignments,centroids):
    plt.figure()
    plt.scatter(data[cluster_assignments[:,0]==1,0],data[cluster_assignments[:,0]==1,1],c = "r")
    plt.scatter(data[cluster_assignments[:,1]==1,0],data[cluster_assignments[:,1]==1,1],c = "b")
    plt.scatter(centroids[:,0],centroids[:,1],c = "y")
    plt.show()

data = np.random.multivariate_normal([3,3],[[1,0],[0,1]],100)
data = np.append(data,np.random.multivariate_normal([1,1],[[1,0],[0,1]],100),axis = 0)
random.shuffle(data)
plt.scatter(data[:,0],data[:,1])

#initialization
mean = np.zeros((K,D,D))
cluster_assignments = np.zeros((N,K))
centroid_distances = np.zeros((N,K))

centroid_positions = np.random.randint(N+1,size = K)
centroids = data[centroid_positions]
print(centroids)
for i in range(1000):
    if i%10 == 0:
        plot(data,cluster_assignments,centroids)
        print(centroids)
    for n in range(N):
        for k in range(K):
            centroid_distances[n,k] = distance(data[n],centroids[k])
        cluster_assignments[n,np.argmin(centroid_distances[n,:])] = 1
    for k in range(K):
        centroids[k,:] = np.mean(data[cluster_assignments[:,k] == 1])
                            



