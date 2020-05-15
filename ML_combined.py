# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:21:33 2019

@author: vener
The algorithm needs 3 arguments from the command line:
the name of the file where the features
the file where the pat ind is
The max number of bases allowed per feature
"""
import matplotlib as mpl
import os
#if os.environ.get('DISPLAY','') == '':
#    print('no display found. Using non-interactive Agg backend')
#    mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from train_test_segm_picc import train_test_segm_picc_func
from train_test_set import train_test_func
import sys
import pandas as pd



def create_NN():
    
    #define the model
    model = Sequential()
    model.add(Dense(64, input_dim=len(X_train.columns), activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

selection = None
while selection not in ['1','2','3']:
    selection = input('-type 1 to apply ML on the set of features (segments) selected with variance\n-type 2 to apply ML only on the selected features that are < 20 bases:\n-type 3 to use the features obtained by variance combined with random forest > ')
var = None
while var not in ['0.070', '0.080', '0.090', '0.095','0.100']:
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
print('defining the models..')
model = []
model.append(('KNN', KNeighborsClassifier(n_neighbors=20)))
model.append(('DT', DecisionTreeClassifier()))
model.append(('SVM', SVC(gamma='auto')))
model.append(('SGDC', SGDClassifier(random_state=42)))
model.append(('NN', KerasClassifier(build_fn = create_NN, epochs=150, batch_size=10, verbose=0)))

results, names = [], []

for n, M in model:    
    print('Now using %s' %n)
    if n != 'NN':
        M.fit(X_train, Y_train)

    score = cross_val_score(M, X_train, Y_train, cv=10, scoring="accuracy")

    y_train_pred = cross_val_predict(M, X_train, Y_train, cv=10)
    y_test_pred = cross_val_predict(M, X_test, Y_test, cv = 10)
    
    confmat_train = confusion_matrix(Y_train, y_train_pred)
    confmat_test = confusion_matrix(Y_test, y_test_pred)
    
    print('\nTraining %s: mean of accuracy = %f; std dev = (%f)' % (n, score.mean(), score.std()))
    
    results.append(score)
    names.append(n)

    print("\n%s: Confusion matrix train = " % (n))
    print(confmat_train)
    print("\n%s: Confusion matrix test = " % (n))
    print(confmat_test)

plt.boxplot(results, labels=names)
plt.ylim((0.5,1.0))
if selection == '2':
    plt.title('Algorithm Comparison var %s basi<20' %(var))
    plt.show(block=True)    
    plt.savefig("ML_comparison_prove/ML_Comparison_var%s_basi20.png" % (var))    
elif selection =='3':
    plt.title('Algorithm Comparison var %s + rand forest' %(var))
    plt.show(block=True)
    plt.savefig("ML_comparison_prove/ML_Comparison_var%s_rf.png" % (var))
else:
    plt.title('Algorithm Comparison var %s' %(var))
    plt.show(block=True)
    plt.savefig("ML_comparison_prove/ML_Comparison_var%s.png" % (var))