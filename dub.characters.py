#!/usr/bin/env python3

import argparse, re, os
from time import sleep

#cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='Name of input file (REQUIRED)', required=True)
args = parser.parse_args()

#convert the rtf file to text
tokens = args.input.rsplit('.', 1)
input_text = tokens[0] + '.txt'
file = os.getcwd() + '/' + input_text
os.popen('/usr/bin/unoconv -d document -f text "{}"'.format(args.input))
while True:
	sleep(0.1)
	if os.path.isfile(file): break

#list the characters
with open(file, 'r') as script:
	content = script.read()

	characters = re.findall(r'\[(.*?)\]', content)
	printed = list()
	for character in characters:
		if not character in printed:
			print("[{}]".format(character))
			printed.append(character)


#delete the text file
os.remove(file)
