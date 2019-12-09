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

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-i', '--input', default=None, required=True,
        help='A input filename.')
    parser.add_argument('-o', '--output', default=None, required=True,
        help='A output filename.')

    args = parser.parse_args()
    return args

args = parse_arguments()

MYDIR = os.path.abspath(os.path.dirname(__file__))
infile = os.path.join(MYDIR, args.input)
outfile = os.path.join(MYDIR, args.output)

lines = file2list(infile)
outlines = []
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
    if line[0]=='#':
        outlines.append(line)
        continue

    # if not content line, invalid
    if line[0]!='-':
        continue

    # (example)
    # - 2019/10/14 争わない「生き方」 自分は自分 人は人 和田秀樹 / マイペース / 肉食系は夜型が似合い、草食系は朝型が似合います……そういう人たちに、夜を任せておけばいいでしょう……肉食系と草食系の棲み分け / 節目というのは争いとは無縁の世界です / 相変わらずとっつきにくい雰囲気を漂わせてしまう……「気さくな人」だとわかってもらえただけで、穏やかな人間関係を保つことができる

    body = line[1:].strip()

    datelen = len('yyyy/mm/dd')
    this_date = body[:datelen]
    body_without_date = body[datelen+1:]

    elements = body_without_date.split('/')
    elements = [x.strip() for x in elements]

    book_header = elements[0]
    outlines.append('- {} {}'.format(this_date, book_header))

    for element in elements[1:]:
        template_line = '    - {} {}'
        emoji_quote  = ':notebook:'
        emoji_mynote = ':speech_balloon:'
        out_emojis = '' 
        if element.startswith('('):
            out_emojis = emoji_mynote
        else:
            out_emojis = emoji_quote
            if element.find('(') != -1:
                out_emojis += emoji_mynote

        outline  = template_line.format(out_emojis, element)
        outlines.append(outline)

outbody = '\n'.join(outlines)

def list2file(filepath, ls):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.writelines(['{:}\n'.format(line) for line in ls] )

list2file(outfile, outlines)
