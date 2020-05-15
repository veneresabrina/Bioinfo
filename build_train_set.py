# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:24:32 2020

@author: vener

split train set randomly just once to keep track of the patients that will 
be used in the training fase, the same 1500 patients will be used for any of
the variance values used.

"""
import csv
import random

random.seed(42)
# select train set randomly
a = list(range(2000))
random.shuffle(a)
rand_pat = a[:1500]

with open("train_test_set/pat_ind_train.txt", "w") as output:
    for p in rand_pat:
        writer = csv.writer(output, lineterminator='\n')            
        writer.writerow([p])