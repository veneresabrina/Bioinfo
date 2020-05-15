# -*- coding: utf-8 -*-
"""
Created on Thu May 14 20:40:29 2020

@author: vener

apply random forest to perform feature selection

"""

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
import pandas as pd
import csv


num_feat = 0

features = []
with open("segments_in_df.txt", "r") as f:
    csv_reader = csv.reader(f)
    for row in f:
        row = row.rstrip('\n')
        row = row.rstrip('\r')
        features.append(row)
step = 20000
r = list(range(0,len(features),step))
r2 = list(range(step,len(features),step))
r2.append(len(features))
rand_pat = []
with open("train_test_set/pat_ind_train.txt", "r") as f:
    for line in f:
        rand_pat.append(f.readline())

for i in range(len(r)):
    # selecting only first chunk of features and the 1500 random patients
    X = pd.read_csv("df_T.csv", usecols = features[r[i]:r2[i]])
    X = X.iloc[rand_pat]

Y = []
for ind in X.index:
    if int(ind) < 1000:
        Y.append(0)  # kidney
    else:
        Y.append(1)  # lung


clf = ExtraTreesClassifier(n_estimators=50)
clf = clf.fit(X, Y)
model = SelectFromModel(clf, prefit=True)
#X_new = model.transform(X)
# find the features with tree value > 0
features = X.columns.to_list()
features_selected=[]
for ind in range(len(clf.feature_importances_)):
    if clf.feature_importances_[ind] > 0:
        features_selected.append(features[ind])


cont = 0
with open("train_test_set/features_tree.txt", "a") as output:
    for name in features_selected:
        writer = csv.writer(output, lineterminator='\n')            
        writer.writerow([name])
        cont += 1
print(">> %d features added." % cont)
