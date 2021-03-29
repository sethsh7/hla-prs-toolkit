#####################################################################
##  plink2call - PLINK hard genotypes to HLA allele calls
#####################################################################

""" plink2call.py

	Usage:
		plink2call.py --bfile <bfile> --mapping <mapping>

	Options:
		--bfile	: Show this help message
		--mapping	: Training feature set

"""	
from docopt import docopt
import pandas as pd
import numpy as np
import subprocess
import sys
import os

#####################################################################
##  Main
#####################################################################
def main(docopt_args):
	bfile=docopt_args["<bfile>"]
	mapping=docopt_args["<mapping>"]

	#PLINK Location
	plink="/gpfs/mrc0/projects/Research_Project-MRC158833/programs/plink/plink --silent"

	#Generate frequencies
	print("Generating frequencies with PLINK...")
	command=plink+" --bfile "+bfile+" --freq --out "+bfile
	subprocess.run(command,shell=True)
	freq=pd.read_csv(bfile+".frq",header=0, delim_whitespace=True)
	ma=freq[["SNP","A1"]]

	#Append MAF and tagged allele to SNP matrix
	print("Matching SNP allele to HLA allele...")
	tags=pd.read_csv(mapping, header=0, sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
	vmap=pd.merge(ma,tags)

	#Use plink score function to generate a table of allele dosages	
	print("Generating table of allele dosages...")
	tmp=bfile+"_temp.tmp"
	for i in range(len(vmap)):
		scorefile=vmap[['SNP','A1']]
		scorefile['VAL']=1
		scorefile.iloc[[i]].to_csv(tmp,header=False, index=False, sep="\t")
		command=plink+" --bfile "+bfile+" --score "+tmp+" no-mean-imputation"
		subprocess.run(command,shell=True)
		temp=pd.read_csv("plink.profile",header=0, sep="\s+|\t+|\s+\t+|\t+\s+", 
									engine='python')
		temp['SCORE']=temp['SCORE']*2

		#Label the correct allele
		allele=str(vmap.loc[i,'ALLELE'])
		if i==0:
			table_hla=temp[['FID','IID','SCORE']]
			table_hla=table_hla.rename(columns = {'SCORE': allele})
		if i>0:
			table_hla[allele]=temp['SCORE']
	#Clean up and out
	command="rm "+bfile+".log "+bfile+".frq "+bfile+".nosex "+tmp+" 2> /dev/null"
	subprocess.run(command,shell=True)
	command="rm plink.profile plink.log plink.nosex 2> /dev/null"
	subprocess.run(command,shell=True)
	#table_hla.to_csv(bfile+"_dosage_anot.txt", header=True, index=False, sep="\t")
	#print("Success! Created "+bfile+"_dosage_anot.txt")

	#Sum rows and check
	print("Checking row sums for excess alleles...")
	table_hla['COUNT']=table_hla.iloc[:,3:].sum(axis=1).to_frame()
	table_count=table_hla[['FID','IID','COUNT']]
	table_count.to_csv(bfile+"_count.txt", header=True, index=False, sep="\t")
	print("Created count file for failure checking "+bfile+"_count.txt")
	table_clean=table_hla[(table_hla['COUNT'] < 3)]
	del table_clean['COUNT']
	table_clean.to_csv(bfile+"_table.txt", header=True, index=False, sep="\t")
	print("Success! Created cleaned table "+bfile+"_clean.txt")

	#Create categorised list
	print("Creating categorical list of genotypes per sample...")
	table_cat=table_clean[['FID','IID']].copy()
	table_cat['GENO1']="X"
	table_cat['GENO2']="X"
	for i in range(len(table_clean)):
		for j in range(2,len(table_clean.columns)):
			col=str(table_clean.columns[j])
			if table_clean.iloc[i,j]==2:
				col=table_clean.columns[j]
				table_cat.loc[table_cat.index[i],'GENO1']=col
				table_cat.loc[table_cat.index[i],'GENO2']=col
			elif table_clean.iloc[i,j]==1:
				if table_cat.loc[table_cat.index[i],'GENO1']=="X":
					table_cat.loc[table_cat.index[i],'GENO1']=col
				else:
					table_cat.loc[table_cat.index[i],'GENO2']=col
			
	table_cat.to_csv(bfile+"_cat.txt", header=True, index=False, sep="\t")
	print("Success! Created "+bfile+"_cat.txt")

	print("Finished.")

if __name__ == "__main__":
	args = docopt(__doc__)
	main(args)
