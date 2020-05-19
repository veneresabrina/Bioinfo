# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:34:19 2019

@author: vener

given the pat_ind file (containing the indeces of the chosen training samples)
and the feat_var file (containing the name of the chosen segments after the feature selection)
gives in output the train and test sets to perform machine learning

"""


def train_test_func(name1,name2):

    import csv
    import pandas as pd

    features = []
    with open(name1 , "r") as f:
        csv_reader = csv.reader(f)
        for row in f:
            features.append(row.strip('\n'))
    pat_ind = []
    with open(name2 , "r") as f2:
        csv_reader = csv.reader(f2)
        for row2 in f2:
            pat_ind.append(row2.strip('\n'))
    
    X = pd.read_csv("df_T.csv", usecols = features)
    X_train = X.iloc[pat_ind]

    indici = range(2000)    
    test_ind = [str(i) for i in indici if str(i) not in pat_ind]
    X_test = X.iloc[test_ind]
 
    
    return X_train, X_test

    
    
if __name__ == '__main__':
    
    import sys

    n1 = sys.argv[1]
    n2 = sys.argv[2]
    X_train, X_test = train_test_func(n1,n2)
