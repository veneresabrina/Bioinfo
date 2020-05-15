# Bioinfo
# Copy number variation data as a biomarker for cancer types
The data was provided by the GDC portal and it covers kidney and lung tumours.
The copy number value points out whether a region of the DNA is diploid or if it presents amplification or deletion:
- CNV > 0 : amplification
- CNV = 0 : diploid
- CNV < 0 : deletion

The original dataset was made up of 1000 patients for the kidney tumor and 1000 patients for the lung tumor, the patients are on the rows and the columns were the following:
- chromosome
- start coordinate of the segment
- end coordinate of the segment
- number of probes
- segment mean value

# Creating the dataset 
The first approach was segmenting each chromosome with a step k and then assigning the corresponding CNV but these procedure presented some issues one of them was the fact that the highest values of CNV were found on the smallest segments.
The chromosome was finally segmented with a variable step, taking into consideration all of the start and end coordinates indicated in the original dataset, those coordinates were sorted and marked as the separating points of the new segments.
In the end an approximately 2000x400000 matrix was obtained, the patients on the rows and the segments (in the form nchr_start_end, for example 1_30000_30020) as columns, and the matrix contained the corresponding CNV values.
A balanced training set was generated with 1500 samples, the remaining 500 were used for testing.

# Feature selection
400000 features had to be greatly reduced with an appropriate feature selection method.
Variance proved to be computationally lighter than other methods but the results of the machine learning tools were not optimal (about 0.8 accuracy on the training set and 0.7 on the test set). The algorithm correctly removed the features with the smallest variation (e.g. the segments where the CNV mantained approximately the same value for all of the patients examined) but it did not take into consideration the classes and consequently prefered those segments where tha values were diversified but not necesseraly differenciating the case of the kidney from the case of the lung. As a matter of fact from the statistical analysis it was clear that chromosome 7 had one of the best set of features (segments) able to separate the classification problem (the mean value of the CNV of the kidney was very different from the one of the lung) but even with different threshold values the variance method neglected those segments prefering the ones from chromosome 3 for example.
To choose the best feature selection method and machine learning tool cross validation was applied to each set obtained with the different fs methods.

# Machine learning and deep learning
Finally three tools were chosen to perform the classification task: Decision tree, SVM and multilayer perceptron.
