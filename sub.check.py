#!/usr/bin/env python3

import argparse, sys, re, srt, datetime, math

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='name of input file (REQUIRED)', required=True)
parser.add_argument('-rs', '--readingspeed', action='store_true', default=False,
	help='Check reading speed.')
args = parser.parse_args()

general_check_items = {'double_space':'  ',
                 'space_before_period':' .',
                 'space_before_comma':' ,',
                 'space_before_question_mark':' ?',
                 'space_before_exclamation_mark':' !',
                 'missing_word(s)':'==',
                 'hala':'hala',
                 'ellipses':'...',
                 'an8':'an8'}

#open the file and check for issues
try:
	with open(args.input, 'r') as script:
		content = script.read()

		#go through general check
		def general_check():
			return_list = list()
			for key in general_check_items:
				occurences = content.count(general_check_items[key])
				if occurences == 0: pass
				else:
					results = key + ' : ' + str(occurences)
					return_list.append(results)
			space_after_dash = len(re.findall(r'^- ', content, flags=re.MULTILINE))
			if space_after_dash == 0: pass
			else: 
				results = 'space_after_dash : ' + str(space_after_dash)
				return_list.append(results)
			trailing_space = len(re.findall(r' $', content, flags=re.MULTILINE))
			if trailing_space == 0: pass
			else:
				results = 'trailing_space : ' + str(trailing_space)
				return_list.append(results)
			return return_list
		general_check = general_check()
		for item in general_check:
			print(item)

		#parse the subtitle file
		subtitles_generator = srt.parse(content)
		subtitles = list(subtitles_generator)

                #check if any line exceeds the maximum number of characters
		def chk_exceeding_lines():
			return_list = list()
			for x in subtitles:
				split_subs= list(x.content.split('\n'))
				for i in split_subs:
					if len(i) > 42:
						return_list.append(x.index)
			return return_list
		exceeding_lines = chk_exceeding_lines()
		if exceeding_lines:
			print("Exceeding maximum line length :", exceeding_lines)

                #check if there is any line that would fit into one line
		def chk_potential_oneliners():
			return_list = list()
			for x in subtitles:
				if "\n" not in x.content: pass
				else:
					if x.content.startswith("-"): pass
					else:
						if len("".join(filter(lambda i: i!='\n', x.content))) < 42:
							return_list.append(x.index)
			return return_list
		potential_oneliners = chk_potential_oneliners()
		if potential_oneliners:
			print("Lines that can fit into one line :", potential_oneliners)

		#check for maximum/minimum duration violation
		def chk_duration():
			max_dur = list()
			min_dur = list()
			for x in subtitles:
				duration_timedelta = x.end - x.start
				duration = duration_timedelta.total_seconds() * 1000
				if duration > 7000: max_dur.append(x.index)
				if duration < 833: min_dur.append(x.index)
			return max_dur, min_dur
		duration = chk_duration()
		if duration[0]:
			print("Lines over maximum duration :", duration[0])
		if duration[1]:
			print("Lines below minimum duration :", duration[1])


		#check for reading speed if toggled
		def chk_cps():
			return_list = list()
			for x in subtitles:
				duration_timedelta = x.end - x.start
				duration = duration_timedelta.total_seconds()
				line_length = len("".join(filter(lambda i: i!='\n', x.content)))
				cps = line_length / duration
				if cps > 17: return_list.append(x.index)
			return return_list

		if args.readingspeed:
			over_rs_limit = chk_cps()
			if over_rs_limit:
				print("Lines over reading speed limit :", over_rs_limit)

except FileNotFoundError:
        sys.exit('Unable to open {}. Does the file exist?'.format(args.input))
except PermissionError:
        sys.exit('Unable to open {}. Check your file permissions.'.format(args.input))
except:
        sys.exit('Something broke.')
