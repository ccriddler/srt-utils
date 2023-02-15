#!/usr/bin/python3

import argparse
import srt
import os

parser = argparse.ArgumentParser(description="Fill an .srt with given text lines")
parser.add_argument("srt", help="the .srt file containing the timings to be overwritten")
parser.add_argument("text", help="the text file containing script lines. Must match srt line count")
args = parser.parse_args()

def read_text(path):
    with open(path, "r") as buf:
        result = buf.read()
    return result

def read_text_lines(path):
    with open(path, "r") as buf:
        result = buf.readlines()
    return result

def write_text(path, data):
    print("Writing text -> {}".format(path))
    with open(path, "w") as buf:
        buf.write(data)

subs = srt.parse(read_text(args.srt))
text_lines = read_text(args.text).split("\n")

fill_subs = []
for sub in subs:
    text=text_lines.pop(0)

    new_sub = srt.Subtitle(
        index=len(fill_subs),
        start=sub.start,
        end=sub.end,
        content=text
    )

    fill_subs.append(new_sub)

print(srt.compose(fill_subs))

#name, ext = os.path.splitext(args.srt)
#outname = name+"_"+ext
#write_text(outname, srt.compose(fill_subs))
