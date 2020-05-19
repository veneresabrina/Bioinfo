# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:19:26 2019

@author: vener
"""
import pandas as pd
from bisect import bisect_left

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return 0
    if pos == len(myList):
        return  - 1
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return pos
    else:
       return pos - 1

kdata = pd.read_csv("kidney_data.csv")
ldata = pd.read_csv("lung_data.csv")
CHRs = list(kdata['Chromosome'].unique())

for chromosome in CHRs:
    
    df = pd.read_csv("data_chr\emptydf_chr%s.csv" %chromosome)
    start_v = df[df.columns[0]].tolist()
    end_v = df[df.columns[1]].tolist()
    chr1 = pd.read_csv("data_chr\chr%s.csv" %chromosome)
    
    for index, row in chr1.iterrows():
        pos_s = take_closest(start_v, row.Start)
        pos_e = take_closest(end_v, row.End)
        df.loc[pos_s:pos_e, row.GDC_Aliquot] = row.Segment_mean
    
    df.to_csv(r"D:\vener\Documents\Bioinformatica\progetto\Bioinfo-master\data_chr\df_chr%s.csv" %chromosome, index=True, header=True)

    
    
    
    
    
    
    