#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:37:38 2019

@author: sabrina

All of the kidney data for each of the samples is store in the dataframe named "data"

"""
import os, glob 
import pandas as pd

# get current directory
# current_dir = "/home/sabrina/Documenti/Bioinformatica/Progetto"
# go to the directory where the files are (KIDNEY)
kidney_dir = '/home/sabrina/Scrivania/Bioinformatica/Progetto/gdc_kidney_download_20191002_151641.408115'
lung_dir = '/home/sabrina/Scrivania/Bioinformatica/Progetto/gdc_lung_download_20191002_152306.154805'
directories = [kidney_dir, lung_dir]
for dirs in directories:
    os.chdir(dirs)
    data = pd.DataFrame()
    # get the list of the directory's content
    content_dir = os.listdir(dirs)
    for d in content_dir:
        filename, file_extension = os.path.splitext(d)
        if file_extension != '' :
            continue
        os.chdir(d)
        for file in glob.glob("*.txt"):
            newdata = pd.read_csv(file, sep="	", header=None)  # read and store
            newdata = newdata.iloc[1:]  # discard first row (header)
            data = data.append(newdata)  # create the big dataframe
        os.chdir(dirs)
    
    col = ["GDC_Aliquot", "Chromosome", "Start", "End", "Num_Probes", "Segment_mean"]
    data.columns = col
#datac = data.to_csv(r"/home/sabrina/Documenti/Bioinformatica/Progetto/kidney_data.csv", index=False, header=True)
#datal = data.to_csv(r"/home/sabrina/Documenti/Bioinformatica/Progetto/lung_data.csv", index=False, header=True)
