# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 15:48:19 2019

@author: vener

modified to work on external server
takes in input the dataframes of each chromosome and puts them together in a single dataframe 

"""

import pandas as pd

chrs_list = range(1,23)
CHRs = []
for item in chrs_list:
    CHRs.append(str(item))
CHRs.append('X')
dataframe = pd.DataFrame()
for chromosome in CHRs:
    
    df = pd.read_csv("data_chr/df_chr%s.csv" %chromosome, index_col=0)
    df = df.fillna(0)
    df = df.set_index([df.columns[0], df.columns[1]])
    df.insert(0,'Chromosome',chromosome)
    dataframe = dataframe.append(df)

dataframe.to_csv(r"df_allchr.csv" , index=True, header=True)

