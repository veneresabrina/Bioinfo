# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:11:21 2019

@author: vener
"""

import pandas as pd
from sklearn.feature_selection import VarianceThreshold
#from sklearn.model_selection import train_test_split
import sys
import csv


if len(sys.argv) < 2:
    print("The algorithm needs 1 argument from the command line: the variance value")
    sys.exit(1)  # abort because of error



def variance_threshold_selector(data, threshold):
    cont = 0
    try:
        selector = VarianceThreshold(threshold)
        selector.fit(data)    
        with open("train_test_set/%.3f_feat_var.txt" % threshold, "a") as output:
            for name in data.columns[selector.get_support(indices=True)]:
                writer = csv.writer(output, lineterminator='\n')            
                writer.writerow([name])
                cont += 1
        print(">> %d features added." % cont)
        
    except Exception as e:
        print(e)
        print(">> No features added.")
        pass

    return cont


var = float(sys.argv[1])

num_feat = 0

features = []
with open("segments_in_df.txt", "r") as f:
    csv_reader = csv.reader(f)
    for row in f:
        row = row.rstrip('\n')
        row = row.rstrip('\r')
        features.append(row)

step = 20000
r = range(0,len(features),step)
r2 = range(step,len(features),step)
r2.append(len(features))

rand_pat = []
with open("train_test_set/pat_ind_train.txt", "r") as f:
    for line in f:
        rand_pat.append(f.readline())

for i in range(len(r)):
    # selecting only first chunk of features and the 1500 random patients
    X = pd.read_csv("df_T.csv", usecols = features[r[i]:r2[i]])
    X = X.iloc[rand_pat]
    
    cont = variance_threshold_selector(X, var)
    num_feat += cont
    print("%d/%d chunks done, there are %d features in the file" %(i+1,len(r), num_feat))
    
perc = (float(num_feat)/r2[-1]) * 100
print("final percentage of retained features over the total = %.2f" % perc)
