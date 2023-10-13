
from itertools import product
from typing import List, Dict

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
    'N': ['A', 'C', 'G', 'T'],
}

def expand_degenerate_bases(seq: str) -> List[str]:
    """return a list of all possible k-mers given a degenerate base"""
    return list(map("".join, product(*map(d.get, seq.upper()))))

def expand_primers(input_file: str) -> List[str]:
    primers = {}
    output = []
    with open(input_file, 'r') as infile:
        next(infile)
        for line in infile:
            line = line.rstrip()
            line = line.split(",")
            primers[line[0]] = [line[1], line[2], line[3], line[4]]

    output.append("name,primerF,seqF,primerR,seqR")
    for item in primers.keys():
        primers[item][1] = expand_degenerate_bases(primers[item][1])
        primers[item][3] = expand_degenerate_bases(primers[item][3])
        expanded = [[x, y] for x in primers[item][1] for y in primers[item][3]]
        for pair in expanded:
            output.append(",".join([item, primers[item][0], pair[0], primers[item][2], pair[1]]))

    return output
