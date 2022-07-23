#!/usr/bin/env python3

import argparse, sys, os

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
	help='name of input file (REQUIRED)', required=False)
parser.add_argument('--batikan', action='store_true', default=False,
        help='Toggle if Batikan prepared the subs.')
parser.add_argument('-l', '--list', action='store_true', default=False,
	help='Print the abbrevation list.')
args = parser.parse_args()

#list of items to replace
abbr_list = {'[gm]':'[gerilim müziği]',
             '8gm]':'[gerilim müziği]',
             '[gm9':'[gerilim müziği]',
             '8gm9':'[gerilim müziği]',
             '[gmd]':'[gerilim müziği devam eder]',
             '8gmd]':'[gerilim müziği devam eder]',
             '[gmd9':'[gerilim müziği devam eder]',
             '8gmd9':'[gerilim müziği devam eder]',
             '[gmy]':'[gerilim müziği yükselir]',
             '8gmy]':'[gerilim müziği yükselir]',
             '[gmy9':'[gerilim müziği yükselir]',
             '8gmy9':'[gerilim müziği yükselir]',
             '[gmb]':'[gerilim müziği biter]',
             '8gmb]':'[gerilim müziği biter]',
             '[gmb9':'[gerilim müziği biter]',
             '8gmb9':'[gerilim müziği biter]',
             '[gmbb]':'[gerilim müziği bozulur ve biter]',
             '8gmbb]':'[gerilim müziği bozulur ve biter]',
             '[gmbb9':'[gerilim müziği bozulur ve biter]',
             '8gmbb9':'[gerilim müziği bozulur ve biter]',
             '[dm]':'[duygusal müzik]',
             '8dm]':'[duygusal müzik]',
             '[dm9':'[duygusal müzik]',
             '8dm9':'[duygusal müzik]',
             '[dmd]':'[duygusal müzik devam eder]',
             '8dmd]':'[duygusal müzik devam eder]',
             '[dmd9':'[duygusal müzik devam eder]',
             '8dmd9':'[duygusal müzik devam eder]',
             '[dmy]':'[duygusal müzik yükselir]',
             '8dmy]':'[duygusal müzik yükselir]',
             '[dmy9':'[duygusal müzik yükselir]',
             '8dmy9':'[duygusal müzik yükselir]',
             '[dmb]':'[duygusal müzik biter]',
             '8dmb]':'[duygusal müzik biter]',
             '[dmb9':'[duygusal müzik biter]',
             '8dmb9':'[duygusal müzik biter]',
             '[dmbb]':'[duygusal müzik bozulur ve biter]',
             '8dmbb]':'[duygusal müzik bozulur ve biter]',
             '[dmbb9':'[duygusal müzik bozulur ve biter]',
             '8dmbb9':'[duygusal müzik bozulur ve biter]',
             '[nm]':'[neşeli müzik]',
             '8nm]':'[neşeli müzik]',
             '[nm9':'[neşeli müzik]',
             '8nm9':'[neşeli müzik]',
             '[nmd]':'[neşeli müzik devam eder]',
             '8nmd]':'[neşeli müzik devam eder]',
             '[nmd9':'[neşeli müzik devam eder]',
             '8nmd9':'[neşeli müzik devam eder]',
             '[nmy]':'[neşeli müzik yükselir]',
             '8nmy]':'[neşeli müzik yükselir]',
             '[nmy9':'[neşeli müzik yükselir]',
             '8nmy9':'[neşeli müzik yükselir]',
             '[nmb]':'[neşeli müzik biter]',
             '8nmb]':'[neşeli müzik biter]',
             '[nmb9':'[neşeli müzik biter]',
             '8nmb9':'[neşeli müzik biter]',
             '[nmbb]':'[neşeli müzik bozulur ve biter]',
             '8nmbb]':'[neşeli müzik bozulur ve biter]',
             '[nmbb9':'[neşeli müzik bozulur ve biter]',
             '8nmbb9':'[neşeli müzik bozulur ve biter]',
             '[hm]':'[hareketli müzik]',
             '8hm]':'[hareketli müzik]',
             '[hm9':'[hareketli müzik]',
             '8hm9':'[hareketli müzik]',
             '[hmd]':'[hareketli müzik devam eder]',
             '8hmd]':'[hareketli müzik devam eder]',
             '[hmd9':'[hareketli müzik devam eder]',
             '8hmd9':'[hareketli müzik devam eder]',
             '[hmy]':'[hareketli müzik yükselir]',
             '8hmy]':'[hareketli müzik yükselir]',
             '[hmy9':'[hareketli müzik yükselir]',
             '8hmy9':'[hareketli müzik yükselir]',
             '[hmb]':'[hareketli müzik biter]',
             '8hmb]':'[hareketli müzik biter]',
             '[hmb9':'[hareketli müzik biter]',
             '8hmb9':'[hareketli müzik biter]',
             '[hmbb]':'[hareketli müzik bozulur ve biter]',
             '8hmbb]':'[hareketli müzik bozulur ve biter]',
             '[hmb9]':'[hareketli müzik bozulur ve biter]',
             '8hmbb9':'[hareketli müzik bozulur ve biter]',
             '[gdm]':'[duygusal gerilim müziği]',
             '8gdm]':'[duygusal gerilim müziği]',
             '[gdm9':'[duygusal gerilim müziği]',
             '8gdm9':'[duygusal gerilim müziği]',
             '[gdmd]':'[duygusal gerilim müziği devam eder]',
             '8gdmd]':'[duygusal gerilim müziği devam eder]',
             '[gdmd9':'[duygusal gerilim müziği devam eder]',
             '8gdmd9':'[duygusal gerilim müziği devam eder]',
             '[gdmy]':'[duygusal gerilim müziği yükselir]',
             '8gdmy]':'[duygusal gerilim müziği yükselir]',
             '[gdmy9':'[duygusal gerilim müziği yükselir]',
             '8gdmy9':'[duygusal gerilim müziği yükselir]',
             '[gdmb]':'[duygusal gerilim müziği biter]',
             '8gdmb]':'[duygusal gerilim müziği biter]',
             '[gdmb9':'[duygusal gerilim müziği biter]',
             '8gdmb9':'[duygusal gerilim müziği biter]',
             '[tç]':'[telefon çalar]',
             '8tç]':'[telefon çalar]',
             '[tç9':'[telefon çalar]',
             '8tç9':'[telefon çalar]',
             '[kç]':'[kapı çalar]',
             '8kç]':'[kapı çalar]',
             '[kç9':'[kapı çalar]',
             '8kç9':'[kapı çalar]',
             '[ka]':'[kapı açılır]',
             '8ka]':'[kapı açılır]',
             '[ka9':'[kapı açılır]',
             '8ka9':'[kapı açılır]',
             '[kk]':'[kapı kapanır]',
             '8kk]':'[kapı kapanır]',
             '[kk9':'[kapı kapanır]',
             '8kk9':'[kapı kapanır]',
             '[kv]':'[kapı vurulur]',
             '8kv]':'[kapı vurulur]',
             '[kv9':'[kapı vurulur]',
             '8kv9':'[kapı vurulur]',
             '[ai]':'[adam inler]',
             '8ai]':'[adam inler]',
             '[ai9':'[adam inler]',
             '8ai9':'[adam inler]',
             '[ss]':'[silah sesi]',
             '8ss]':'[silah sesi]',
             '[ss9':'[silah sesi]',
             '8ss9':'[silah sesi]',
             '[ssl]':'[silah sesleri]',
             '8ssl]':'[silah sesleri]',
             '[ssl9':'[silah sesleri]',
             '8ssl9':'[silah sesleri]',
             '[as]':'[arama sonlanır]',
             '8as]':'[arama sonlanır]',
             '[as9':'[arama sonlanır]',
             '8as9':'[arama sonlanır]',
             '[ge]':'[gerilim efekti]',
             '8ge]':'[gerilim efekti]',
             '[ge9':'[gerilim efekti]',
             '8ge9':'[gerilim efekti]',
             '[at]':'[arama tonu]',
             '8at]':'[arama tonu]',
             '[at9':'[arama tonu]',
             '8at9':'[arama tonu]',
             '[ms]':'[mesaj sesi]',
             '8ms]':'[mesaj sesi]',
             '[ms9':'[mesaj sesi]',
             '8ms9':'[mesaj sesi]'}

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

#print the abbrevation list
if args.list:
	for key in abbr_list:
		print('{} --> {}'.format(key, abbr_list[key]))

#open the input file and replace the items
try:
	if args.input:
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
if args.input:
	old_name = os.getcwd() + '/' + args.input
	tokens = args.input.rsplit('.', 1)
	new_name = os.getcwd() + '/' + tokens[0] + '-old.' + tokens[1]
	os.rename(old_name, new_name)

#dump the buffer into a file
try:
	if args.input:
		with open(args.input, 'w') as output:
			output.writelines(buffer)
			print("Items have been replaced in {}.".format(args.input))
except:
	sys.exit('Cannot write to {}.'.format(args.input))
