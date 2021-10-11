![image](https://user-images.githubusercontent.com/12270542/136563821-5c850dcb-eb96-444f-aec1-17f6764d44dd.png)

Stitch together Nanopore tiled amplicon data using a reference guided approach

Tiled amplicon data, like those produced from primers designed with primal scheme (https://github.com/aresti/primalscheme), are typically assembled using methods that involve aligning them to a reference and polishing the reference into a sequence that represents the reads. This works very well for obtaining a genome with SNPs and small indels representative of the reads. However in cases where the reads cannot be mapped well to the reference (e.g. genomes containing hypervariable regions between primers) or in cases where large structrual variants are expected this method may fail as polishing tools expect the reference to originate from the reads.

Lilo uses a reference only to assign reads to the amplicon they originated from and to order and orient the polished amplicons, no reference sequence is in the final assembly. Once assigned to an amplicon, a read with high average base quality of roughly median length for that amplicon is selected as a reference and polished with up to 300x coverage three times with medaka. The polished amplicons have primers removed with porechop (fork: https://github.com/sclamons/Porechop-1) and are then assembled with scaffold_builder (https://github.com/metageni/Scaffold_builder). 

Lilo is likely more reliable on larger overlaps, but has been tested on SARS-CoV-2 with artic V3 primers with sensible results. It has also been tested on 7kb and 4kb amplicons with ~100-1000bp overlaps for ASFV, PRRSV-1 and PRRSV-2.

# Requirments not covered by conda
Install this fork of porechop and make sure it is in your path:
https://github.com/sclamons/Porechop-1

# Installation
*git clone https://github.com/amandawarr/Lilo  
cd Lilo  
conda install --file LILO.yaml  
conda install --file scaffold_builder.yaml*

# Usage
Lilo assumes your reads are in a folder called *raw/* and have the suffix *.fastq.gz.* Multiple samples can be processed at the same time.  
Lilo requires a config file detailing the location of a reference, a primer scheme (in the form of a primal scheme style bed file), and a primers.csv file (described below). Additionally the medaka model should be specified in accordance with the guppy model used to basecall the reads.

*conda activate LILO
snakemake -k -s /path/to/LILO --configfile /path/to/config.file --cores N*

It is recommended to run with -k so that one sample with insufficient coverage will not stop the other jobs completing.
# Input specifications
**config.file**: an example config file has been provided.  
**Primer scheme**: As output by primal scheme, removing alt primers. Bed file of primer alignment locations. Columns: reference name, start, end, primer name, pool (must end with 1 or 2).  
**Primers.csv**: Comma delimited, includes alt primers, **with header line**. Columns: amplicon_name, F_primer_name, F_primer_sequence, R_primer_name, R_primer_sequence. If there are ambiguous bases in any of the primers it is recommended to expand these, the script expand.py will expand the described csv into a longer csv with IUPAC codes expanded.

# Output
Lilo uses the names from raw/ to name the output file. For a file named "sample.fastq.gz", the final assembly will be named "sample_Scaffold.fasta", and files produced during the pipeline will be in a folder called "sample". The output will contain amplicons that had at least 40X full length coverage. Missing amplicons will be represented by Ns. Any ambiguity at overlaps will be indicated with IUPAC codes.

# Note
Use of the wrong fork for porechop will cause the pipeline to fail.  
Lilo is a work in progress and has been tested on a limited number of references, amplicon sizes, and overlap sizes, I recommend checking the results carefully.  
If the pipeline fails it is usually because there is insufficient coverage.  
The pipeline currently assumes that any structural variants do not change the length of the amplicon by more than 5%. If alt amplicons produce a product of a different length to the original amplicon they may not be allocated to their amplicon.
