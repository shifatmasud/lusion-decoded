#!/usr/bin/env python3
"""Resolve [[IMG:path|caption]] to Notion file-upload images. usage: finalize.py in.md out.md"""
import re, sys, os
os.chdir('/home/sprite/lusion/handbook/ch15')
sys.path.insert(0, '.')
from content import GLOBALS
up = {}
if os.path.exists('uploads15.tsv'):
    for l in open('uploads15.tsv'):
        p, i = l.strip().split('\t')
        up[p] = i
s = open(sys.argv[1]).read()
s = s.replace('{{GLOBALS}}', GLOBALS).replace('{{SUBPAGES}}', 'One sub-page per site page, in scroll order, follows below. Each has the section-by-section screenshots, callout tables, build specs, exact CSS and DOM outlines.')
pending = []
def rep(m):
    p, cap = m.group(1), m.group(2)
    if p in up:
        return f'![{cap}](file-upload://{up[p]})'
    pending.append(p)
    return f'IMGPENDING {p}'
s = re.sub(r'\[\[IMG:([^|\]]+)\|([^\]]*)\]\]', rep, s)
open(sys.argv[2], 'w').write(s)
print(len(s), 'chars; pending:', pending)
