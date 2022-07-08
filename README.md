# Polygenic Risk Score (PRS) Toolkit for HLA

This toolkit is for generating Single Nucleotide Polymorphism (SNP) based Polygenic Risk Scores (PRS) for common polygenic disease / traits where it is necessary to impute HLA alleles using single SNPs and model epistasis.

The major advantage of this is the ability to assign HLA haplogenotypes (e.g DR3/DQ2.5) using SNPs alone which is quicker and more cost effective than typical methods such array imputation and HLA typing. Demo data and guide files are provided for our own published PRS but these could be easily generated in order to apply code to your own HLA calling and or scoring schema.

For any questions about code on this page please contact Seth Sharp by email (Ssharp@stanford.edu).

## Updates
7/8/2022 - Updated the SNP lists for TOPMED (r2) imputations as per NIH TOPMED server\
7/8/2022 - Reordered the SNP lists folder to split by TOPMED vs 1000G imputation\
7/8/2022 - Added a wrapper script

## Download
[hla-prs-toolkit-0.21b.zip](https://github.com/sethsh7/hla-prs-toolkit/releases/download/0.21-beta/hla-prs-toolkit-0.21b.zip) - Latest version of all scripts and demo data.\
Alternatively "git clone https://github.com/sethsh7/hla-prs-toolkit.git" to clone onto your working local directory or server.

## Requirements
[PLINK 1.9](https://www.cog-genomics.org/plink/1.9/) is required.\
[Anaconda](https://www.anaconda.com) or Python (Version 3.8).\
[PLINK genotyping data](https://www.cog-genomics.org/plink/1.9/formats) (.bed/.bim/.fam)

## Scripts
### 1. PLINK2CALL - Hard calling of HLA haplogenotypes from SNP proxies
#### Usage:
```
python 1_plink2call.py --bfile <prefix> --mapping <mapping> --rank <ranking>
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
Additionally a ranking file is now needed to resolve impossible calls and invoke the HLA-LD tiebreak algorithm (see below).
### HLA LD-Tiebreak algorithm (new December 2021)
Since only 2 HLA calls are possible per person (corresponding to 2 chromosomes) any samples with >2 calls were previously filtered out. This is no longer the case as an (unpublished) HLA LD-Tiebreak algorithm as been added based on a reference ranking. The reference ranking provided has been calculated based on the following:

Ranking score = SNP LD (r2) * Prior odds (frequency in reference population)

The reference prior odds were generated from HLA typing data take from [Klitz et al (2003)](https://pubmed.ncbi.nlm.nih.gov/12974796/) and are therefore appropriate for a White US (European ancestry) population. This scenario typically occurs either in genotyping miscalls or in non-European ancestry samples.You can generate your own reference if you have other ethnicity data from any published HLA typing database. Our internal data shows ~72% of calls recovered this way are accurate compared to HLA typing. 

The ranking file provided must have the following format:
```
ALELE RANK
allele1 1
allele2 2
allele3 3
...
```
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
Scoring and mapping files are provided to generate scores from our publications with either TOPMED or 1000G imputed data.

#### Type 1 Diabetes (T1D-GRS)
10-SNP / 30-SNP score ("GRS1") [1] - Original 10 and 30 SNP Exeter scores, they use a simple interaction model for DR3 and DR4 haplotypes.

67-SNP score ("GRS2") [2] - Updated 67 SNP Exeter score, complex interaction model, combines interaction and additive models (as described above), best prediction.

#### Coeliac Disease (CD-GRS)
42-SNP score [3] - 42 SNP Exeter score, interaction model only consisting of DQ2.5, DQ2.2, DQ8.1 and DQ2.2 haplotypes.

## Example with Demo Data
In the scripts folder a subfolder "Demo" contains randomly generated data on 50 samples. Run with RunDemo.sh.

## FAQ
#### I have array genotyping data. How do I get the desired SNPs?
You will need to impute your data using [NIH Imputation Server](https://imputation.biodatacatalyst.nhlbi.nih.gov). You will then need to convert your VCF of imputed dosages to PLINK format and extract the variants you need.

#### Should I impute to HRC, TOPMED or 1000Genomes?
We have provided SNP lists for TOPMED r2 and 1000 Genomes as an alternative.

#### How do I apply this to my own 23andMe data? 
You will need to download your raw genome data and impute it via a third party service.

#### How are missing genotype values handled?
They are set to 0 by default as the algorithm is conservative with calls.

## Supporting Publications

[1] *"A Type 1 Diabetes Genetic Risk Score Can Aid Discrimination Between Type 1 and Type 2 Diabetes in Young Adults"*, DiabetesCare 2016, RA Oram et al

[2] *"Development and Standardization of an Improved Type 1 Diabetes Genetic Risk Score for Use in Newborn Screening and Incident Diagnosis"*, DiabetesCare 2019, SA Sharp et al

[3] *"A single nucleotide polymorphism genetic risk score to aid diagnosis of coeliac disease: a pilot study in clinical care"*, AP&T 2020, SA Sharp et al

## License

Resources are provided under the GNU General Public License v3.0. For more information please LICENSE.md.
