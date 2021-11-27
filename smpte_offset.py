#!/usr/bin/env python3
import argparse, re
from timecode import Timecode

#cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='Name of input file (REQUIRED)', required=True)
parser.add_argument('-s', '--shift', metavar='TIME', 
        help='Amount to shift by in seconds, default is 20. It can be negative')
parser.add_argument('-f',  '--fps', metavar='FPS')
parser.add_argument('--forward', action='store_true', default=False)
args = parser.parse_args()

add = True if args.forward is True else False

def parse_timecodes(lines):
    start_list = list()
    end_list = list()
    for line in lines:
        tc_regex = re.findall('\d\d:\d\d:\d\d:\d\d', line)
        if len(tc_regex) == 0:
            pass
        else:
            start_list.append(tc_regex[0])
            end_list.append(tc_regex[-1])
    return start_list, end_list

def offset_timecodes(timecodes, shift_amount):
    shifted_tc = list()
    for timecode in timecodes:
        if timecode == '01:00:00:00':
            tc_event = Timecode(args.fps, '01:00:00:01')
        else:
            tc_event = Timecode(args.fps, timecode)
        offset = Timecode(args.fps, '00:00:00:00')
        new_tc = tc_event - shift_amount + offset
        shifted_tc.append(new_tc)
    return shifted_tc

def swap_timecodes(st_old_tc, st_new_tc, en_old_tc, en_new_tc, content):
    swap_index = {}
    for i, x, j, k in zip(st_old_tc, st_new_tc, en_old_tc, en_new_tc):
        swap_index[i] = x
        swap_index[j] = k
    
    for number, line in enumerate(content):
        for key in swap_index:
            if key in line:
                line = line.replace(str(key), str(swap_index[key]))
                content[number] = line
            else:
                pass
    return content

def main():
    with open(args.input, 'r') as f:
        content = f.readlines()
        orig_tc = parse_timecodes(content)
        shift_amt = Timecode(args.fps, args.shift)
        shifted_start = offset_timecodes(orig_tc[0], shift_amt)
        shifted_end = offset_timecodes(orig_tc[-1], shift_amt)
        shifted_file = swap_timecodes(orig_tc[0], shifted_start, orig_tc[-1], shifted_end, content)

    tokens = args.input.rsplit('.', 1)
    new_file = tokens[0] + '-shifted.' + tokens[1]
    with open(new_file, 'w') as output:
        output.writelines(shifted_file)

main()
