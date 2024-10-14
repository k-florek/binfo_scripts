#!/usr/bin/env python3

import os
import sys
import re
import argparse

#setup argparser to display help if no arguments
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument("path",help="Path to folder with each flowcell results")

args = parser.parse_args()

# dictionary to hold sample names and paths
fileProc = {}

# regular expressions used to dissect the sample name from the filename.
cutPatterns = ["^\w+_pass_","_........_........_\d+\.fastq\.gz"]

# traverse path and find all ".fastq.gz" files and sort them into the dictionary
for root,dir,files in os.walk(args.path,topdown=False):
    for name in files:
        p = os.path.abspath(os.path.join(root,name))
        if "_pass_" in name and ".fastq.gz" in name:
            sampleName = re.sub(cutPatterns[1],"",re.sub(cutPatterns[0],"",name))
            if sampleName not in fileProc.keys():
                fileProc[sampleName] = [p]
            else:
                fileProc[sampleName].append(p)

# check if merged_fastq exists and exit if does
if os.path.isdir(os.path.join(args.path,"merged_fastq")):
    print("There is already a 'merged_fastq' directory, please remove the directory before running this script.")
    sys.exit(1)

# concatenate fastq files
for key in fileProc:
    print(f"Merging {key}...",end="",flush=True)
    for file in fileProc[key]:
        fc = os.path.basename(file).split("_pass_")[0]
        p = os.path.join(args.path,"merged_fastq",fc)
        os.makedirs(p,exist_ok=True)
        with open(os.path.join(p,f"{key}.fastq.gz"), 'ab') as outfile:
            with open(file,'rb') as infile:
                for line in infile:
                    outfile.write(line)
    print("  Done")

print("Completed fastq merging.")