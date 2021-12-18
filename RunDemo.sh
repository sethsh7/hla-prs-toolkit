#!/usr/bin/bash

echo "Running script to generate allele calls from PLINK data..."
python 1_plink2call.py --bfile Demo/demo_cohort --mapping Demo/mapping_old.txt --rank Tools/Reference/HLADQ_USAEuropean_Klitz.txt
echo "Running script to generate scores from allele calls..."
#python 2_cat2scores.py --cat demo/demo_cohort_cat.txt --score demo/scorefile.txt 
