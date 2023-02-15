#!/usr/bin/python3

import pylrc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("srt", help="the .srt file to translate")
args = parser.parse_args()

with open(args.srt) as buf:
    lrc_string = ''.join(buf.readlines())

srt = pylrc.parse(lrc_string).toSRT()
print(srt)
