#!/usr/bin/env python3

import argparse, sys, os
from xlsx2csv import Xlsx2csv

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='name of input file (REQUIRED)', required=True)
parser.add_argument('-k', '--knp', metavar='FILENAME',
	help='The list of knp terms (REQUIRED)', required=True)
args = parser.parse_args()

#convert the input xlsx file to csv
try:
	Xlsx2csv(args.input, outputencoding="utf-8").convert("temp.csv")
except FileNotFoundError:
        sys.exit('Unable to open {}. Does the file exist?'.format(args.input))
except PermissionError:
        sys.exit('Unable to open {}. Check your file permissions.'.format(args.input))
except:
        sys.exit('Something broke trying to convert the excel file into csv.')

#dump the knp terms into a list
try:
	knp_terms = list()
	with open(args.knp, 'r') as knp_list:
		content = knp_list.readlines()
		for line in content:
			knp_terms.append(line)
except FileNotFoundError:
        sys.exit('Unable to open {}. Does the file exist?'.format(args.knp))
except PermissionError:
        sys.exit('Unable to open {}. Check your file permissions.'.format(args.knp))
except:
        sys.exit('Something broke trying to write the knp terms into a list.')

#open the dialogue list and check if there are any instances of the terms in the knp list
try:
	with open("temp.csv", 'r') as pldl:
		content = pldl.read()
		#print the excel file's name
		print("<br><b>" + args.input + "</b><br><br>")
		for term in knp_terms:
			term_new = term.strip('\n')
			occurences = content.upper().count(term_new.upper())
			if occurences > 0: print("{}: {}".format(term_new, occurences) + "<br>")
except FileNotFoundError:
        sys.exit('Unable to open temp.csv. Does the file exist?')
except PermissionError:
        sys.exit('Unable to open temp.csv. Check your file permissions.')
except:
        sys.exit('Something broke trying to go through the csv file.')

#delete temp.csv
try:
	os.remove("temp.csv")
except FileNotFoundError:
        sys.exit('Unable to open temp.csv. Does the file exist?')
except PermissionError:
        sys.exit('Unable to open temp.csv. Check your file permissions.')
except:
        sys.exit('Something broke trying to delete temp.csv')
