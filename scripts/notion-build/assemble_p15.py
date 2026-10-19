# Expand {{IMG:path|caption}} and {{LEGEND:slug/mode/frame}} in src_15_*.md.
# usage: python3 assemble_p15.py list   -> prints image paths in order
#        python3 assemble_p15.py build  -> writes 15_3_projects.md / 15_4_project_template.md (file-upload ids from p15_uploads.tsv)
import re, json, sys, os
sys.path.insert(0, '.')
SRC = {'src_15_3_projects.md': '15_3_projects.md', 'src_15_4_project_template.md': '15_4_project_template.md'}
URL = {
    4: 'https://app.notion.com/p/3fd48559569d816eb890f8d968ec1fae',
    5: 'https://app.notion.com/p/3fd48559569d816d8a50c22e35b3ce7b',
    6: 'https://app.notion.com/p/3fd48559569d817280f5e9676aca01db',
    8: 'https://app.notion.com/p/3fd48559569d81daa932c9558ddf8b9a',
    10: 'https://app.notion.com/p/3fd48559569d81289d5ff6769e1f1d55',
    14: 'https://app.notion.com/p/3fe48559569d81a98b50c232287e3463',
}
NAMES = {4: '4. DOM to WebGL sync (Ufx)', 5: '5. Scroll, input and motion', 6: '6. Routing, pages and sections', 8: '8. Shaders and the post-processing pipeline', 10: '10. CSS, layout and DOM state', 14: '14. ScreenPaint cursor trail'}
GALLERY = 'https://app.notion.com/p/3fe48559569d817a9a25eb56b9252c63'

def esc(s):
    return str(s).replace('<', '&lt;').replace('>', '&gt;').replace('|', '/')

def legend(key):
    slug, mode, frame = key.split('/')
    L = json.load(open(f'img/{slug}/{mode}/legend.json'))
    rows = L[frame]['rows']
    t = ['<table header-row="true">', '<tr><td>#</td><td>Element</td><td>Text (live, may be mid-animation)</td><td>Type (computed)</td><td>Colour / background</td><td>Box x,y w×h</td></tr>']
    for r in rows:
        t.append(f"<tr><td>{r['n']}</td><td>`{esc(r['sel'])[:80]}`</td><td>{esc(r['text'])[:60]}</td><td>{esc(r['font'])}</td><td>{esc(r['color'])} / {esc(r['bg'])}</td><td>{esc(r['box'])}</td></tr>")
    t.append('</table>')
    return '\n'.join(t)

def related(chs):
    return '**Related chapters:** ' + ', '.join(f'[{NAMES[c]}]({URL[c]})' for c in chs)

def images(text):
    return re.findall(r'\{\{IMG:([^|]+)\|', text)

if sys.argv[1] == 'list':
    for s in SRC:
        for p in images(open(s).read()):
            print(p, os.path.getsize(p))
else:
    up = dict(l.rstrip('\n').split('\t')[:2] for l in open('p15_uploads.tsv') if '\t' in l)
    for s, d in SRC.items():
        t = open(s).read()
        t = re.sub(r'\{\{LEGEND:([^}]+)\}\}', lambda m: legend(m.group(1)), t)
        t = re.sub(r'\{\{IMG:([^|]+)\|([^}]+)\}\}', lambda m: f'![{m.group(2)}](file-upload://{up[m.group(1)]})' if m.group(1) in up else f'*(image missing: {m.group(1)})*', t)
        chs = [4, 5, 6, 8, 10] if '15_3' in s else [4, 5, 6, 8, 10, 14]
        t = t.replace('</callout>\n', '</callout>\n\n' + related(chs) + ('' if '15_3' in s else f'  ·  [15.5 Project pages gallery]({GALLERY})') + '\n', 1)
        for n, u in URL.items():
            t = re.sub(rf'(?<![\[\w])chapter {n}\b(?!\])', f'[chapter {n}]({u})', t)
        open(d, 'w').write(t)
        print(d, len(t))
