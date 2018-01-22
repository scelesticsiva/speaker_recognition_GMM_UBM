import matplotlib.pyplot as plt
import numpy as np
import csv
from utils import unit_gaussian
from k_means import k_means
from scipy.stats import multivariate_normal

def train_ubm(args):
    data = []
    N = args.N
    D = args.D
    K = args.K
    iterations = 0
    with open(args.csv_file,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        for count,datum in enumerate(reader):
            if count < N:
                data.append(datum)
            else:
                break
    
    data = np.array(data).astype(np.float)
    #print(data)
    for_cov = []
    for d in range(D):
        for_cov.append(data[:,d])
    
    z_n_k = np.zeros((N,K))
    mu_k = np.zeros((K,D))
    cov_k = np.zeros((K,D,D))
    pi_k = np.zeros((K,1))
    #n_k = np.zeros((K,1))
    
    old_likelihood = 0
    new_likelihood = 9999
    likelihood = []
    
    
    #mu_k = np.random.randn(K,D)
    #cov_k = np.array([np.cov(for_cov)]*K)
    #pi_k = np.reshape(np.array([0.5]*K),(K,1))
    mu_k,cov_k,pi_k = k_means(data,N,K,D,100)
    cov_k += 0.001*np.eye(cov_k[0].shape[0])
    
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
        #print("--mu",mu_k)
        for i in range(K):
            #temp_1 = np.zeros((D,D))
            cov_k[i] = np.dot(np.dot((data - mu_k[i,:]).T, np.diag(z_n_k[:,i])), (data-mu_k[i])) / n_k[i]
            cov_k[i] = cov_k[i] + 0.001*np.eye(cov_k[i].shape[0])
        #print("--cov",cov_k)
        for i in range(K):
            pi_k[i] = n_k[i]/N
        #print("--pi",pi_k)
        
    def e_step():
        num = np.zeros((K,1))
        #print(cov_k)
        for n in range(N):
            for k in range(K):
                #num[k] = pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
                num[k] = pi_k[k] * (unit_gaussian(data[n],mu_k[k],cov_k[k]))
            z_n_k[n] = np.reshape(num/np.sum(num),(K,))
        #print("-->z",z_n_k[n])
        
    def calculate_likelihood():
        log_likelihood = 0
        for n in range(N):
            temp = 0
            for k in range(K):
                #temp += pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
                temp += pi_k[k] * (unit_gaussian(data[n],mu_k[k],cov_k[k]))
            log_likelihood += np.log(temp)
        return log_likelihood
        
        
    while(abs(old_likelihood - new_likelihood)>args.likelihood_threshold and iterations < args.max_iterations):
        iterations += 1
        old_likelihood = new_likelihood
        e_step()
        m_step()
        new_likelihood = calculate_likelihood()
        likelihood.append(new_likelihood)
        print("iterations:{0}|likelihood:{1}".format(str(iterations),str(new_likelihood)))
        #plot(z_n_k)
        
    print(likelihood)
    
    final_dict = {"mean":mu_k,"cov":cov_k,"pi":pi_k,"likelihood":likelihood}
    np.save(args.ubm_file_name,final_dict)