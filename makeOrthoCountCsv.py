import os
import sys
import json
import csv
import re

###sys.argv[1] is species list file
###sys.argv[2] is orthogroup dictionary
###sys.argv[3] is name for output csv file

species_list=[line.split("\t")[0].rstrip("\n") for line in open(sys.argv[1],"r")]
with open(sys.argv[2],"r") as f:
	for line in f:
		ortho_dict=json.loads(line)

output=open(sys.argv[3],"w")
writer = csv.writer(output)
header=[line.split("\t")[0].rstrip("\n") for line in open(sys.argv[1],"r")]
header.insert(0,"gene")
header.insert(0, "orthogroup")
writer.writerow(header)

for key,value in ortho_dict.items():
	orthogroup=key
	for k,v in value.items():
		gene=k
		copies=[re.sub("\d","",i) for i in v]
		row=list(map(lambda x: copies.count(x),species_list))
		row.insert(0,gene)
		row.insert(0,key)
		writer.writerow(row)

output.close()
		