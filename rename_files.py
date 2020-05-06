#!/usr/bin/env python3

#Author: Kelsey Florek
#Description: Renames files in a directory using a given csv file where column 1 is the current file identifer and column 2 is the value to rename to. Keeps old extension.

import os,sys
import csv
import argparse
import glob

#setup argparser to display help if no arguments
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument("csv_file",help="CSV or TSV file that has search strings and replacement strings")
parser.add_argument("search_column",type=int,help="column in file to search on (zero indexed)")
parser.add_argument("replacement_column",type=int,help="column in file to replace with (zero indexed)")
parser.add_argument("file_dir",help="Location of files to be renamed.")

args = parser.parse_args()

string_map = {}
with open(args.csv_file,'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile,dialect)
    for row in reader:
        s_string = row[args.search_column]
        r_string = row[args.replacement_column]
        string_map[s_string] = r_string

rename_files = []

os.chdir(args.file_dir)
print(os.getcwd())
for key in string_map:
    for file in glob.glob(f"*{key}*"):
        new_name = file.replace(key,string_map[key])
        rename_files.append([file,new_name])

for item in rename_files:
    print(f"Rename {item[0]} to {item[1]}")

do_continue = input("Do you wish to continue (y/n)? : ")
if do_continue == 'y' or do_continue == 'Y' or do_continue == 'yes' or do_continue == 'Yes':
    for item in rename_files:
        os.rename(item[0],item[1])
    print("Done.")
else:
    print("Quitting without renaming.")
