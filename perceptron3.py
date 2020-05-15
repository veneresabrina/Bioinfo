# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:56:45 2019

@author: vener
"""

from train_test_set import train_test_func
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import optimizers
from train_test_segm_picc import train_test_segm_picc_func
from sklearn import metrics
import numpy as np



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
accuracies_train, accuracies_test = [], []

layers =  [[64,48,24],[24,24,24],[64,48,64],[24,48,64]]
ep = 200
for l1,l2,l3 in layers:
    
    #define the model
    model = Sequential()
    model.add(Dense(l1, input_dim=len(X_train.columns), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(l2, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(l3, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    learning_rate = 0.001
    decay_rate = learning_rate/ep
    opt = optimizers.Adam(lr=learning_rate, decay=1e-6)    
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])    
    history = model.fit(X_train, Y_train, validation_split=0.33, epochs=ep, batch_size=10, verbose=0)
    # summarize history for accuracy
    print("max of accuracy %d-%d-%d model: %.2f" %(l1,l2,l3,max(history.history['acc'])))
    print("max of val accuracy %d-%d-%d model: %.2f" %(l1,l2,l3,max(history.history['val_acc'])))
    y_train_pred = model.predict_classes(X_train)
    y_test_pred = model.predict_classes(X_test)
    confmat_train = metrics.confusion_matrix(Y_train, y_train_pred)
    confmat_test = metrics.confusion_matrix(Y_test, y_test_pred)
    acc_train = metrics.accuracy_score(Y_train, y_train_pred)
    acc_test = metrics.accuracy_score(Y_test, y_test_pred)
    prec_train = metrics.precision_score(Y_train, y_train_pred)
    prec_test = metrics.precision_score(Y_test, y_test_pred)
    print("\nConfusion matrix train = ")
    print(confmat_train)
    print("\nConfusion matrix test = ")
    print(confmat_test)
    print('training acc {}'.format(acc_train))
    print('test acc {}'.format(acc_test))
    accuracies_train.append(acc_train)
    accuracies_test.append(acc_test)
    
    
plt.plot(accuracies_train, label='acc train')
plt.plot(accuracies_test, label='acc test')
plt.legend()
plt.show()
plt.xticks(ticks=np.arange(len(layers)), labels=layers)
mysave = {'2':'short segments','1':'whole region','3':'random forest'}
plt.title('Accuracy over different NN models for variance: {} and {}'.format(var, mysave[selection]))
plt.savefig('NN_performances/acc_{}_{}.png'.format(mysave[selection],var))
