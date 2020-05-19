# -*- coding: utf-8 -*-
"""
Created on Thu May 14 20:40:29 2020

@author: vener

apply random forest to perform feature selection
computational cost is high, therefore it was not used later in the project

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

rand_pat = []
with open("train_test_set/pat_ind_train.txt", "r") as f:
    for line in f:
        rand_pat.append(f.readline())

X = pd.read_csv("df_T.csv",index_col=0)
X.reset_index(inplace=True,drop=True)

Y = []
for ind in X.index:
    if int(ind) < 1000:
        Y.append(0)  # kidney
    else:
        Y.append(1)  # lung


clf = ExtraTreesClassifier(n_estimators=10)
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
with open("train_test_set/features_tree.txt", "w") as output:
    for name in features_selected:
        writer = csv.writer(output, lineterminator='\n')            
        writer.writerow([name])
        cont += 1
print(">> %d features added." % cont)
