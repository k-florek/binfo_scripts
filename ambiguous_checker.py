#!/usr/bin/env python3
import sys, os
import Bio
from Bio import SeqIO
# Description: This script takes in a multifasta, counts the number of gaps and ambiguous characters and outputs a list of samples with greater than 450 gaps and ambiguous characters
# Author: Abigail Shockey
# Email: abigail.shockey@slh.wisc.edu
sitesNumber = 450 #threshold for calling pass/fail

d = {}
file_dir = sys.argv[1]
for root,dirs,files in os.walk(file_dir):
    for file in files:
        if ".fa" in files or ".fasta" in file:
            for seq_record in SeqIO.parse(file, "fasta"):
              no_gaps = sum(seq_record.seq.count(x) for x in ("-", "?", "N","n"))
              d[seq_record.id] = [no_gaps]

with open("fail.txt", 'w') as outfile:
  for samp in d:
    if d[samp][0] > sitesNumber:
      outfile.write(f"{samp}\n")
