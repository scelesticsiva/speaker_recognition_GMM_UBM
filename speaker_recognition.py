#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:11:07 2018

@author: siva
"""

#Creating UBM model and MAP adaptation
import argparse
from UBM import train_ubm
from MAP_adapt import map_adaptation
#from scipy.stats import multivariate_normal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N",type = int,\
                        help = "number of datapoints from csv file",default = 10000)
    parser.add_argument("--D",type = int,\
                        help = "dimension of each datapoint",default = 13)
    parser.add_argument("--K",type = int,\
                        help = "number of clusters/gaussians",default = 32)
    parser.add_argument("--likelihood_threshold",type = float,\
                        help = "criteria for stopping EM",default = 1e-20)
    parser.add_argument("--max_iterations",type = int,\
                        help = "maximum number of EM iterations",default = 300)
    parser.add_argument("--csv_file",type = str,\
                        help = "file where mfcc coefficients are stored",required = True)
    parser.add_argument("--ubm_file_name",type = str,\
                        help = "file name for the UBM numpy file",default = "ubm_file")
    parser.add_argument("--map_file_name",type = str,\
                        help = "file name for the numpy file after map adaptation", default = "map_file")
    parser.add_argument("--rf",type = int,\
                        help = "relevance factor for map adaptation",default = 16)
    parser.add_argument("--operation",type = str,\
                        help = "ubm or map adaptation",default = "ubm")
    parser.add_argument("--ubm_file",type = str,\
                        help = "numpy file for trained UBM model",default = "ubm_file.npy")
    
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":
    arguments = main()
    if arguments.operation == "ubm":
        train_ubm(arguments)
    if arguments.operation == "map":
        map_adaptation(arguments)
    
    