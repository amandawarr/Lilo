import sys
from itertools import product

#to run: python expand.py primers.csv > expanded_primers.csv

#partially borrowed from Darian Hole https://github.com/phac-nml/biohansel/issues/60
d = {
'A': ['A'],
'C': ['C'],
'G': ['G'],
'T': ['T'],
'R': ['A', 'G'],
'Y': ['C', 'T'],
'S': ['G', 'C'],
'W': ['A', 'T'],
'K': ['G', 'T'],
'M': ['A', 'C'],
'B': ['C', 'G', 'T'],
'D': ['A', 'G', 'T'],
'H': ['A', 'C', 'T'],
'V': ['A', 'C', 'G'],
'N': ['A', 'C', 'G', 'T'],}

def expand_degenerate_bases(seq):
   """return a list of all possible k-mers given a degenerate base"""

   return list(map("".join, product(*map(d.get, seq))))

primers={}
infile=open(sys.argv[1])
print("name,primerF,seqF,primerR,seqR")
next(infile)
for line in infile:
	line=line.rstrip()
	line=line.split(",")
	primers[line[0]]=[line[1],line[2],line[3],line[4]]	

for item in primers.keys():
	primers[item][1]=expand_degenerate_bases(primers[item][1].upper())
	primers[item][3]=expand_degenerate_bases(primers[item][3].upper())
	expanded=[[x,y] for x in primers[item][1] for y in primers[item][3]]
	for pair in expanded:
		print(",".join([item,primers[item][0],pair[0],primers[item][2], pair[1]]))
