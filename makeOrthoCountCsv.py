import os
import sys
import json
import csv

###sys.argv[1] is species list file
###sys.argv[2] is orthogroup dictionary
###sys.argv[3] is name for output csv file

species_list=[line.split("\t")[0].rstrip("\n") for line in open(sys.argv[1],"r")]
with open(sys.argv[2],"r") as f:
	for line in f:
		ortho_dict=json.loads(line)

output=open(sys.argv[3],"wb")
writer = csv.writer(output)

for key,value in ortho_dict.items():
	orthogroup=key
	for k,v in value:
		gene=k
		row=map(lambda x: v.count(x),species_list)
	    writer.writerow(row)
    
output.close()
		