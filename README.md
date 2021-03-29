# Polygenic Risk Score (PRS) Toolkit for HLA

### Please note the terms Polygenic Risk Score (PRS) and Genetic Risk Score (GRS) are used interchangeably dependent on audience.

This page contains a collection of scripts and tools along with an explanation on published Single Nucleotide Polymorphism (SNP) based Polygenic Risk Scores (PRS) for common polygenic disease / traits where Human Leukocyte Antigen (HLA) region epistasis (gene vs gene interaction) is modelled. Additionally, we provide instructions and resources in order to verify your own scripts in the publicly available 1000 Genomes data. This work is a collective effort from researchers at the University of Exeter and elsewhere, please see references to corresponding publications below. For any questions about code on this page please contact Seth Sharp by email (s.sharp@exeter.ac.uk). For any questions about the individual PRS utilised here please contact the corresponding author of the relevant publication cited.

## Requirements

All scripts are designed to be run from a bash or compatible shell environment.

PLINK 1.9 is required.

Anaconda (Tested Python 3.8 as of 10/9/2020).

Scripts are generally intended to be used with array genotyping data in PLINK 1.9 (BED/BIM/FAM) hard calls format OR Oxford (BGEN/SAMPLE) imputed dosages. If your files are in VCF format you will need to convert them.

Input data should be built to GRCh37 / hg19 reference genome. If you have older data you may be able to lift over to hg19. If you have newer data you will have to modify SNP positions in the scripts manually.

## Type 1 Diabetes (T1D-PRS)

We provide scripts to assist with generation of 3 variants of the Exeter T1D-GRS

10-SNP / 30-SNP score ("GRS1") [1]

Original variant of the score intended for either direct genotyping or limited chip data (10/30 SNP versions available)

Ensure all variants are present and on positive strand
Run GEN_GRS1.py targeting your PLINK data prefix, specify score version (10 or 30 SNP)
py GEN_GRS1.py --prefix <mydata> --version 10

If input is correct sample IDs and corresponding scores will print to stdout
67-SNP score ("GRS2") [2]

Largest and most discriminative score containing complex HLA interaction modelling, designed for use with imputed array data.

To be added at a later date.
## Coeliac Disease (CD-PRS)

We provide scripts to assist with generation of our CD-GRS.

42-SNP score [3]

Recently published score containing the majority of GWAS significant polygenic variants and a HLA interaction model for the most common risk haplotypes.

To be added at a later date.
## Verifying Results

Below demonstrates how to verify your results are correct in the publicly available 1000 Genomes phase 3 genotyping data which we provide in both PLINK hard calls and Oxford imputed format.

## Supporting Publications

[1] A Type 1 Diabetes Genetic Risk Score Can Aid Discrimination Between Type 1 and Type 2 Diabetes in Young Adults, DiabetesCare 2016, RA Oram et Al

[2] Development and Standardization of an Improved Type 1 Diabetes Genetic Risk Score for Use in Newborn Screening and Incident Diagnosis, DiabetesCare 2019, SA Sharp et Al

[3] A single nucleotide polymorphism genetic risk score to aid diagnosis of coeliac disease: a pilot study in clinical care, AP&T 2020, SA Sharp et Al

## License

Resources are provided under the GNU General Public License v3.0. For more information please LICENCE.
