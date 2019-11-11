#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:16:29 2019

@author: sabrina

Per il cromosoma1 si ricava un dataframe che ha come righe una discretizzazione
delle coordinate del cromosoma e come colonne tutti i pazienti
A ogni cella corrisponde il segment_mean più rappresentativo di quella porzione
di cromosoma, se non ve n'è nessuno allora si assegna 0.
Il valore più rappresentativo è quello che occupa la maggior parte del segmento

I valori ottenuti non mi convincono. Perchè mette 0? Siamo sicuri che quella
porzione non fosse rappresentata magari da un valore precedente o successivo?

Rimane da definire il nome dei geni avendo le coordinate, alcune misure statistiche,
eventuale dimensionality reduction, generalizzazione a tutti i cromosomi, salvando
il dataset ottenuto sia per il kidney che per il lung tumor.

"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

kdata = pd.read_csv("kidney_data.csv")
pat_names = kdata.GDC_Aliquot.unique()
chr1 = pd.DataFrame()

for pat in pat_names:  # for each patient
    rows = kdata.loc[kdata[kdata.columns[0]] == pat]  #take all of patient1 rows
    # now get only chromosome 1
    rows = rows.loc[rows[rows.columns[1]] == '1']
    rows = rows.drop(columns = [rows.columns[1],rows.columns[4]])
    chr1 = chr1.append(rows)
    
inizio = min(chr1["Start"])
fine = max(chr1["End"])
distanze = np.array(chr1["End"] - chr1["Start"])
hist, bin_edges = np.histogram(distanze, bins = len(chr1)/100)
n = bin_edges[list(hist).index(max(hist)) + 1]
s = str(int(n))
step = int(s[0] + '0'*(len(s)-1))/2

#y, x, _ = plt.hist(distanze, bins = 77)
#plt.title('Distribution of the dimensions of segments in CHR1')
#plt.xlabel('Length of the segment')
#plt.ylabel('Frequency')
#print x.max()
#print y.max()
#step = 2000000  # deciso dopo aver valutato l'istogramma


# redefine index to match segments points 
l1 =  list(range(inizio, fine - step, step))
l2 = list(range(inizio + step, fine, step))

df = pd.DataFrame(columns = list(pat_names))
df.insert(0,"Min",l1)
df.insert(1,"Max",l2)
df = df.set_index(['Min', 'Max'])

# per ogni riga di chr1
for index, segment in chr1.iterrows():
    # per ogni range predefinito
    for min_max in df.index:
        # se non è ancora stato messo un valore
        if df.isnull().at[min_max, segment["GDC_Aliquot"]]:
            # se cade all'interno dei range predefiniti e occuperebbe almeno il 60% del segmento
            if min_max[0] >= segment["Start"] and min_max[1] <= segment["End"] and segment["End"] - segment["Start"] >= 0.6 * step:
                df.at[min_max, segment["GDC_Aliquot"]] = segment['Segment_mean']
            # se è a cavallo tra due range predefiniti ma molto vicino a quello corrente
            elif (min_max[0] - segment["Start"] < 0.01*step or min_max[1] - segment["End"] < 0.01*step) and segment["End"] - segment["Start"] >= 0.6 * step:
                df.at[min_max, segment["GDC_Aliquot"]] = segment['Segment_mean']
            # se è troppo piccolo rispetto al range predefinito
            elif segment["End"] - segment["Start"] < 0.6 * step:
                df.at[min_max, segment["GDC_Aliquot"]] = 0
        # se gli è già stato assegnato un valore ma il nuovo segmento è predominante
        elif min_max[0] >= segment["Start"] and min_max[1] <= segment["End"] and segment["End"] - segment["Start"] >= 0.6 * step:
            df.at[min_max, segment["GDC_Aliquot"]] = segment['Segment_mean']



#
## itera su ogni riga del chr1
#for index, segment in chr1.iterrows():
#    for ind in df.index:
#        if ind >= segment["Start"] and ind <= segment["End"]:
#            df.at[ind, df.columns == segment["GDC_Aliquot"]] = segment['Segment_mean']
#        # Se non rientra nei range definiti dallo step allora allarga leggermente il range
#        elif ind >= segment["Start"] - 1000 and ind <= segment["End"] + 1000:
#            df.at[ind, df.columns == segment["GDC_Aliquot"]] = segment['Segment_mean']
#            

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
