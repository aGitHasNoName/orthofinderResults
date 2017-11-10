import os
import sys
import json
import csv

###sys.argv[1] is species list file
###sys.argv[2] is orthogroup dictionary
###sys.argv[3] is name for output csv file

species_list=[line.split()[0] for line in open(sys.argv[1],"r")]
ortho_dict=json.loads(sys.argv[2])

output=open(sys.argv[3],"wb")
writer = csv.writer(output)

for key,value in ortho_dict.items():
	orthogroup=key
	for k,v in value:
		gene=k
		row=map(lambda x: v.count(x),species_list)
	    writer.writerow(row)
    
output.close()
		