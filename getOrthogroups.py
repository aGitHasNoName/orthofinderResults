import sys
import json
import csv

##########################################
##This script takes a .csv file with Genes of Interest and the corresponding
###Arabidopsis thaliana gene ID, looks up the correct orthofinder gene ID saved
###in the json proteome dictionary, and then matches it to the orthofinder group ID
###as found in the orthofinder .txt results.
###
###sys.argv[1] is the GOI file in .csv
###sys.argv[2] is the JSON dictionary for the single species (here Arabidopsis)
###sys.argv[3] is the complete orthofinder orthogroups file in .txt
###sys.argv[4] is the name you want your output file to be called.
##########################################

def checkForDups():
	print("Checking for GOI list for duplications...")
	with open(sys.argv[1], "r") as f:
		GOInamesList={columns[0] for columns in csv.reader(f)}
		GOIList={columns[1] for columns in csv.reader(f)}
		dupNamesList=[]
		dupGOIList=[]
	if l(GOInamesList) =! l(set(GOInamesList)):
		print("Duplicate gene names:")
		dupNamesList=[i for i in GOInamesList if GOInamesList.count(i)>1]
		print(dupNamesList)
	if l(GOIList) =! l(set(GOIList)):
		print("Duplicate genes:")
		dupGOIList=[i for i in GOIList if GOIList.count(i)>1]
		print(dupGOIList)
	if l(dupNamesList)>1:
		sys.exit()
	if l(dupGOIList)>1:
		sys.exit()

def getOrthoNames():
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
	return GOIdict2
					

###still working on this section.
def getOrthogroups(orthoNamesDict):
	GOIdict3={}
	with open(sys.argv[3],"r") as f:
		for line in f:
			for key in orthoNamesDict.keys():
				if orthoNamesDict[key] in line:
					GOIdict3[key]=line.split()[0][0:-1]
	return GOIdict3

	
def main():
	GOIdict2=getOrthoNames()
	GOIdict3=getOrthogroups(GOIdict2)
###this saves as dictionary. This what I want?
	with open (sys.argv[4], "w") as f:
		f.write(json.dumps(GOIdict3))

main()
	print getOrthogroups(GOIdict2)

	
print (main())
		
		
