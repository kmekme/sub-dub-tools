#!/usr/bin/env python3

import argparse, sys, os
from xlsx2csv import Xlsx2csv

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='name of input file (REQUIRED)', required=True)
parser.add_argument('-k', '--knp', metavar='FILENAME',
	help='The list of knp terms (REQUIRED)', required=False)
args = parser.parse_args()

#print the excel file's name
print("<br><b>" + args.input + "</b><br><br>")

#convert the input xlsx file to csv
Xlsx2csv(args.input, outputencoding="utf-8").convert("temp.csv")

#dump the knp terms into a list
knp_terms = list()

with open(args.knp, 'r') as knp_list:
	content = knp_list.readlines()
	for line in content:
		knp_terms.append(line)

#open the dialogue list and check if there are any instances of the terms in the knp list
with open("temp.csv", 'r') as pldl:
	content = pldl.read()
	for term in knp_terms:
		term_new = term.strip('\n')
		occurences = content.count(term_new)
		if occurences > 0: print("{}: {}".format(term_new, occurences) + "<br>")
