#!/usr/bin/env python3

import argparse, sys, re, datetime, os
from time import sleep

#cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='name of input file (REQUIRED)', required=True)
parser.add_argument('-s', '--shift', metavar='TIME', type=int, default=20,
        help='amount to shift by in seconds, default is 20. can be negative')
parser.add_argument('--hours', action='store_true', default=False,
        help='use hh:mm:ss as timestamp format instead of mm:ss')
args = parser.parse_args()

# don't need to do anything to shift by 0
if args.shift == 0:
    sys.exit('Nothing to do.')

#convert the input file to text file
try:
	tokens = args.input.rsplit('.', 1)
	input_text = tokens[0] + '.txt'
	file = os.getcwd() + '/' + input_text
	os.popen('/usr/bin/unoconv -d document -f text {}'.format(args.input))
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
	with open(file, 'r') as script:
		content = script.readlines()

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
	buffer_new = list()
        for line in buffer:
            buffer_new.append("\t".join(line.split(None, 1)))
        # do something with buffer_new
except:
	sys.exit('Something broke when trying to fix inconsistent use of tabs and spaces.')


#dump buffer to a text file
try:
	with open('shifted.temp', 'w') as temp_file:
		temp_file.writelines(buffer)
except PermissionError:
	sys.exit("Can't create shifted.temp. Permission denied.")
except:
	sys.exit("Something broke when creating the text file.")

#convert the temp file into rtf
try:
	output = tokens[0] + '-shifted.rtf'
	output_file = os.getcwd() + '/' + output
	os.popen('/usr/bin/unoconv -f rtf -o {} {}'.format(output, 'shifted.temp'))
	while True:
		sleep(0.1)
		if os.path.isfile(output_file): break
except:
	sys.exit('Something broke when converting the text file to rtf.')

#delete the files generated by the script
try:
	os.remove(file)
	os.remove("shifted.temp")
except FileNotFoundError:
	sys.exit('The files generated by the files do not exist.')
except PermissionError:
	sys.exit("Can't delete the files the script created.")
except:
	sys.exit("Something broke trying to delete the script generated files.")
