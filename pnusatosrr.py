#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
import sys
import re

#setup argparser to display help if no arguments
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument("pnusa_list",help="a text file that has the PNUSA numbers to search for, one per line")

args = parser.parse_args()
IDs = []
with open(args.pnusa_list,"r") as pnusa_numbers:
    for searchString in pnusa_numbers:
        searchString = searchString.strip()
        url = 'https://www.ncbi.nlm.nih.gov/sra/?term='+searchString
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('td',text=re.compile("SRR.*"))
        if results == []:
            print("Could not find: "+searchString)
        else:
            for result in results:
                print("Found: "+result.text+" Matching: "+searchString)
                IDs.append([searchString,result.text])
if IDs == []:
    print('Nothing found.')
    sys.exit(1)
with open("srr_list.csv",'w') as outfile:
    for idPair in IDs:
        outfile.write(idPair[0]+','+idPair[1]+'\n')
