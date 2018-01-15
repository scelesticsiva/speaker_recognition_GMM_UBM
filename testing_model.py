import matplotlib.pyplot as plt
import numpy as np
import argparse
import csv
from utils import calculate_likelihood

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map_file_name",type = str,\
                        help = "file after map adaptation",required = True)
    parser.add_argument("--test_csv_file",type = str,\
                        help = "csv file which containes mfcc from test audio",required = True)
    parser.add_argument("--N",type = int,\
                        help = "number of test datapoint",default = 1000)
    parser.add_argument("--D",type = int,\
                        help = "dimension of each datapoint",default = 13)
    parser.add_argument("--K",type = int,\
                        help = "number of clusters",default = 32)
    args = parser.parse_args()
    test(args)
    
def test(args):
    N = args.N
    D = args.D
    K = args.K
    data = np.zeros((N,D))
    count = 0
    map_adapted = np.load(args.map_file_name).item()
    #plt.plot(np.arange(len(map_adapted["likelihood"])),map_adapted["likelihood"])
    #plt.show()
    with open(args.test_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for i,each_d in enumerate(csv_reader):
            if i >= 100:
                count += 1
                if count > N:
                    break
                data[i-100,:] = each_d
    mu = map_adapted["mean"]
    cov = map_adapted["cov"]
    pi = map_adapted["pi"]
    print(calculate_likelihood(N,K,data,mu,cov,pi))
    
if __name__ == "__main__":
    main()