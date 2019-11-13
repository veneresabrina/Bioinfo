# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:36:06 2019

@author: vener
"""



import pandas as pd
import numpy as np

kdata = pd.read_csv("kidney_data.csv")
pat_names = kdata.GDC_Aliquot.unique()

for chromosome in kdata['Chromosome'].unique():
    
    chr1 = pd.DataFrame()
    
    for pat in pat_names:  # for each patient
        rows = kdata.loc[kdata[kdata.columns[0]] == pat]  #take all of patient1 rows
        # now get only chromosome 1
        rows = rows.loc[rows[rows.columns[1]] == chromosome]
        rows = rows.drop(columns = [rows.columns[1],rows.columns[4]])
        chr1 = chr1.append(rows)
        
    inizio = min(chr1["Start"])
    fine = max(chr1["End"])
    distanze = np.array(chr1["End"] - chr1["Start"])
    hist, bin_edges = np.histogram(distanze, bins = len(chr1)/100)
    n = bin_edges[list(hist).index(max(hist)) + 1]
    s = str(int(n))
    step = int(s[0] + '0'*(len(s)-1))
    
    # redefine index to match segments points 
    start_v =  list(range(inizio, fine - step, step))
    end_v = list(range(inizio + step, fine, step))
    start_v.insert(0, int(inizio-step))
    end_v.insert(len(end_v),int(fine+step))
    end_v.insert(0,int(inizio))
    start_v.insert(len(start_v),int(fine))
    start_v = [start_v[i] + 1 for i in range(len(end_v))]

    df = pd.DataFrame(columns = list(pat_names))
    df.insert(0,"Min",start_v)
    df.insert(1,"Max",end_v)
    df = df.set_index(['Min', 'Max'])

    i, j = 0, 0

    for index, segment in chr1.iterrows():
        while segment["Start"] > end_v[i]:
            i = i + 1
            j = i
        if segment["End"] <= end_v[i]:
            if segment["End"] - segment["Start"] >= 0.6*step:
                df.at[start_v[i], segment["GDC_Aliquot"]] = segment['Segment_mean']
            i, j = 0, 0
        else:
            while segment["End"] > end_v[j]:
                j = j + 1
            if end_v[i] - segment["Start"] >= 0.6*step:
                df.at[start_v[i], segment["GDC_Aliquot"]] = segment['Segment_mean']
            if segment["End"] - start_v[j] >= 0.6*step:
                df.at[start_v[j], segment["GDC_Aliquot"]] = segment['Segment_mean']
            if j > i + 1:
                for k in range(i+1,j):
                    df.at[start_v[k], segment["GDC_Aliquot"]] = segment['Segment_mean']
            i, j = 0, 0
        
        
    saving = df.to_csv(r"D:\vener\Documents\Bioinformatica\progetto\Bioinfo-master\data_chr\kdf_chr%s.csv" % chromosome, index=True, header=True)
        
        
