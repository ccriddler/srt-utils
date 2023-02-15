#!/usr/bin/python3

import srt
import os
import argparse

parser = argparse.ArgumentParser(description="inject plaintext lines into srt file, overwriting sub content sequentially while maintaining timings")
parser.add_argument("srt", help="path to subtitle file to inject into")
parser.add_argument("text", help="path to text file to read from")
args = parser.parse_args()

def load_text(path):
    with open(path, "r") as f:
        data = f.read()
    return data

# load
srt_data = load_text(args.srt)
srt_parse = list(srt.parse(srt_data))
print("read {} subs from {}".format(len(srt_parse), args.srt))

text_data = load_text(args.text).split("\n")
print("read {} lines from {}".format(len(text_data), args.text))

if(len(text_data) != len(srt_parse)):
    print("srt / plaintext size mismatch!")
    #exit(0)

for idx, sub in enumerate(srt_parse):
    srt_parse[idx].content = text_data[idx]

# compile the new subs into srt data format
srt_output = ""
for sub in srt_parse:
    srt_output += sub.to_srt()

print(srt_output)
