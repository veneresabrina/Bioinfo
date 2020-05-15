# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 16:10:24 2020

@author: vener
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


cols = ["chr","type","start","end","gene_id","gene_biotype"]
df = pd.read_csv("grch38.csv", usecols=cols)

pc = df.loc[(df['gene_biotype'] == 'protein_coding') & (df['type'] =="gene")]
# the protein coding genes are 0.73% of the total genes found in grch38 -> len(pc)/len(df)*100 = 0.73
pc = pc.drop(['gene_biotype','type'], axis = 1)
sizes = []
with open("distribution of the dimensions of segments/size_of_chromosome.txt", 'r') as f:
    for line in f:
        sizes.append(line)
# NCHR = list(set(pc.chr)) # si nota che in alcuni casi sono int e in altri str

Nchr = [num for num in range(1,23)]
Nchr.append('X')
pc_perc, stats = [], []
for ind in range(len(Nchr)):

    if Nchr[ind] == 'X':
        nchr = Nchr[ind]
    else:
        nchr = int(Nchr[ind])
    
    pc1 = pc.loc[(pc['chr'] == nchr) | (pc['chr'] == str(nchr))]  # taking into account str chr as well
    size1 = int(sizes[ind].split(",")[1].split('\n')[0])
    
    
    df_chr1 = pd.read_csv(r"D:\vener\Documents\Bioinformatica\progetto\Bioinfo-master\data_chr\df_chr%s.csv" %nchr, index_col=0)  
    df_chr1 = df_chr1.fillna(0)
    
#    y = []
#    for i in range(2,2002):
#        y.append(list(df_chr1[df_chr1.columns[i]]))
#    
    x = [int(elem) for elem in df_chr1[df_chr1.columns[0]]]  # intervalli di regioni analizzate, porzioni del chr
    
    ########## plot median ##############
    medk, medl = [], []
    kidney = df_chr1.iloc[:,2:1002]
    lung = df_chr1.iloc[:,1002:]
    for k in kidney.values:
        medk.append(np.median(k))
    for l in lung.values:
        medl.append(np.median(l))
    
    line1, = plt.plot(x,medk,'b', label = "kidney")
    line2, = plt.plot(x,medl,'r', label = "lung")
    plt.title('Median of Segment_mean values in chr%s\n protein coding genes highligthed' %nchr)
    plt.ylabel('Segment_mean values')  
    plt.xlabel('Coordinates of the chromosome')
    plt.legend(handles = [line1, line2])
    pc_length = 0

        
    # dato start e end di questa protein coding region assegnamole un segment mean value
    regions = df_chr1.iloc[:,0:2]
    start_v = list(regions.iloc[:,0])
    end_v = list(regions.iloc[:,1])
        
    genes_out = 0  # geni che sono rimasti fuori dai dati perchè le loro misure non erano congruenti con le regioni definite    
    i, j = 0, 0
    value_k, value_l = [None] * len(start_v), [None] * len(start_v)
    for index, pc_region in pc1.iterrows():
        s = int(pc_region.start)
        e = int(pc_region.end)
        pc_length += e-s
        if s > end_v[-1]:
            print('gene {} outside of defined region!'.format(pc_region.gene_id))
            genes_out += 1
            pc_length -= e-s # togliere la misura errata dalla lunghezza complessiva delle regioni            
            continue
        while s > end_v[i]:
            i = i + 1
            j = i
        if e <= end_v[i]:
            value_k[i] = float(medk[i])
            value_l[i] = float(medl[i])
            i, j = 0, 0
        else:
            while e > end_v[j]:
                if e > end_v[-1]:
                    j = len(end_v)-1
                    pc_length -= e-s # togliere la misura errata dalla lunghezza complessiva delle regioni
                    pc_length += end_v[-1] - s # si suppone che la regione finisca alla fine del cromosoma                    
                    break
                else:
                    j = j + 1
            if j > i + 1:
                for k in range(i+1,j):
                    value_k[k] = float(medk[i])
                    value_l[k] = float(medl[i])
            i, j = 0, 0
        plt.axvspan(s, e, color='yellow')
            
        
    total_length = x[-1] - x[0]
    pc_perc.append(pc_length/total_length*100)
    CNV_pc_kidney = [item for item in value_k if type(item)==float]
    CNV_pc_lung = [item for item in value_l if type(item)==float]
    plt.savefig("distribution of the dimensions of segments/pc_median_chr%s.png" %nchr, bbox_inches = 'tight')
    plt.close()
    print("{} genes out of {} were outside of the defined regions of chr {}".format(genes_out,len(pc1.gene_id),nchr))
    print("%.2f%% of chromosome %s is protein coding" %(pc_perc[-1],Nchr[ind]))
    with open('CNV_data_chr/CNV_kidney_pc_chr{}.txt'.format(nchr),'w') as f:
        f.write("%.2f%% of chromosome %s is protein coding" %(pc_perc[-1],Nchr[ind]))
        f.write('\n')
        for elem in CNV_pc_kidney:
            f.write(str(elem))
            f.write('\n')
    with open('CNV_data_chr/CNV_lung_pc_chr{}.txt'.format(nchr),'w') as f:
        f.write("%.2f%% of chromosome %s is protein coding" %(pc_perc[-1],Nchr[ind]))
        f.write('\n')        
        for elem in CNV_pc_lung:
            f.write(str(elem))
            f.write('\n')
    with open('CNV_data_chr/CNV_kidney_chr{}.txt'.format(nchr),'w') as f:
        for elem in medk:
            f.write(str(elem))
            f.write('\n')
    with open('CNV_data_chr/CNV_lung_chr{}.txt'.format(nchr),'w') as f:
        for elem in medl:
            f.write(str(elem))
            f.write('\n')
         