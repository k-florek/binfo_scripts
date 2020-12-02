#!/usr/bin/env python3
import sys
import Bio
from Bio import SeqIO
# Description: This script takes in a multifasta, counts the number of gaps and ambiguous characters and outputs a list of samples with greater than 450 gaps and ambiguous characters
# Author: Abigail Shockey
# Email: abigail.shockey@slh.wisc.edu
sitesNumber = 450 #threshold for calling pass/fail

d = {}
fastaIN = sys.argv[1]
for seq_record in SeqIO.parse(fastaIN, "fasta"):
  no_gaps = sum(seq_record.seq.count(x) for x in ("-", "?", "N","n"))
  d[seq_record.id] = [no_gaps]
with open("fail.txt", 'w') as outfile:
  for samp in d:
    if d[samp][0] > sitesNumber:
      outfile.write(f"{samp}\n")
