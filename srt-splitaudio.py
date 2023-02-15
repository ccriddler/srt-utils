#!/usr/bin/python3

import srt
import os
import argparse

parser = argparse.ArgumentParser(description="chop an audio file, using .srt subtitles as timings")
parser.add_argument("srt", help="path to subtitle file containing timings to reference from")
parser.add_argument("audio", help="path to audio to chop")
parser.add_argument("--dry", action="store_true", help="show potential commands without executing")
args = parser.parse_args()

def load_text(path):
    with open(path, "r") as f:
        data = f.read()
    return data

def write_text(path, text):
    with open(path, "w") as f:
        f.write(text)

def get_pot(num):
    pot = 0
    while(num >= 10):
        num /= 10
        pot += 1
    return pot+1

# load
srt_data = load_text(args.srt)
srt_parse = list(srt.parse(srt_data))

# detect output filename format
audio_name, audio_ext = os.path.splitext(args.audio)
chop_pad = get_pot(len(srt_parse))

for idx, sub in enumerate(srt_parse):
    dur = sub.end - sub.start

    chop = "{}_{}{}".format(audio_name, str(idx).zfill(chop_pad), audio_ext)

    cmd = "ffmpeg -ss {} -i '{}' -t {} '{}'".format(
        sub.start,
        args.audio,
        dur,
        chop
    )

    print("execute {}".format(cmd))
    if(not args.dry):
        os.system(cmd)
