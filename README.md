# Polygenic Risk Score (PRS) Toolkit for HLA

### Please note the terms Polygenic Risk Score (PRS) and Genetic Risk Score (GRS) are used interchangeably.

This page contains a collection of scripts and tools along with an explanation on published Single Nucleotide Polymorphism (SNP) based Polygenic Risk Scores (PRS) for common polygenic disease / traits where Human Leukocyte Antigen (HLA) region epistasis (gene vs gene interaction) is modelled. Additionally, we provide instructions and resources in order to verify your own scripts in the publicly available 1000 Genomes data. This work is a collective effort from researchers at the University of Exeter and elsewhere, please see references to corresponding publications below. For any questions about code on this page please contact Seth Sharp by email (s.sharp@exeter.ac.uk). For any questions about the individual PRS utilised here please contact the corresponding author of the relevant publication cited.

## Requirements

All scripts are designed to be run from a bash or compatible shell environment.

[PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) is required.

[Anaconda](https://www.anaconda.com) or Python (Version 3.8).

[PLINK genotyping data](https://www.cog-genomics.org/plink/1.9/formats) (.bed/.bim/.fam)

## Download
Download [hla-prs-toolkit.zip](https://github.com/sethsh7/hla-prs-toolkit/releases/download/0.1-beta/hla-prs-toolkit.zip)

Alternatively "git clone https://github.com/sethsh7/hla-prs-toolkit.git" to clone onto your working local directory or server.

## Scripts
### 1. PLINK2CALL - Hard calling of HLA haplogenotypes from SNP proxies
#### Usage:
```
python 1_plink2call.py --bfile <prefix> --mapping <mapping> 
```
This script takes your PLINK data containing a set of SNPs for which you wish to generate HLA haplogenotypes and a mapping file which should be text (space or tab delimited) in the format:
```
SNP ALLELE
snp1  allele1
snp2 allele2
snp3 allele3
...
```
The SNPs are matched on RSID and should match *exactly* with your PLINK .bim file.
The script will output the following results if succesful:

```
a) <prefix>_clean.txt - A table of allele counts by sample and mapped allele.
b) <prefix>_count.txt - Row wise sum of alleles per person for quality control.
c) <prefix>_cat.txt - List of categorical haplogenotypes by sample.
```

#### Filtering:
Since only 2 calls are possible per person (corresponding to 2 chromosomes) any samples with >2 calls will be filtered out in the same way missing genotypes are filtered. Work in progress - Implementing a custom allele prioritisation number system to eliminate excess SNP calls on a probabilistic basis.

### 2. CAT2SCORES - Assign scores to samples by HLA haplogenotype
#### Usage:
```
python 2_cat2scores.py --cat <your_cat.txt> --score <scorefile> 
```
The second script takes the by-sample categorical haplogenotype list file (c above) generated from PLINK2CALL and applies a scoring scheme. This can be EITHER on a full haplogenotype basis (one weight per combination) or on an additive basis (sum of each allele weight) or a mixture of both. The scorefile should be text (space or tab delimited) in the format:

```
ALLELE1 ALLELE2 BETA
allele1  allele2 value - Use this format for complete haplogenotypes
allele1 allele3 value
allele3 allele2 value
NULL allele1 value - For addition of an additive model use the NULL representation for the first column.
...
```
By default the script will NOT generate an additive term if a complete haplogenotype term is available (this differs from specific "interaction terms").
The script will output the following results file:

```
a) <prefix>_Scored.txt - List of samples and their corresponding scores as above
```

To generate a complete PRS (e.g. variants outside the HLA region) you can then sum this component with regular allele scoring generated using PLINK score function.

## SNP Lists
A number of scoring and mapping files are provided to utilise in generating scores from their referenced publications. There are versions available generated from SNPs used in the publications (recommended with TOPMED imputed data) or safer proxy SNPs that are more likely to be presented in all data (recommended with 1000Genomes or similar imputation).

### Type 1 Diabetes (T1D-PRS)
10-SNP / 30-SNP score ("GRS1") [1] - Original 10 and 30 SNP Exeter scores, they use a simple interaction model for DR3 and DR4 haplotypes.

67-SNP score ("GRS2") [2] - Updated 67 SNP Exeter score, complex interaction model, combines interaction and additive models (as described above), best prediction.

### Coeliac Disease (CD-PRS)
42-SNP score [3] - 42 SNP Exeter score, interaction model only consisting of DQ2.5, DQ2.2, DQ8.1 and DQ2.2 haplotypes.

## Example with Demo Data
In the scripts folder a subfolder "Demo" contains randomly generated data on 50 samples. You can run this code with either Run.sh or the following commands:
```
python 1_plink2call.py --bfile demo/demo_cohort --mapping demo/mapping.txt 
python 2_cat2scores.py --cat demo/demo_cohort_cat.txt --score demo/scorefile.txt
```
If all is succesful these scripts will terminate without error and you will have the output files as described above.

## Additional files
In tutorials a PDF guide to HLA nomenclature is available as background.

## FAQ
How do I get from a PLINK direct genotyping file to all of these additional SNPs?
You will need to impute your data, a useful tool for this is the [NIH TOPMED Imputation Server](https://imputation.biodatacatalyst.nhlbi.nih.gov). You will then need to convert your VCF of imputed dosages to PLINK format and extract the variants you need.

Should I imputed to TOPMED or 1000Genomes?
If you are able to impute to TOPMED this will eliminate many issues with missing SNPs. In addition 1000Genomes designs for PRS listed here are less accurate overall.

I am still missing SNPs listed how do I get alternatives?
The best way is to use the [NIH LDProxy tool](https://ldlink.nci.nih.gov/?tab=ldproxy) to look up the next best 1000Genomes proxy SNPs.

My SNPs are badly imputed (INFO<0.8) what should I do?
Use the same tool as above, if you cannot find a good proxy SNP then you may have to exclude this locus.

How do I apply this to my own 23andMe data? 
You will need to download your raw genome data and imputed it via a third party service.

How are missing genotype values handled?
They are set to 0 by default as the algorithm is conservative with calls.

Will this be updated? 
Yes, as time allows (infrequently at present).

## Supporting Publications

[1] A Type 1 Diabetes Genetic Risk Score Can Aid Discrimination Between Type 1 and Type 2 Diabetes in Young Adults, DiabetesCare 2016, RA Oram et al

[2] Development and Standardization of an Improved Type 1 Diabetes Genetic Risk Score for Use in Newborn Screening and Incident Diagnosis, DiabetesCare 2019, SA Sharp et al

[3] A single nucleotide polymorphism genetic risk score to aid diagnosis of coeliac disease: a pilot study in clinical care, AP&T 2020, SA Sharp et al

## License

Resources are provided under the GNU General Public License v3.0. For more information please LICENSE.md.
