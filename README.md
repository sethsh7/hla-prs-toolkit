# Polygenic Risk Score (PRS) Toolkit for HLA

### Please note the terms Polygenic Risk Score (PRS) and Genetic Risk Score (GRS) are used interchangeably.

This page contains a collection of scripts and tools along with an explanation on published Single Nucleotide Polymorphism (SNP) based Polygenic Risk Scores (PRS) for common polygenic disease / traits where Human Leukocyte Antigen (HLA) region epistasis (gene vs gene interaction) is modelled. Additionally, we provide instructions and resources in order to verify your own scripts in the publicly available 1000 Genomes data. This work is a collective effort from researchers at the University of Exeter and elsewhere, please see references to corresponding publications below. For any questions about code on this page please contact Seth Sharp by email (s.sharp@exeter.ac.uk). For any questions about the individual PRS utilised here please contact the corresponding author of the relevant publication cited.

## Requirements

All scripts are designed to be run from a bash or compatible shell environment.

PLINK 1.9 is required.

Python / Anaconda (Tested Python 3.8).

PLINK genotyping data.

## 1. PLINK2CALL - Hard calling of HLA haplogenotypes from SNP proxies 


## 2. CAT2SCORES - Assign scores to samples by HLA haplogenotype

## SNP Lists - Assign scores to samples by HLA haplogenotype

### Type 1 Diabetes (T1D-PRS)

10-SNP / 30-SNP score ("GRS1") [1]
67-SNP score ("GRS2") [2]

### Coeliac Disease (CD-PRS)
42-SNP score [3]
Recently published score containing the majority of GWAS significant polygenic variants and a HLA interaction model for the most common risk haplotypes.

To be added at a later date.
## Example with Demo data.

## Supporting Publications

[1] A Type 1 Diabetes Genetic Risk Score Can Aid Discrimination Between Type 1 and Type 2 Diabetes in Young Adults, DiabetesCare 2016, RA Oram et Al

[2] Development and Standardization of an Improved Type 1 Diabetes Genetic Risk Score for Use in Newborn Screening and Incident Diagnosis, DiabetesCare 2019, SA Sharp et Al

[3] A single nucleotide polymorphism genetic risk score to aid diagnosis of coeliac disease: a pilot study in clinical care, AP&T 2020, SA Sharp et Al

## License

Resources are provided under the GNU General Public License v3.0. For more information please LICENSE.md.
