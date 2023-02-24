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

    return {
        "best_ratio":best_ratio,
        "best_ratio_idx":best_ratio_idx,
        "dest_text":lines[best_ratio_idx]
    }

# full line replacement search
def find_best_lines(lines_src, lines_dest):
    matches = {}
    last_match = 0
    for idx, src in enumerate(lines_src):
        best = find_best_line(clean_line(src), lines_dest[last_match:])

        if(best["best_ratio"] < RATIO_OK):
            continue

        best["src_text"] = src
        best["best_ratio_idx"] += last_match

        # Got a hit!
        matches[idx] = best
        print("best match @ {} : {} = '{}' [{}%] @ {} ".format(idx, best["src_text"].strip(), best["dest_text"].strip(), best["best_ratio"], best["best_ratio_idx"]))
        last_match = idx

    return matches

def apply_matches(matches, lines_dest):
    for match in matches:
        dest_idx = matches[match]["best_ratio_idx"]
        lines_dest[dest_idx] = matches[match]["src_text"]
    return lines_dest

txt_src = load_text(args.src)
txt_dest = load_text(args.dest)

full_ratio = fuzz.ratio('\n'.join(txt_src), '\n'.join(txt_dest))

print("fulltext similarity = {}".format(full_ratio))
matches = find_best_lines(txt_src, txt_dest)

txt_dest = apply_matches(matches, txt_dest)
full_ratio = fuzz.ratio('\n'.join(txt_src), '\n'.join(txt_dest))
print("full-line replace similarity = {}".format(full_ratio))

# TODO partial line replacements
# multiple lines, when joined together, create a high ratio based on search text
