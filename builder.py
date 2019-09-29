# -*- coding: utf-8 -*-

import os
import re
import sys

def file2list(filepath):
    ret = []
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = [line.rstrip('\n') for line in f.readlines()]
    return ret

def list2file(filepath, ls):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.writelines(['{:}\n'.format(line) for line in ls] )

def file2str(filepath):
    ret = None
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = f.read()
    return ret

def str2file(filepath, s):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.write(s)

def raise_option_error(msg, lineno, line):
    raise RuntimeError('{0} at line {1}, "{2}".'.format(msg, lineno, line))

def append_to_out(appendee_list, appender, use_ignore=False):
    if use_ignore:
        return
    appendee_list.append(appender)

class render:

    # @param re_pattern Must contains () to use grouping for this tags algorithm even if simple query.
    def get_all_taginfo(original_string, re_pattern):
        compiled_obj = re.compile(re_pattern)
        iters = compiled_obj.finditer(original_string)

        all_taginfo = []

        for matchobj in iters:
            matched_string = None
            tags = []

            total = len(matchobj.groups())

            startpos, endpos = matchobj.span()
            matched_string = original_string[startpos:endpos]

            for idx in range(total):
                tag = matchobj.groups()[idx]
                tags.append(tag)

            taginfo = {
                'matched_string' : matched_string,
                'tags'           : tags,        
            }
            all_taginfo.append(taginfo)

        return all_taginfo

    def replace_bold_pattern(original_string):
        pattern = r'\*\*([^\*]+)\*\*'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            tag1 = taginfo['tags'][0]

            before = taginfo['matched_string']
            after = '<strong>{:}</strong>'.format(tag1)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_link_pattern(original_string):
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            title = taginfo['tags'][0]
            url = taginfo['tags'][1]

            before = taginfo['matched_string']
            after = '<a href="{:}">{:}</a>'.format(url, title)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_literal_pattern(original_string):
        pattern = r'`([^`]+)`'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            tag1 = taginfo['tags'][0]

            before = taginfo['matched_string']
            after = '<code>{:}</code>'.format(tag1)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_quote_pattern(original_string):
        pattern = r'『([^』]+)』'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            tag1 = taginfo['tags'][0]

            before = taginfo['matched_string']
            after = '<q>{:}</q>'.format(tag1)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_emphasis_pattern(original_string):
        pattern = r'「([^」]+)」'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            unused = taginfo['tags'][0]

            before = taginfo['matched_string']
            after = '<dummy class="emphasis">{:}</dummy>'.format(before)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_additiondate_pattern(original_string):
        pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2})'

        all_taginfo = render.get_all_taginfo(original_string, pattern)

        replaced_string = original_string

        for taginfo in all_taginfo:
            datestr = taginfo['tags'][0]

            before = taginfo['matched_string']
            after = '<dummy class="additiondate">{:}</dummy>'.format(datestr)

            replaced_string = replaced_string.replace(before, after)

        return replaced_string

    def replace_all(original_string):
        replaced_string = original_string
        replaced_string = render.replace_bold_pattern(replaced_string)
        replaced_string = render.replace_link_pattern(replaced_string)
        replaced_string = render.replace_literal_pattern(replaced_string)
        replaced_string = render.replace_quote_pattern(replaced_string)
        replaced_string = render.replace_emphasis_pattern(replaced_string)
        replaced_string = render.replace_additiondate_pattern(replaced_string)
        return replaced_string

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-i', '--input', default=None, required=True,
        help='A input filename.')
    parser.add_argument('-o', '--output', default=None, required=True,
        help='A output filename.')
    parser.add_argument('-t', '--template', default=None, required=True,
        help='A template filename.')

    args = parser.parse_args()
    return args

args = parse_arguments()

MYDIR = os.path.abspath(os.path.dirname(__file__))
infile = os.path.join(MYDIR, args.input)
outfile = os.path.join(MYDIR, args.output)
templatefile = os.path.join(MYDIR, args.template)

# Fix body contents from source markdown.
# ---------------------------------------

lines = file2list(infile)
outlines = []
outtitle = ''
for i,line in enumerate(lines):
    # blank line
    if len(line)==0:
        continue

    # comment line
    #   ; comment
    #   <!-- comment -->
    #   // comment
    if line[0]==';' or line[0]=='<' or line[0]=='/':
        continue

    # title line
    #   # title
    if line[0]=='#':
        title_candidate = line[1:].strip()
        if len(title_candidate)==0:
            continue
        outtitle = title_candidate
        continue

    # content line
    if line[0]=='-':
        body = line[1:].strip()

        outline = '<li class="entry">{:}</li>'.format(body)

        outline = render.replace_all(outline)

        outlines.append(outline)
        continue

outbody = '\n'.join(outlines)

# Merge fixed body to the template.
# ---------------------------------

template_content = file2str(templatefile)
merged_content = template_content.replace('{{body}}', outbody).replace('{{title}}', outtitle)

# Save.
# -----

str2file(outfile, merged_content)
