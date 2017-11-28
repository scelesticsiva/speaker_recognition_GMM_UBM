import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal

N = 300
K = 5
D = 2
ITERATIONS = 300

data = np.random.multivariate_normal([13,13],[[15,0],[0,17]],int(N))
#data1 = np.random.multivariate_normal([11,11],[[23,12],[8,12]],int(N/3))
#data = np.append(data,data1,axis = 0)
#data1 = np.random.multivariate_normal([9,9],[[8,2],[3,10]],int(N/3))
#data = np.append(data,data1,axis = 0)

plt.scatter(data[:,0],data[:,1])
plt.show()

z_n_k = np.zeros((N,K))
mu_k = np.zeros((K,D))
cov_k = np.zeros((K,D,D))
pi_k = np.zeros((K,1))
n_k = np.zeros((K,1))

#np.random.seed(11909)

mu_k = np.random.randn(K,D)
cov_k = np.array([np.cov(data[:,0],data[:,1])]*K)
pi_k = np.reshape(np.array([0.5,0.5,0.5,0.5,0.5]),(K,1))

def plot(z_n_k):
    plt.figure()
    color_array = ["r","g","b","y","black"]
    for i,each in enumerate(data):
        plt.scatter(each[0],each[1],c = color_array[np.argmax(z_n_k[i,:])],edgecolor = color_array[np.argmax(z_n_k[i,:])])
    plt.show()

def m_step():
    n_k = np.sum(z_n_k,axis = 0)
    #print("--->",n_k)
    for i in range(K):
        temp = np.zeros((1,D))
        for n in range(N):
            temp += z_n_k[n][i]*data[n,:]
        mu_k[i] = (1/n_k[i])*temp
    print("--mu",mu_k)
    for i in range(K):
        temp_1 = np.zeros((D,D))
        cov_k[i] = np.dot(np.dot((data - mu_k[i,:]).T, np.diag(z_n_k[:,i])), (data-mu_k[i])) / n_k[i]
        
    #print("--cov",cov_k)
    for i in range(K):
        pi_k[i] = n_k[i]/N
    #print("--pi",pi_k)

def e_step():
    num = np.zeros((K,1))
    for n in range(N):
        for k in range(K):
            num[k] = pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
        z_n_k[n] = np.reshape(num/np.sum(num),(K,))
    #print("-->z",z_n_k[n])
    
    
for i in range(ITERATIONS):
    e_step()
    m_step()
    plot(z_n_k)

