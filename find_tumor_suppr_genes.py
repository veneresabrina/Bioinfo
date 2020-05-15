# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:59:41 2020

@author: vener
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
pc = pd.read_csv("cancermine_genenames.csv", index_col=0)

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
    plt.title('Median of Segment_mean values in chr%s\n tumor related genes highligthed' %nchr)
    plt.ylabel('Segment_mean values')  
    plt.xlabel('Coordinates of the chromosome')
    plt.legend(handles = [line1, line2])
    pc_length = 0

        
    # dato start e end di questa protein coding region assegnamole un segment mean value
    regions = df_chr1.iloc[:,0:2]
    start_v = list(regions.iloc[:,0])
    end_v = list(regions.iloc[:,1])
        
    genes_out = 0
    i, j = 0, 0
    value_k, value_l = [None] * len(start_v), [None] * len(start_v)
    for index, pc_region in pc1.iterrows():
        s = int(pc_region.start)
        e = int(pc_region.end)
        pc_length += e-s
        if s > end_v[-1]:
            print('gene {} outside of defined region!'.format(pc_region.gene_normalized))
            genes_out+=1
            pc_length -= e-s # togliere la misura errata dalla lunghezza complessiva delle regioni
            continue
        while s > end_v[i]:  # l'inizio di questa regione è più avanti -> aumenta gli indici i e j
            i = i + 1
            j = i
        if e <= end_v[i]:  # se è incluso in questo segmento
            value_k[i] = float(medk[i])
            value_l[i] = float(medl[i])
            i, j = 0, 0
        else:
            while e > end_v[j]:
                if e > end_v[-1]:
                    j = len(end_v)-1  # di modo che il riempimento del segmento fino alla fine non crei errori
                    pc_length -= e-s # togliere la misura errata dalla lunghezza complessiva delle regioni
                    pc_length += end_v[-1] - s # si suppone che la regione finisca alla fine del cromosoma
                    break
                else:
                    j = j + 1
            if j > i + 1:
                for h in range(i+1,j):
                    value_k[h] = float(medk[i])
                    value_l[h] = float(medl[i])
            i, j = 0, 0
        plt.axvspan(s, e, color='yellow')
        
                
    
    plt.savefig("distribution of the dimensions of segments/tumor_suppr_chr%s.png" %nchr, bbox_inches = 'tight')
    plt.close()
    
    print("{} genes out of {} were outside of the defined regions of chr {}".format(genes_out,len(pc1.gene_normalized),nchr))
    total_length = x[-1] - x[0]
    pc_perc.append(pc_length/total_length*100)
    print("%.2f%% of chromosome %s is tumor related" %(pc_perc[-1],Nchr[ind]))
    # i valori CNV corrispondenti alle regioni evidenziate sono contenuti in value_v
    # bisogna selezionare solo i valori esistenti (not None)
    CNV_tumorsuppr_kidney = [item for item in value_k if type(item)==float]
    CNV_tumorsuppr_lung = [item for item in value_l if type(item)==float]
    with open('CNV_data_chr/CNV_kidney_tumorsuppr_chr{}.txt'.format(nchr),'w') as f:
        f.write("%.2f%% of chromosome %s is tumor related" %(pc_perc[-1],Nchr[ind]))  
        f.write('\n')        
        for elem in CNV_tumorsuppr_kidney:
            f.write(str(elem))
            f.write('\n')
    with open('CNV_data_chr/CNV_lung_tumorsuppr_chr{}.txt'.format(nchr),'w') as f:
        f.write("%.2f%% of chromosome %s is tumor related" %(pc_perc[-1],Nchr[ind]))  
        f.write('\n')          
        for elem in CNV_tumorsuppr_lung:
            f.write(str(elem))
            f.write('\n')
         
#    total_length = x[-1] - x[0]
#    pc_perc.append(pc_length/total_length*100)
#    print("%.2f%% of chromosome %s is tumor related" %(pc_perc[-1],Nchr[ind]))    
#    print("%f is the mean of the median over all patients for kidney" %np.mean(CNV_tumorsuppr_kidney))
#    stats.append(np.mean(CNV_tumorsuppr_kidney))
#    print("%f is the mean of the median over all patients for lung" %np.mean(CNV_tumorsuppr_lung))
#    stats.append(np.mean(CNV_tumorsuppr_lung))
#    print("%f is the std of the median over all patients for kidney" %np.std(CNV_tumorsuppr_kidney))
#    stats.append(np.std(CNV_tumorsuppr_kidney))
#    print("%f is the std of the median over all patients for lung" %np.std(CNV_tumorsuppr_lung))
#    stats.append(np.std(CNV_tumorsuppr_lung))
#    print("%f is the 80-percentile of the median over all patients for kidney" %np.percentile(CNV_tumorsuppr_kidney,80))
#    stats.append(np.percentile(CNV_tumorsuppr_kidney,80))
#    print("%f is the 80-percentile of the median over all patients for lung" %np.percentile(CNV_tumorsuppr_lung,80))
#    stats.append(np.percentile(CNV_tumorsuppr_lung,80))
#    print("%f is the 25-percentile of the median over all patients for kidney" %np.percentile(CNV_tumorsuppr_kidney,25))
#    stats.append(np.percentile(CNV_tumorsuppr_kidney,25))
#    print("%f is the 25-percentile of the median over all patients for lung" %np.percentile(CNV_tumorsuppr_lung,25))
#    stats.append(np.percentile(CNV_tumorsuppr_lung,25))    
#
#    
#mediek = stats[0::8]
#mediel = stats[1::8]
#stdk = stats[2::8]
#stdl = stats[3::8]
#perc80k = stats[4::8]
#perc80l = stats[5::8]
#perc25k = stats[6::8]
#perc25l = stats[7::8]
#with open('avg_std_tumorsuppr.txt','w') as f:
#    for elem in stats:
#        f.write(str(elem))
#        f.write('\n')
#    
