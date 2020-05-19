# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:14:00 2020

@author: vener

tumor related genes were obtained from cancermine website: http://bionlp.bcgsc.ca/cancermine/

"""

import csv
import pandas as pd

cancermine = []
with open('cancermine_collated.tsv','r') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    cancermine.append(row)
df = pd.DataFrame(cancermine[1:],columns = cancermine[0])
print(f"there are {len(set(df['gene_normalized']))} unique genes in the file")
print(f"they can be either: {set(df['role'])}")
df.to_csv("cancermine.csv",index=False)

