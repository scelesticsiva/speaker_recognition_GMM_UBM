lsimport numpy as np
import csv
from utils import unit_gaussian

def map_adaptation(args):
    print("loading the required files...")
    #loading the parameter data
    N = args.N
    D = args.D
    K = args.K
    
    z_n_k = np.zeros((N,K))
    mu_k = np.zeros((K,D))
    mu_new = np.zeros((K,D))
    n_k = np.zeros((K,1))
    pi_k = np.zeros((K,1))
    cov_k = np.zeros((K,D,D))
    data = np.zeros((N,D))
    
    ubm = np.load(args.ubm_file).item()
    mu_k = ubm["mean"]
    cov_k = ubm["cov"]
    pi_k = ubm["pi"]
    
    with open(args.csv_file) as f_data:
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
    while(abs(old_likelihood - new_likelihood) > args.likelihood_threshold and iterations < args.max_iterations):
    #while(iterations < MAX_ITERATIONS):
        iterations += 1
        old_likelihood = new_likelihood
        print("epoch:",iterations)
        num = np.zeros((K,1))
        for n in range(N):
            for k in range(K):
                #num[k] = pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
                num[k] = pi_k[k] * (unit_gaussian(data[n],mu_k[k],cov_k[k]))
            z_n_k[n] = np.reshape(num/np.sum(num),(K,))
        print("finished E step...")    
        n_k = np.sum(z_n_k,axis = 0)
        n_k += 1e-10
    
        for i in range(K):
            temp = np.zeros((1,D))
            for n in range(N):
                temp += z_n_k[n][i]*data[n,:]
            mu_new[i] = (1/n_k[i])*temp
    
        adaptation_coefficient = n_k/(n_k + args.rf)
        print("beginning adaptation...")
        for k in range(K):
            mu_k[k] = (adaptation_coefficient[k] * mu_new[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])
        log_likelihood = 0
        print("calculating likelihood")
        for n in range(N):
            temp = 0
            for k in range(K):
                #temp += pi_k[k] * (multivariate_normal.pdf(data[n],mu_k[k],cov_k[k]))
                temp += pi_k[k] * (unit_gaussian(data[n],mu_k[k],cov_k[k]))
            log_likelihood += np.log(temp)
        new_likelihood = log_likelihood
        likelihood_list.append(log_likelihood)
        
        print(log_likelihood)
        print("************************")
     
    #saving the final adapted mean
    final_dict = {"mean":mu_k,"cov":cov_k,"pi":pi_k,"likelihood":np.array(likelihood_list)}
    np.save(args.map_file_name,final_dict)