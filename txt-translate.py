#!/usr/bin/env python3

import argparse
import deepl
import googletrans
import srt
import time
import os

parser = argparse.ArgumentParser(description="An auto translator for .txt files utilizing google's translate API")
parser.add_argument("txt", help="the .txt file to translate")
parser.add_argument("--lang-from", default="JA", help="Source language of the .srt file")
parser.add_argument("--lang-to", default="EN-US", help="Dest language of the output .srt file")
parser.add_argument("--delay", default=1, type=int, help="Delay time between translation api requests")
parser.add_argument("--deepl-auth", help="Auth key for your account, if using deepl API (WIP)")
args = parser.parse_args()

translator = googletrans.Translator()
if(args.deepl_auth):
    translator = deepl.Translator(args.deepl_auth)

def read_text(path):
    with open(path, "r") as buf:
        result = buf.readlines()
    return result

def write_text(path, data):
    with open(path, "w") as buf:
        buf.write(data)

lines = read_text(args.txt)

def process_sub(tl, line):
    if(isinstance(tl, googletrans.Translator)):
        return tl.translate(
            text=line,
            dest=args.lang_to,
            src=args.lang_from
        ).text

    if(isinstance(tl, deepl.Translator)):
        return tl.translate_text(
            line,
            target_lang=args.lang_to,
            source_lang=args.lang_from
        ).text
    return ""

print("TRANSLATION BEGIN '{}'".format(args.txt))

trans_lines = []
for idx, line in enumerate(lines):
    trans_lines.append(line)

    print("LINE {}/{}".format(idx, len(lines)))
    print("---")

    print("In -> {}".format(line))
    trans_lines[-1] = process_sub(translator, line)
    print("Out -> {}".format(trans_lines[-1]))

    print("")
    #print("Delay {} sec".format(args.delay))
    time.sleep(args.delay)

path, ext = os.path.splitext(args.txt)
ext = ext.replace(".txt", ".{}.txt".format(args.lang_to))
outname = path + ext

print("Writing translation -> {}".format(outname))
write_text(outname, "".join(trans_lines))
