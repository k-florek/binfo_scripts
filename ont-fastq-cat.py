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

parser = MyParser(description="This python script scans through the ONT output directory and concatenates the passing reads by placing them in a new folder named by the barcode folder.")
parser.add_argument("flowcell_path",help="Path to folder containing flowcell data, eg 20000101_1000_X1_ABC12345_ab123c4d")
parser.add_argument("-o",default="combined_fastq_passing",help="Path where combined fastqs should be output, defaults to 'combined_fastq_passing' in the flowcell path")
parser.add_argument("-p",default="_pass_",help="Passing identifier in sample name, defaults to '_pass_'")

args = parser.parse_args()

# dictionary to hold sample names and paths
fileProc = {}

# regular expressions used to dissect the sample name from the filename.
cutPatterns = [f"^\w+{args.p}","_........_........_\d+\.fastq\.gz"]

# traverse path and find all ".fastq.gz" files and sort them into the dictionary
for root,dir,files in os.walk(args.flowcell_path,topdown=False):
    for name in files:
        p = os.path.abspath(os.path.join(root,name))
        if args.p in name and ".fastq.gz" in name:
            sampleName = re.sub(cutPatterns[1],"",re.sub(cutPatterns[0],"",name))
            if sampleName not in fileProc.keys():
                fileProc[sampleName] = [p]
            else:
                fileProc[sampleName].append(p)

# check if combined_fastq_passing exists and exit if does
if os.path.isdir(os.path.join(args.flowcell_path,args.o)):
    print(f"There is already a {args.o} directory, please remove the directory before running this script.")
    sys.exit(1)

# concatenate fastq files
for key in fileProc:
    print(f"Merging {key}...",end="",flush=True)
    for file in fileProc[key]:
        fc = os.path.basename(file).split(args.p)[0]
        p = os.path.join(args.flowcell_path,args.o,fc)
        os.makedirs(p,exist_ok=True)
        with open(os.path.join(p,f"{key}.fastq.gz"), 'ab') as outfile:
            with open(file,'rb') as infile:
                for line in infile:
                    outfile.write(line)
    print("  Done")

print("Completed fastq concatenation.")