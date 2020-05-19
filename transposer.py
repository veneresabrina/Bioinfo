# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 13:09:41 2019

@author: vener
"""
import pandas as pd
df = pd.read_csv("df.csv", index_col=0)

df = df.transpose()
df.to_csv(r"df_T.csv", index=True, header=True)
