#!/usr/bin/env python3

import argparse, re, os, sys
from time import sleep

#cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='Name of input file (REQUIRED)', required=True)
args = parser.parse_args()

#convert the rtf file to text
try:
	tokens = args.input.rsplit('.', 1)
	input_text = tokens[0] + '.txt'
	file = os.getcwd() + '/' + input_text
	os.popen('/usr/bin/unoconv -d document -f text "{}"'.format(args.input))
	while True:
		sleep(0.1)
		if os.path.isfile(file): break
except FileNotFoundError:
	sys.exit('Unable to open {}. Does the file exist?'.format(args.input))
except PermissionError:
	sys.exit('Unable to open {}. Check your file permissions.'.format(args.input))
except:
	sys.exit('Something broke when converting the rtf file to text.')

#list the characters
try:
	with open(file, 'r') as script:
		content = script.read()
		characters = re.findall(r'\[(.*?)\]', content)
		printed = list()
		for character in characters:
			if not character in printed:
				print("[{}]".format(character))
				printed.append(character)
except FileNotFoundError:
        sys.exit('Unable to open {}. Does the file exist?'.format(input_text))
except PermissionError:
        sys.exit('Unable to open {}. Check your file permissions.'.format(input_text))
except:
	sys.exit('Something broke when looking for terms.')

#delete the text file
try:
	os.remove(file)
except FileNotFoundError:
        sys.exit('Unable to open {}. Does the file exist?'.format(file))
except PermissionError:
        sys.exit('Unable to open {}. Check your file permissions.'.format(file))
except:
        sys.exit('Something broke when deleting {}.'.format(file))
