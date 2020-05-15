# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:45:52 2019

@author: vener
"""
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from train_test_segm_picc import train_test_segm_picc_func
from train_test_set import train_test_func
import pandas as pd



selection = None
while selection not in ['1','2','3']:
    selection = input('-type 1 to apply ML on the set of features (segments) selected with variance\n-type 2 to apply ML only on the selected features that are < 20 bases:\n-type 3 to use the features obtained by variance combined with random forest > ')
var = None
while var not in ['0.070', '0.080', '0.090','0.100']:
    var = input('type the level of variance to use to reduce the num of features [0.070, 0.080, 0.090,0.095, 0.100]\n > ')
name1 = str(var) + '_feat_var.txt'
name2 = 'pat_ind_train.txt'
if selection == '2':
    try:
        X_train = pd.read_csv('train_test_set/X_train_var%s_basi20.csv' %(var),index_col=0)
        X_test = pd.read_csv('train_test_set/X_test_var%s_basi20.csv' %(var),index_col=0)
    except FileNotFoundError:  # se non erano stati già calcolati e salvati con HPC allora vengono calcolati al momento
        X_train, X_test = train_test_segm_picc_func(name2)
elif selection =='3':
    try:
        X_train = pd.read_csv('train_test_set/X_train_var%s_rf.csv' %(var),index_col=0)
        X_test = pd.read_csv('train_test_set/X_test_var%s_rf.csv' %(var),index_col=0)
    except FileNotFoundError: # se non erano stati già calcolati e salvati con HPC allora vengono calcolati al momento
        X_train, X_test = train_test_func(name1,name2)    
else:
    try:
        X_train = pd.read_csv('train_test_set/X_train_var%s.csv' %(var),index_col=0)
        X_test = pd.read_csv('train_test_set/X_test_var%s.csv' %(var),index_col=0)
    except FileNotFoundError: # se non erano stati già calcolati e salvati con HPC allora vengono calcolati al momento
        X_train, X_test = train_test_func(name1,name2)



Y_train = []
for ind in X_train.index:
    if int(ind) < 1000:
        Y_train.append(0)  # kidney
    else:
        Y_train.append(1)  # lung
Y_test = []
for t_ind in X_test.index:
    if int(t_ind) < 1000:
        Y_test.append(0)  # kidney
    else:
        Y_test.append(1)  # lung
params = []
accuracies_train, accuracies_test = [], []
confmat_train, confmat_test =  [],  []
k='linear'
print(k)
params.append([k])
SVM = SVC(kernel=k)
SVM.fit(X_train, Y_train)
y_train_pred = SVM.predict(X_train)
confmat_train.append(metrics.confusion_matrix(Y_train, y_train_pred))
y_test_pred = SVM.predict(X_test)
confmat_test.append(metrics.confusion_matrix(Y_test, y_test_pred))
accuracies_train.append(metrics.accuracy_score(Y_train,y_train_pred))
accuracies_test.append(metrics.accuracy_score(Y_test,y_test_pred))
print("acc train: {}, acc test: {}".format(metrics.accuracy_score(Y_train,y_train_pred),metrics.accuracy_score(Y_test,y_test_pred)))

for k in ['poly','rbf','sigmoid']:
    for gamma in ['auto','scale']:
        print(k)
        params.append([k,gamma])
        SVM = SVC(kernel=k,gamma=gamma)
        SVM.fit(X_train, Y_train)
        y_train_pred = SVM.predict(X_train)
        confmat_train.append(metrics.confusion_matrix(Y_train, y_train_pred))
        y_test_pred = SVM.predict(X_test)
        confmat_test.append(metrics.confusion_matrix(Y_test, y_test_pred))
        accuracies_train.append(metrics.accuracy_score(Y_train,y_train_pred))
        accuracies_test.append(metrics.accuracy_score(Y_test,y_test_pred))
        print("acc train: {}, acc test: {}".format(metrics.accuracy_score(Y_train,y_train_pred),metrics.accuracy_score(Y_test,y_test_pred)))

    
plt.plot(accuracies_train, label='acc train')
plt.plot(accuracies_test, label='acc test')
plt.legend()
plt.show()
plt.xticks(ticks=np.arange(len(params)), labels=params, rotation=20)
mysave = {'2':'short segments','1':'whole region','3':'random forest'}
plt.title('Accuracy over different models for variance: {} and {}'.format(var, mysave[selection]))
plt.savefig('ML_comparison_prove/acc_{}_{}.png'.format(mysave[selection],var))


