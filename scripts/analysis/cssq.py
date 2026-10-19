#!/usr/bin/env python3
"""Print condensed CSS rules whose selector contains any of the given ids/classes. usage: cssq.py sel1 [sel2...]"""
import re, sys
css = open('/home/sprite/lusion/handbook/ch15/lusion_pretty.css').read()
# flatten: track @media context
out = []
media = None
i = 0
toks = re.finditer(r'([^{}]+)\{|\}', css)
stack = []
buf_sel = None
pos = 0
for m in re.finditer(r'([^{}]*)\{([^{}]*)\}|(@[^{]+)\{|\}', css):
    if m.group(3):
        stack.append(m.group(3).strip())
    elif m.group(1) is not None:
        sel = ' '.join(m.group(1).split())
        body = ' '.join(m.group(2).split())
        if any(s in sel for s in sys.argv[1:]):
            ctx = stack[-1] if stack else ''
            out.append((ctx + ' | ' if ctx else '') + sel + ' { ' + body + ' }')
    else:
        if stack:
            stack.pop()
print('\n'.join(out))
