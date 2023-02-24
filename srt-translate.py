#!/usr/bin/env python3

import argparse
import deepl
import googletrans
import srt
import time
import os

parser = argparse.ArgumentParser(description="An auto translator for .srt files utilizing google's translate API")
parser.add_argument("srt", help="the .srt file to translate")
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
        result = buf.read()
    return result

def write_text(path, data):
    with open(path, "w") as buf:
        buf.write(data)

subs = srt.parse(read_text(args.srt))

def process_sub(tl, sub):
    if(isinstance(tl, googletrans.Translator)):
        return tl.translate(
            text=sub.content,
            dest=args.lang_to,
            src=args.lang_from
        ).text

    if(isinstance(tl, deepl.Translator)):
        return tl.translate_text(
            sub.content,
            target_lang=args.lang_to,
            source_lang=args.lang_from
        ).text
    return ""

print("TRANSLATION BEGIN '{}'".format(args.srt))
trans_subs = []
sublist = list(subs)

for idx, sub in enumerate(sublist):
    trans_subs.append(sub)

    print("LINE {}/{}".format(idx, len(sublist)))
    print("---")

    print("In -> {}".format(sub.content))
    trans_subs[-1].content = process_sub(translator, sub)
    print("Out -> {}".format(trans_subs[-1].content))

    print("")
    #print("Delay {} sec".format(args.delay))
    time.sleep(args.delay)

path, ext = os.path.splitext(args.srt)
ext = ext.replace(".srt", ".{}.srt".format(args.lang_to))
outname = path + ext

print("Writing translation -> {}".format(outname))
write_text(outname, srt.compose(trans_subs))
