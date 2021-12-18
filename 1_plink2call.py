#####################################################################
##  plink2call - PLINK hard genotypes to HLA allele calls
#####################################################################

""" plink2call.py

	Usage:
		plink2call.py --bfile <bfile> --mapping <mapping> --rank <ranking>

	Options:
		--bfile		: Show this help message
		--mapping	: Mapping file
		--rank		: Ranking file for HLA LD-tiebreak algorithm

"""	
from docopt import docopt
import pandas as pd
import numpy as np
import subprocess
import sys
import os

#PLINK Globalvar
plink="plink --silent"

##  Generate a SNP frequency matrix
def genSnpMatrix(bfile, mapping):
	#Generate frequencies
	print("Generating frequencies with PLINK...")
	command=plink+" --bfile "+bfile+" --freq --out "+bfile
	subprocess.run(command,shell=True)
	freq=pd.read_csv(bfile+".frq",header=0, delim_whitespace=True)
	ma=freq[["SNP","A1"]]


	#Append MAF and tagged allele to SNP matrix
	tags=pd.read_csv(mapping, header=0, sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
	vmap=pd.merge(ma,tags)
	return vmap

#Generate a table of HLA allele dosages
def genDosageTable(vmap, bfile, mapping):
	scores=bfile+"_temp.scores"
	for i in range(len(vmap)):
		scorefile=vmap[['SNP','A1']]
		scorefile['VAL']=1
		scorefile.iloc[[i]].to_csv(scores,header=False, index=False, sep="\t")
		command=plink+" --bfile "+bfile+" --score "+scores+" no-mean-imputation"
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
	command="rm "+bfile+".log "+bfile+".frq "+bfile+".nosex "+scores+" 2> /dev/null"
	subprocess.run(command,shell=True)
	command="rm plink.profile plink.log plink.nosex 2> /dev/null"
	subprocess.run(command,shell=True)
	return table_hla

#Sum rows and check
def toCategorical(table_dosage, rank):
	table_cat=table_dosage[['FID','IID']].copy()
	table_cat['GENO1']="X"
	table_cat['GENO2']="X"

	#Load ranking to resolve conflicts
	df=pd.read_csv(rank, sep="\t")
	ranking=pd.Series(df.DQ.values,index=df.RANK).to_dict()
	ranking.update(dict((ranking[k], k) for k in ranking) )

	#Create a temporary list
	#Loop over the row and add possible genotypes to the temporary list
	#Eliminate least likely (whilst list >3)
	for i in range(len(table_dosage)):
		calls = []

		#For the row add all possible calls to the calls array
		for j in range(2,len(table_dosage.columns)):
			col=str(table_dosage.columns[j])
			if table_dosage.iloc[i,j]==2:
				calls.extend([col, col])
			elif table_dosage.iloc[i,j]==1:
				calls.append(col)
	
		#Now loop over the calls array until its size 2
		while len(calls)!=2:
			if len(calls)>2:
				calls=dropLeastLikely(calls, ranking)
			if len(calls)<2:
				#add an X
				calls.append("X")

		#Add to categorical genotype array
		table_cat.loc[table_cat.index[i],'GENO1']=calls[0]
		table_cat.loc[table_cat.index[i],'GENO2']=calls[1]
	
	return table_cat

#Drop the least likely calls
def dropLeastLikely(calls, ranking):
	#Transform based on ranking and sort
	ranked=[]
	for call in calls:
		ranked.append(ranking[call])
	ranked.sort()

	#Transform back
	calls=[]
	for rank in ranked:
		calls.append(ranking[rank])
	calls.pop()
	return calls

#####################################################################
##  Main
#####################################################################
def main(docopt_args):
	bfile=docopt_args["<bfile>"]
	mapping=docopt_args["<mapping>"]
	rank=docopt_args["<ranking>"]

	vmap=genSnpMatrix(bfile,mapping)
	dosage=genDosageTable(vmap,bfile,mapping)
	hla=toCategorical(dosage,rank)
	
	#Output result
	hla.to_csv(bfile+"_cat.txt", header=True, index=False, sep="\t")
	print("Success! Created "+bfile+"_cat.txt")


if __name__ == "__main__":
	args = docopt(__doc__)
	main(args)
