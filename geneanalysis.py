#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:16:29 2019

@author: sabrina

Discretizzare i segmenti di geni per capire quale valore attribuirgli
Si crea un plot che mostra in blu i punti di start e in rosso di end
Si valutano le eventuali sovrapposizioni
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

kdata = pd.read_csv("kidney_data.csv")
pat_names = kdata.GDC_Aliquot.unique()
chr1 = pd.DataFrame()

for pat in pat_names:  # for each patient
    rows = kdata.loc[kdata[kdata.columns[0]] == pat]  #take all of patient1 rows
    # now get only chromosome 1
    rows = rows.loc[rows[rows.columns[1]] == '1']
    rows = rows.drop(columns = [rows.columns[0],rows.columns[1],rows.columns[4]])
    chr1 = chr1.append(rows)
    
inizio = min(chr1["Start"])
fine = max(chr1["End"])
distanze = np.array(chr1["End"] - chr1["Start"])
plt.hist(distanze, bins = 100)
plt.title('Distribution of the dimensions of segments in CHR1')
plt.xlabel('Length of the segment')
plt.ylabel('Frequency')
step = 2000000  # deciso dopo aver valutato l'istogramma

df = pd.DataFrame(index=range((fine-inizio)/step+1),columns = list(pat_names))
#for p in range(inizio, fine, passo):
#BO vedere quaderno
if chr1["Start"][j] >= inizio and chr1["End"][j] <= fine:
    
    
    
    

#    # l'idea era di creare la discretizzazione a partire dai reali segmenti
#    # a quel punto valutare caso per caso quale valore attribuire
#chr1 = chr1.reset_index(drop = True)
#segments = np.hstack((np.array(chr1["Start"]), np.array(chr1["End"])))
#segments = np.unique(segments)
#if len(segments)%2 != 0:
#    segments = np.append(segments,segments[-1]+10) 
#segments = segments.reshape((len(segments)/2,2))
#segments = pd.DataFrame(segments)
#segments.columns = ['Start', 'End']
#segments['values'] = [list() for x in range(len(segments.index))]
## guardo il valore del primo segmento in chr1
## attribuisco quel valore a tutti i segmenti di segm compresi in quel segmento
#for i in range(len(chr1)):
#    for j in range(len(segments)):
#        if segments["Start"][j] >= chr1["Start"][i] and segments["End"][j] <= chr1["End"][i]:
#            segments["values"][j].append(chr1["Segment_mean"][i])
#    
## ad esempio il gene AJAP1 protein coding si posiziona tra i segmenti 64 e 71    
## plt.plot(segments["values"][64])
#for k in range(len(segments)):
#    segments['mean_significant_values'][k] = np.mean([i for i in segments["values"][k] if abs(i) >= 0.1])
