#!/usr/bin/env python3

import argparse, re, datetime, os
from time import sleep

#cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='Name of input file (REQUIRED)', required=True)
parser.add_argument('-s', '--shift', metavar='TIME', type=int, default=20,
        help='Amount to shift by in seconds, default is 20. It can be negative')
parser.add_argument('-f', '--filetype', metavar='FILETYPE', type=str, default='rtf',
	choices=['rtf', 'txt', 'text'],
        help='Specify the file type as rtf, txt or text. Default is rtf.')
parser.add_argument('--hours', action='store_true', default=False,
        help='Use hh:mm:ss as timestamp format instead of mm:ss')
args = parser.parse_args()

# don't need to do anything to shift by 0
if args.shift == 0:
    sys.exit('Nothing to do.')

#split the file name for later use
tokens = args.input.rsplit('.', 1)

#convert the input file to text file
if args.filetype == 'rtf':
	try:
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
		sys.exit('Something broke when converting the rtf file to text')

# are we adding or subtracting?
add = True if args.shift > 0 else False

# get the shift amount
shift = datetime.timedelta(seconds=abs(args.shift))

# timestamp pattern to match
regex = '\d\d:\d\d' if not args.hours else '\d\d:\d\d:\d\d'
pattern = '%M:%S' if not args.hours else '%H:%M:%S'

# initialize list to write to output at the end
buffer = list()

#open the file
try:
	if args.filetype == 'rtf': script = file
	else: script = args.input
	with open(script, 'r') as script2:
		content = script2.readlines()

		#check and fix hours pattern
		if args.hours:
			content_string = ''.join(content)
			broken_hours_pattern = re.findall('^\d\d:\d\d$\n\[', content_string, flags=re.MULTILINE)
			if broken_hours_pattern:
				content_old = content.copy()
				content.clear()
				for broken_hours_pattern in content_old:
					fixed = re.sub(r'^(\d\d:\d\d)$', r'00:\1', broken_hours_pattern)
					content.append(fixed)
				content_old2 = content.copy()
				content.clear()
				broken_hours_pattern2 = re.findall('\(\d\d:\d\d\)', content_string, flags=re.MULTILINE)
				for broken_hours_pattern2 in content_old2:
					fixed2 = re.sub(r'\((\d\d:\d\d)\)', r'(00:\1)', broken_hours_pattern2)
					content.append(fixed2)
		#shift timecodes
		for line in content:
		            matches = re.findall(regex, line)
		            for match in matches:
		                timestamp = datetime.datetime.strptime(match, pattern)
		                newtime = timestamp + shift if add else timestamp - shift
		                line = line.replace(match, newtime.strftime(pattern))
		            buffer.append(line)

except:
	sys.exit('Something broke during shifting.')

#fix inconsistent use of tabs and spaces
try:
	buffer_old = buffer.copy()
	buffer_string= ''.join(buffer)
	buffer.clear()
	inconsistent_use = re.findall(r"\](?!\s/)\s+", buffer_string, flags=re.MULTILINE)
	if inconsistent_use:
		for inconsistent_use in buffer_old:
			fixed3 = re.sub(r"\](?!\s/)\s+", "]\t", inconsistent_use)
			buffer.append(fixed3)
except:
	sys.exit('Something broke when trying to fix inconsistent use of tabs and spaces.')

#dump buffer to a text file
try:
	buffer_file = tokens[0] + '-shifted.txt'
	with open(buffer_file, 'w') as temp_file:
		temp_file.writelines(buffer)
except PermissionError:
	sys.exit("Can't create {}. Permission denied.".format(buffer_file))
except:
	sys.exit("Something broke when creating the text file.")

#convert the temp file into rtf
if args.filetype == 'rtf':
	try:
			output = tokens[0] + '-shifted.rtf'
			output_file = os.getcwd() + '/' + output
			os.popen('/usr/bin/unoconv -f rtf -o "{}" {}'.format(output, buffer_file))
			while True:
				sleep(0.1)
				if os.path.isfile(output_file): break
	except:
		sys.exit('Something broke when converting the text file to rtf.')

#delete the files generated by the script
try:
	if args.filetype == 'rtf': os.remove(file)
	if args.filetype == 'rtf': os.remove(buffer_file)
except FileNotFoundError:
	sys.exit('The files generated by the files do not exist.')
except PermissionError:
	sys.exit("Can't delete the files the script created.")
except:
	sys.exit("Something broke trying to delete the script generated files.")
