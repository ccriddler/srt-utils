#!/usr/bin/python3

import argparse
import srt
import os

parser = argparse.ArgumentParser(description="Write srt lines to text file")
parser.add_argument("srt", help="the .srt file to convert")
args = parser.parse_args()

def read_text(path):
    with open(path, "r") as buf:
        result = buf.read()
    return result

def write_text(path, data):
    print("Writing text -> {}".format(path))
    with open(path, "w") as buf:
        buf.write(data)

subs = srt.parse(read_text(args.srt))

subs_text = [sub.content for sub in subs]

print("\n".join(subs_text))
#path, ext = os.path.splitext(args.srt)
#outname = path + ext.replace(".srt", ".txt")
#write_text(outname, "\n".join(subs_text))
