#!/usr/bin/bash

### DEMO SCRIPT - Generates HLA-DQ calls and corresponding T1D-GRS67 HLA scores in randomly generated demo PLINK data ###

echo "Running script to generate allele calls from PLINK data..."
python 1_plink2call.py --bfile Demo/demo_cohort --mapping Tools/Snplists/T1D_GRS67/mapping_1000G.txt --rank Tools/Reference/HLADQ_USAEuropean_Klitz.txt
echo "Running script to generate scores from allele calls..."
python 2_cat2scores.py --cat Demo/demo_cohort_Categorical.txt --score Tools/Snplists/T1D_GRS67/scorefile.txt
