# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:01:51 2020

@author: vener

printing the number of features from each set previously obtained

"""

variances = ['0.070', '0.080', '0.090','0.095','0.100']
for var in variances:
    filename = 'train_test_set/' + var + '_feat_var.txt'
    with open(filename,'r') as f:
        content = f.readlines()
    print('for variance: %s there are %d fetures (segments)' %(var, len(content)))
bases = ['2','3','5','10','15','20']
for b in bases:
    filename = 'train_test_set/X_train_basi' + b + '.csv'
    with open(filename,'r') as f:
        firstline = f.readline().split(',')
        firstline.pop(0)
    print('for %s bases there are %d fetures (segments)' %(b, len(firstline)))
        
