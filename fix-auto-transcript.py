#!/usr/bin/env python

import argparse
import re

from fuzzywuzzy import fuzz

"""
(WIP!)
Search, identify, and replace incorrect transcriptions using another text file as reference.
This is mainly helpful for fixing auto-transcribed subtitles, if the original text is available.

This process DOES NOT MODIFY the dest file's line count - it fits the correct text into the formatting 
of the dest file.
"""

parser = argparse.ArgumentParser(description="downloads metadata + script files from HVDB")
parser.add_argument("src", help="source of 'good' text, to be substitute into dest")
parser.add_argument("dest", help="source of 'bad' text, whose line count must be unmodified")
args = parser.parse_args()

frag_delim="、|？|　|\?"
junk_sub="ｗ|。"
RATIO_OK=80

def load_text(path):
    with open(path, "r") as f:
        data = f.readlines()
    return data

def clean_line(line):
    return re.sub(frag_delim+"|"+junk_sub, ' ', line).strip()

def find_best_line(search, lines):
    ratios = [fuzz.ratio(search, clean_line(line)) for line in lines]

    best_ratio = max(ratios)
    best_ratio_idx = ratios.index(best_ratio)

    return (best_ratio, best_ratio_idx, clean_line(lines[best_ratio_idx]))

def find_best_lines(lines_src, lines_dest):
    matches = {}
    for idx, src in enumerate(lines_src):
        src = clean_line(src)

        best = find_best_line(src, lines_dest)

        if(best[0] < RATIO_OK):
            continue

        # Got a hit!
        matches[idx] = best
        print("best match @ {} : {} = '{}' [{}%] @ {} ".format(idx, src, best[2], best[0], best[1]))
    return matches

txt_src = load_text(args.src)
txt_dest = load_text(args.dest)

full_ratio = fuzz.ratio('\n'.join(txt_src), '\n'.join(txt_dest))

print("fulltext similarity = {}".format(full_ratio))
matches = find_best_lines(txt_src, txt_dest)
