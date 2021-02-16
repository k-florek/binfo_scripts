#!/usr/bin/env python3

#Author: Kelsey Florek
#Description: Uses a file with a list of fasta header names and filteres the multifasta to only include those files.

import os,sys
import argparse
from Bio import SeqIO

#setup argparser to display help if no arguments
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument("list_file",help="list of sequence names to keep in fasta file, 1 sequence id per line")
parser.add_argument("fasta",help="fasta file to filter on")
parser.add_argument("--output","-o",help="name of output fasta default: \"filtered.fasta\"",default="filtered.fasta")
args = parser.parse_args()

def list_ids():
    identifiers = []

    with open(args.list_file, 'r') as fi:
        for line in fi:
            line = line.strip()
            identifiers.append(str(line).replace(">", ""))

    return identifiers

identifiers = list_ids()

with open(args.fasta) as original_fasta, open(args.output, 'w') as corrected_fasta:
    records = SeqIO.parse(original_fasta, 'fasta')
    for record in records:
        if record.id in identifiers:
            print("found:",record.id," adding to filtered fasta...")
            SeqIO.write(record, corrected_fasta, 'fasta')
