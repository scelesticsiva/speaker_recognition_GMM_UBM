#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 23:12:30 2018

@author: siva
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.cluster import KMeans
#K-means

#N = 300
#K = 3
#D = 2
#MAX_ITERATIONS = 1000

def distance(array_1,point_2):
    return np.mean(((array_1 - point_2)**2),axis = 1)
    
#def plot(data,cluster_assignments,centroids):
#    plt.figure()
#    plt.scatter(data[cluster_assignments == 0,0],data[cluster_assignments == 0,1],c = "r")
#    plt.scatter(data[cluster_assignments == 1,0],data[cluster_assignments == 1,1],c = "green")
#    plt.scatter(data[cluster_assignments == 2,0],data[cluster_assignments == 2,1],c = "orange")
#    plt.scatter(centroids[:,0],centroids[:,1],c = "y")
#    plt.show()
#
#data = np.random.multivariate_normal([3,3],[[1,0],[0,1]],100)
#data = np.append(data,np.random.multivariate_normal([1,1],[[1,0],[0,1]],100),axis = 0)
#data = np.append(data,np.random.multivariate_normal([-2,-2],[[1,0],[0,1]],100),axis = 0)
#random.shuffle(data)
#plt.scatter(data[:,0],data[:,1])

#initialization
def k_means_1(data,N,K,D,MAX_ITERATIONS):
    centroid_distances = np.zeros((N,K))
    cov = np.zeros((K,D,D))
    pi = np.zeros((K,1))
    
    centroid_positions = np.random.randint(N,size = K)
    centroids = data[centroid_positions]
    prev_centroids = np.zeros(centroids.shape)
    #print(centroids)
    itr = 0
    while not np.array_equal(centroids,prev_centroids) and itr <= MAX_ITERATIONS:
        for k in range(K):
            centroid_distances[:,k] = distance(data,centroids[k,:])
        cluster_assignments = np.argmin(centroid_distances,axis = 1)
        prev_centroids = centroids[:]
        for k in range(K):
            centroids[k,:] = np.mean(data[cluster_assignments == k])
        itr += 1
    for k in range(K):
        cov[k] = np.cov(data[cluster_assignments == k].T)
        pi[k] = data[cluster_assignments == k].shape[0]/N
    #plot(data,cluster_assignments,centroids)
    print("finished kmeans")
    return centroids,cov,pi
    
def k_means(data,N,K,D,MAX_ITERATIONS):
    cov = np.zeros((K,D,D))
    pi = np.zeros((K,1))
    kmeans = KMeans(n_clusters = K).fit(data)
    for k in range(K):
        cov[k] = np.cov(data[kmeans.labels_ == k].T)
        pi[k] = data[kmeans.labels_ == k].shape[0]/N
    print(kmeans.cluster_centers_.shape,cov.shape,pi.shape)
    #plot(data,kmeans.labels_,kmeans.cluster_centers_)
    #print(cov)
    return kmeans.cluster_centers_,cov,pi
#k_means(data,N,K,D,MAX_ITERATIONS)

                            



