# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:14:07 2019

@author: vener

modificare df_allchr per salvare anche il numero di cromosoma di provenienza del segmento

"""

import pandas as pd

df_all = pd.read_csv("df_allchr.csv", index_col=0)

start = df_all.index.values
end = df_all.iloc[:,0].values
segments = []
for i in range(len(df_all)):
    segments.append(str(start[i]) + "_" + str(end[i]))

chrs_list = range(1,23)
CHRs, lengths, new_segments = [], [], []
for item in chrs_list:
    CHRs.append(str(item))
CHRs.append('X')

for chromosome in CHRs:
    df_1 = pd.read_csv("data_chr/df_chr%s.csv" % chromosome, index_col=0)
    lengths.append(len(df_1))
    
segments = []
for i in range(len(df_all)):
    segments.append("_" + str(start[i]) + "_" + str(end[i]))

for l in lengths:
    for i in range(l):
        new_segments.append(CHRs[lengths.index(l)] + segments[i])

df_all = df_all.drop(columns=df_all.columns[0])    
df_all.index = new_segments
df_all.to_csv(r"df.csv", index=True, header=True)