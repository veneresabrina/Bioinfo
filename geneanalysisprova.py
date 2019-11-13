# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:47:59 2019

@author: vener
"""
import pandas as pd
step = 100
start_v = range(0,900,step)
end_v = range(99, 999, step)
dati = [102,285],[289,599],[238,498],[178,492],[160,489],[212,669],[385,870],[315,835]

df = pd.DataFrame(index = [start_v,end_v] ,columns=['a','b','c','d','e','f','g','h'])

i, j = 0, 0

for segment in dati:    
    
    while segment[0] > end_v[i]:
            i = i + 1
            j = i
    if segment[1] <= end_v[i]:
        if segment[1] - segment[0] >= 0.6*step:
            df.at[start_v[i],df.columns[dati.index(segment)]] = 1
        i, j = 0, 0
    else:
        while segment[1] > end_v[j]:
            j = j + 1
        if end_v[i] - segment[0] >= 0.6*step:
            df.at[start_v[i],df.columns[dati.index(segment)]] = 1
        if segment[1] - start_v[j] >= 0.6*step:
            df.at[start_v[j],df.columns[dati.index(segment)]] = 1
        if j > i + 1:
            for k in range(i+1,j):
                df.at[start_v[k],df.columns[dati.index(segment)]] = 1
        i, j = 0, 0

df.columns = dati