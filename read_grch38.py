# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:24:28 2020

@author: vener
"""

import re
import pandas as pd
import sys
import gzip

cont = 0
with gzip.open("Homo_sapiens.GRCh38.95.gtf.gz", 'rb') as hg:
    for line in hg:
        cont += 1
        if len(line)<=50:
            cont -= 1
head = ["chr", "source","type","start","end","strand","gene_id","gene_version", "transcript_id", 
        "transcript_version", "exon_number", "gene_name", "gene_source", "gene_biotype", "transcript_name",
        "transcript_source", "transcript_biotype","ccds_id","havana_transcript","havana_transcript_version",
        "protein_id","protein_version","exon_id","exon_version","tag","transcript_support_level"]
df = pd.DataFrame(columns=head,index=range(cont))
i = 0
with gzip.open("Homo_sapiens.GRCh38.95.gtf.gz", 'rb') as hg:
    for line in hg:
        line = line.decode().strip()
        if len(line)>50:
            delimiters = "; ", "	", " ", ";"
            pattern = '|'.join(map(re.escape, delimiters))
            splitted = re.split(pattern, line)
            newline = splitted[0:5] + [splitted[6]] + splitted[8:-1] #removed empty elements
            # caso particolare "(assigned to previous version)"
            assigned, ind_to_pop = [], []            
            for ind in range(len(newline)):
                if '"' in newline[ind]:
                    if newline[ind].count('"') == 1:
                        # this means that the sentence is not finished
                        assigned.append(newline[ind])
                        ind_to_pop.append(ind)
                        while ')"' not in newline[ind]:
                            ind += 1
                            ind_to_pop.append(ind)
                            assigned.append(newline[ind])
                        break
            if len(assigned)>0:
                for idx in sorted(ind_to_pop, reverse = True):
                    del newline[idx]
                newline.append(' '.join(assigned))
            df.iloc[i]["chr"] = newline[0]
            df.iloc[i]["source"] = newline[1]
            df.iloc[i]["type"] = newline[2]
            df.iloc[i]["start"] = newline[3]
            df.iloc[i]["end"] = newline[4]
            df.iloc[i]["strand"] = newline[5]
            for j in range(6,len(newline),2):
                df.iloc[i][newline[j]] = newline[j+1].strip('""')
                if newline[j] not in head or '"' not in newline[j+1]: #if the case is different from my hypotesis
                    print(newline[j])
                    sys.exit
            i += 1

df.to_csv("grch38.csv",index=False)