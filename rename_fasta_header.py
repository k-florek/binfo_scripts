#!/usr/bin/env python3

#Author: Kelsey Florek
#Description: Renames fasta header using the file name. Multi-fasta files will be labeled with index.

import os,sys
import argparse

#setup argparser to display help if no arguments
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument("file_dir",help="path to fasta files that need to be renamed")
parser.add_argument("--sars","-s",help="add \"hCoV-19/USA/\" to beginning and \"/<value>\" to end",type=str) 

args = parser.parse_args()

if(args.sars):
    prefix = "hCoV-19/USA/"
    postfix = "/" + args.sars
else:
    prefix = ""
    postfix = ""

for root,dirs,files in os.walk(args.file_dir):
    for file in files:
        if ".fa" in file or ".fasta" in file:
            header_name = ">" + prefix + file.split(".")[0] + postfix
            current_fasta_path = os.path.join(root,file)
            temp_fasta_path = os.path.join(root,"temp.fasta")
            print(f"Found fasta: {current_fasta_path}")
            print("Changing fasta headers...")
            with open(current_fasta_path,'r') as fasta_file:
                with open(temp_fasta_path,'w') as out_fasta:
                    counter = 1
                    for line in fasta_file:
                        if line.startswith('>'):
                            if counter == 1:
                                out_fasta.write(header_name+'\n')
                            else:
                                out_fasta.write(header_name+str(counter)+'\n')
                            counter += 1
                        else:
                            out_fasta.write(line)
            os.remove(current_fasta_path)
            os.rename(temp_fasta_path,current_fasta_path)
            print(f"Finished {current_fasta_path}")
print("Done.")
