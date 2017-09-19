import sys
import json
import csv
import os
from Bio import SeqIO

##########################################
##This script takes a .csv file with Genes of Interest and the corresponding
###Arabidopsis thaliana gene ID, looks up the correct orthofinder gene ID saved
###in the json proteome dictionary, and then matches it to the orthofinder group ID
###as found in the orthofinder .txt results.
###
###sys.argv[1] is the GOI file in .csv
###sys.argv[2] is the JSON dictionary for the single species (here Arabidopsis)
###sys.argv[3] is the complete orthofinder orthogroups file in .txt
###sys.argv[4] is the name you want your GOI:orthogroup dictionary to be called
###sys.argv[5] is the path to the folder where the GOI files should be made
###sys.argv[6] is the path to the folder with the full genomes
##########################################

def checkForDups():
	print("Checking for GOI list for duplications...")
	with open(sys.argv[1], "r") as f:
		GOInamesList={columns[0] for columns in csv.reader(f)}
		GOIList={columns[1] for columns in csv.reader(f)}
		dupNamesList=[]
		dupGOIList=[]
	if len(GOInamesList) != len(set(GOInamesList)):
		print("Duplicate gene names:")
		dupNamesList=[i for i in GOInamesList if GOInamesList.count(i)>1]
		print(dupNamesList)
	if len(GOIList) != len(set(GOIList)):
		print("Duplicate genes:")
		dupGOIList=[i for i in GOIList if GOIList.count(i)>1]
		print(dupGOIList)
	if len(dupNamesList)>=1:
		sys.exit()
	if len(dupGOIList)>=1:
		sys.exit()

def getOrthoNames():
	print("Getting Orthofinder gene names from species dictionary...")
	with open(sys.argv[1], "r") as f:
		GOIdict={columns[0]:columns[1] for columns in csv.reader(f)}
	GOIdict2={}
	with open(sys.argv[2], "r") as f:
		for line in f:
			ATdict=json.loads(line)
			for k in ATdict.keys():
				for key,value in GOIdict.items():
					if value in ATdict[k][1][0:-2]:
						GOIdict2[key]=k
	###Next 6 lines check that all GOIs were found. Doesn't quit, but tells you which genes weren't found.
	if len(GOIdict)!=len(GOIdict2):
		print ("Not all GOIs found:")
		notFoundDict={key:value for key,value in GOIdict.items() if key not in GOIdict2.keys()}
		print ("Check for extra spaces, typos in GOI csv: "+notFoundDict)
	else:
		print ("All GOIs found")
	return GOIdict2
					

def getOrthogroups(orthoNamesDict):
	print ("Getting orthogroups...")
	GOIdict3={}
	with open(sys.argv[3],"r") as f:
		for line in f:
			###Next 4 lines ensure correct match (e.g. at1 won't match to at10)
			lineDict={}
			i=line.split()
			k=i[0][0:-1]
			lineDict[k]=list(j for j in i[1:])
			for key,value in orthoNamesDict.items():
				if value in lineDict[k]:
					GOIdict3[key]=lineDict
	###Next lines check that all GOIs were found.
	if len(orthoNamesDict)!=len(GOIdict3):
		print ("Not all GOIs found:")
		notFoundDict={key:value for key,value in orthoNamesDict.items() if key not in GOIdict3.keys()}
		print (notFoundDict)
	else:
		print ("All GOIs found")
	return GOIdict3


def checkOrthogroupsForDups(orthogroupsDict):
	print ("Checking for duplicate orthogroups and merging genes...")
	groupDict={}
	dupsDict={}
	GOIdict4={}
	for key,value in orthogroupsDict.items():
		for i in value.keys():
			if i not in groupDict.keys():
				groupDict[i]=[key]
			else:
				groupDict[i].append(key)
	for key,value in groupDict.items():
		if len(value) > 1:
			dupsDict[key]=value
	for key,value in orthogroupsDict.items():
		for k in value.keys():
			if k not in dupsDict.keys():
				GOIdict4[key]=value
	for key in dupsDict.keys():
		sampV=dupsDict[key][0]
		newKey="_".join(dupsDict[key])
		GOIdict4[newKey]=orthogroupsDict[sampV]
	print ("{} unique orthogroups identified.".format(str(len(GOIdict4)))
	return GOIdict4


###Split into two functions: makeFolders and makeFiles? But it's done, so maybe not.
def makeFoldersAndFiles(orthogroupsDict):
	print ("Making folders and fasta files...")
	for key in orthogroupsDict.keys():
		dirPath="{}/{}".format(sys.argv[5],key)
		if not os.path.exists(dirPath):
			os.makedirs(dirPath)
		writeFile=open("{}/{}.fa".format(dirPath,key),"w")
		groupDict=orthogroupsDict[key]
		for value in groupDict.values():
			for ortholog in value:
				species="".join([c for c in ortholog if c.isalpha()])
				with open("{}/{}.fa".format(sys.argv[6],species), "r") as f:
					for record in SeqIO.parse(f, "fasta"):
						if ortholog==record.id:
							SeqIO.write(record,writeFile,"fasta")
		writeFile.close()
							

	
def main():
	checkForDups()
	GOIdict2=getOrthoNames()
	GOIdict3=getOrthogroups(GOIdict2)
	GOIdict4=checkOrthogroupsForDups(GOIdict3)
	###this saves as dictionary. This what I want?
	with open (sys.argv[4], "w") as f:
		f.write(json.dumps(GOIdict4))
	makeFoldersAndFiles(GOIdict4)

main()


		
