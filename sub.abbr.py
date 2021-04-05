#!/usr/bin/env python3

import argparse, sys, os

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
	help='name of input file (REQUIRED)', required=True)
parser.add_argument('--batikan', action='store_true', default=False,
        help='Toggle if Batikan prepared the subs.')
args = parser.parse_args()

#list of items to replace
abbr_list = {'[gm]':'[gerilim müziği]',
             '[gmd]':'[gerilim müziği devam eder]',
             '[gmy]':'[gerilim müziği yükselir]',
             '[gmb]':'[gerilim müziği biter]',
             '[dm]':'[duygusal müzik]',
             '[dmd]':'[duygusal müzik devam eder]',
             '[dmy]':'[duygusal müzik yükselir]',
             '[dmb]':'[duygusal müzik biter]',
             '[nm]':'[neşeli müzik]',
             '[nmd]':'[neşeli müzik devam eder]',
             '[nmy]':'[neşeli müzik yükselir]',
             '[nmb]':'[neşeli müzik biter]',
             '[hm]':'[hareketli müzik]',
             '[hmd]':'[hareketli müzik devam eder]',
             '[hmy]':'[hareketli müzik yükselir]',
             '[hmb]':'[hareketli müzik biter]',
             '[gdm]':'[gerilimli duygusal müzik]',
             '[gdmd]':'[gerilimli duygusal müzik devam eder]',
             '[gdmy]':'[gerilimli duygusal müzik yükselir]',
             '[gdmb]':'[gerilimli duygusal müzik biter]',
             '[tç]':'[telefon çalar]',
             '[kç]':'[kapı çalar]',
             '[ka]':'[kapı açılır]',
             '[kk]':'[kapı kapanır]',
             '[kv]':'[kapı vurulur]',
             '[ai]':'[adam inler]',
             '[ss]':'[silah sesi]',
             '[ssl]':'[silah sesleri]',
             '[as]':'[arama sonlanır]',
             '[ge]':'[gerilim efekti]',
             '[at]':'[arama tonu]',
             '[ms]':'[mesaj sesi]'}

#items to replace if --batikan is toggled
batikan = {'Ø':']',
           '[gerilimli müzik]':'[gerilim müziği]',
           '?!':'?',
           '#':'♪',
           'aleyküm selam':'aleykümselam',
           'Aleyküm selam':'Aleykümselam',
           'Selamın aleyküm':'Selamünaleyküm',
           'selamın aleyküm':'selamünaleyküm',
           'vallaha':'vallahi',
           'Vallaha':'Vallahi',
           '[küfür eder]':'***',
           '<i>':'',
           '</i>':'',
           '[hareketli müzik]':'[gerilim müziği]'}

#list to write the output
buffer = list()

#open the input file and replace the items
try:
	with open(args.input, 'r') as script:
		content = script.read()
		for key in abbr_list:
			content = content.replace(key, abbr_list[key])
		if args.batikan:
			for key in batikan:
				content = content.replace(key, batikan[key])
		buffer.append(content)
except FileNotFoundError:
	sys.exit('Unable to open {}. Does the file exist?'.format(args.input))
except PermissionError:
	sys.exit('Unable to open {}. Check your file permissions.'.format(args.input))
except:
	sys.exit('Something broke.')


#change the input file's name
old_name = os.getcwd() + '/' + args.input
tokens = args.input.rsplit('.', 1)
new_name = os.getcwd() + '/' + tokens[0] + '-old.' + tokens[1]
os.rename(old_name, new_name)

#dump the buffer into a file
try:
	with open(args.input, 'w') as output:
		output.writelines(buffer)
		print("Items have been replaced in {}.".format(args.input))
except:
	sys.exit('Cannot write to {}.'.format(args.input))
