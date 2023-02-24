#!/usr/bin/env python3

import argparse
import csv
import srt

from datetime import timedelta

parser = argparse.ArgumentParser(description="Convert REAPER generated regions .csv file to srt, filled with input text")
parser.add_argument("csv", help="the .csv file containing REAPER regions")
parser.add_argument("--script", help="the text file containing script lines. When not provided, script lines will be blank")
args = parser.parse_args()

def read_text(path):
    with open(path, "r") as buf:
        result = buf.readlines()
    return result

reaper_timings = csv.reader(read_text(args.csv), skipinitialspace=True)

script_lines = []
if(args.script):
    script_lines = read_text(args.script)

all_subs = []
for row in reaper_timings:
    if(row[0] == "#"):
        continue

    if(script_lines):
        text=script_lines.pop(0)
    else:
        text="{}"

    new_sub = srt.Subtitle(
        index=len(all_subs),
        start=timedelta(seconds=float(row[2])),
        end=timedelta(seconds=float(row[3])),
        content=text
    )

    all_subs.append(new_sub)

print(srt.compose(all_subs))
