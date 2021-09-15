#!/usr/bin/env python3

import argparse, srt, docx

#cli arguments
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='FILENAME',
        help='name of input file (REQUIRED)', required=True)
args = parser.parse_args()

tokens = args.input.rsplit('.', 1)

with open(args.input, 'r') as script:
    content = script.readlines()

    #parse the subtitle file
    content_string = ''.join(content)
    subtitles_generator = srt.parse(content_string)
    subtitles = list(subtitles_generator)

    #recompose the original subtitle
    copy = srt.compose(subtitles)

    buffer = []
    for line in subtitles:
        if 'an8' in line.content:
            buffer.append(line)
   
    #remove an8
    export_cont = []
    for line in content:
        if 'an8' in line:
            new_line = line.replace('{\\an8}', '')
            export_cont.append(new_line)
        else:
            export_cont.append(line)

#content for docx
docx_content = []
for line in buffer:
    index = line.index
    timecode = srt.timedelta_to_srt_timestamp(line.start) + ' --> ' + srt.timedelta_to_srt_timestamp(line.end)
    content = line.content
    docx_content.append(index)
    docx_content.append(timecode)
    docx_content.append(content)

#yukarı atılacaklar
mydoc = docx.Document()
for line in docx_content:
    mydoc.add_paragraph(str(line))
output_file = tokens[0] + ' - yukarı atılacaklar.docx'
mydoc.save(output_file)

#raised subtitles
raised_subs = tokens[0] + ' - raised subtitles.srt'
with open(raised_subs, 'w') as raised:
    raised.writelines(copy)

#for export
for_export = tokens[0] + ' - for export.srt'
with open(for_export, 'w') as export:
    export.writelines(export_cont)
#save_file = srt.compose(buffer)
#buffer_file = tokens[0] + '-an8-only.srt'
#with open(buffer_file, 'w') as new_srt:
#    new_srt.writelines(save_file)
