#!/usr/bin/env python3
"""Convert fetched Notion block JSON into clean GitHub Markdown for the lusion-decoded repo."""
import json, os, re, sys, hashlib, subprocess, urllib.request, posixpath

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/sprite/lusion-decoded'
CACHE = os.path.join(HERE, 'img')
os.makedirs(CACHE, exist_ok=True)
SITE = 'https://shifatmasud.notion.site/'
MAIN_ID = '3fd48559569d81dd80b4c7407caf27cc'
MAIN_URL = SITE + MAIN_ID
REPO_URL = 'https://github.com/shifatmasud/lusion-decoded'

# name, notion id, repo path (relative to repo root), asset dir
PAGES = [
    ('c01', '3fd48559569d8124ab68d56b80867ef5', 'handbook/01_stack_and_bundle_anatomy.md', '01'),
    ('c02', '3fd48559569d811e94b1cd6359ec9594', 'handbook/02_boot_sequence_and_main_loop.md', '02'),
    ('c03', '3fd48559569d810bb1f9d6e4e072ee8a', 'handbook/03_rendering_engine_and_post_processing.md', '03'),
    ('c04', '3fd48559569d816eb890f8d968ec1fae', 'handbook/04_dom_to_webgl_sync_ufx.md', '04'),
    ('c05', '3fd48559569d816d8a50c22e35b3ce7b', 'handbook/05_scroll_input_and_motion.md', '05'),
    ('c06', '3fd48559569d817280f5e9676aca01db', 'handbook/06_routing_pages_and_sections.md', '06'),
    ('c07', '3fd48559569d81549fa5ff6c49d305fb', 'handbook/07_effects_and_scenes.md', '07'),
    ('c08', '3fd48559569d81daa932c9558ddf8b9a', 'handbook/08_shaders_and_post_processing_pipeline.md', '08'),
    ('c09', '3fd48559569d81b397c9f275470e9b7a', 'handbook/09_assets_and_loading.md', '09'),
    ('c10', '3fd48559569d81289d5ff6769e1f1d55', 'handbook/10_css_layout_and_dom_state.md', '10'),
    ('c11', '3fd48559569d81c1b174e921471bcaf6', 'handbook/11_system_architecture_plan_and_conceptual_model.md', '11'),
    ('c12', '3fd48559569d8160ba22f0f918a83fec', 'handbook/12_teardown_guide.md', '12'),
    ('c13', '3fd48559569d81709a8ecf7dc5c65d23', 'handbook/13_class_and_method_inventory.md', '13'),
    ('c14', '3fe48559569d81a98b50c232287e3463', 'handbook/14_special_cursor_fluid_trail_screenpaint.md', '14'),
    ('c15', '3fe48559569d81069c7ff759ffc2bb9a', 'handbook/15_screenshot_atlas/15_0_overview.md', '15'),
    ('c151', '3fe48559569d817bb6bfdc1a46b69d91', 'handbook/15_screenshot_atlas/15_1_home.md', '15'),
    ('c152', '3fe48559569d810a98a2ee47788dcbb5', 'handbook/15_screenshot_atlas/15_2_about.md', '15'),
    ('c153', '3fe48559569d815884e7f0f2ddd6a104', 'handbook/15_screenshot_atlas/15_3_projects.md', '15'),
    ('c154', '3fe48559569d816381a1cb2ae37987bd', 'handbook/15_screenshot_atlas/15_4_project_template.md', '15'),
    ('c155', '3fe48559569d817a9a25eb56b9252c63', 'handbook/15_screenshot_atlas/15_5_gallery.md', '15'),
]
ID2PATH = {p[1]: p[2] for p in PAGES}
ID2PATH[MAIN_ID] = 'README.md'

LANG = {'plain text': '', 'mermaid': 'mermaid', 'javascript': 'javascript', 'typescript': 'typescript',
        'glsl': 'glsl', 'css': 'css', 'html': 'html', 'bash': 'bash', 'shell': 'bash', 'json': 'json',
        'python': 'python', 'markdown': 'markdown', 'yaml': 'yaml', 'xml': 'xml', 'c': 'c', 'c++': 'cpp',
        'java': 'java', 'diff': 'diff', 'sql': 'sql', 'jsx': 'jsx', 'tsx': 'tsx'}

log = {'images': [], 'failed': [], 'unknown_types': set(), 'dropped': [], 'files': []}

def nid(s):
    return s.replace('-', '')

def plain(rt):
    if not rt: return ''
    out = ''
    for seg in rt:
        t = seg[0]
        if t == '\u2023' and len(seg) > 1:
            for d in seg[1]:
                if d[0] == 'p': t = TITLES.get(nid(d[1]), 'page')
        out += t
    return out

TITLES = {}

def map_link(url, cur):
    m = re.search(r'(?:notion\.(?:so|site)|app\.notion\.com)?/(?:p/)?(?:[\w-]*-)?([0-9a-f]{32})', url)
    if url.startswith('/') or ('notion.' in url and m):
        if m:
            pid = m.group(1)
            if pid in ID2PATH:
                return posixpath.relpath(ID2PATH[pid], posixpath.dirname(cur))
            return SITE + pid
    return url

def esc_text(t, in_table):
    t = t.replace('\\', '\\\\').replace('<', '&lt;').replace('*', '\\*')
    t = t.replace('_', '\\_')
    t = t.replace('[', '\\[').replace(']', '\\]')
    if in_table: t = t.replace('|', '\\|')
    return t

def code_span(t, in_table):
    if in_table: t = t.replace('|', '\\|')
    n = 1
    while '`' * n in t: n += 1
    tick = '`' * n
    pad = ' ' if t.startswith('`') or t.endswith('`') else ''
    return f'{tick}{pad}{t}{pad}{tick}'

def rich(rt, cur, in_table=False):
    if not rt: return ''
    parts = []  # (text, bold, italic, strike)
    for seg in rt:
        t = seg[0]
        decos = seg[1] if len(seg) > 1 else []
        d = {x[0]: (x[1] if len(x) > 1 else True) for x in decos}
        if 'p' in d:
            pid = nid(d['p'])
            title = TITLES.get(pid, 'linked page')
            target = map_link('/' + pid, cur)
            s = f'[{esc_text(title, in_table)}]({target})'
        elif 'e' in d:
            s = f'${d["e"]}$'
        elif 'u' in d or 'd' in d:
            s = esc_text(t, in_table)
        else:
            if '\n' in t and not in_table:
                pass
            if 'c' in d:
                lines = t.split('\n')
                s = ('<br>' if in_table else '  \n').join(code_span(x, in_table) if x else '' for x in lines)
            else:
                s = esc_text(t, in_table)
                s = s.replace('\n', '<br>' if in_table else '  \n')
            if 'a' in d:
                url = map_link(d['a'], cur)
                s = f'[{s}]({url})'
        parts.append([s, 'b' in d, 'i' in d, 's' in d])
    # merge runs with same flags
    merged = []
    for p in parts:
        if merged and merged[-1][1:] == p[1:]:
            merged[-1][0] += p[0]
        else:
            merged.append(list(p))
    out = ''
    for s, b, i, st in merged:
        mk = ('**' if b else '') + ('*' if i else '') + ('~~' if st else '')
        if mk and s.strip():
            lead = s[:len(s) - len(s.lstrip())]
            trail = s[len(s.rstrip()):]
            s = lead + mk + s.strip() + mk[::-1] + trail
        out += s
    return out

class Conv:
    def __init__(self, name, pid, path, adir):
        d = json.load(open(os.path.join(HERE, 'raw', name + '.json')))
        self.b = d['blocks']; self.root = d['root']
        self.cur = path; self.adir = adir; self.name = name
        self.first = True

    def children(self, bid):
        return [c for c in (self.b[bid].get('content') or []) if c in self.b]

    def render_children(self, bid):
        out = []
        prev = None
        num = 0
        for c in self.children(bid):
            v = self.b[c]
            t = v.get('type')
            if t == 'numbered_list':
                num = num + 1 if prev == 'numbered_list' else 1
            md = self.block(c, num)
            if md is None:
                continue
            listy = ('bulleted_list', 'numbered_list', 'to_do', 'page')
            if out:
                if t in listy and prev in listy and t == prev:
                    out.append('\n')
                else:
                    out.append('\n\n')
            out.append(md)
            prev = t
        return ''.join(out)

    def indent(self, text, n):
        pad = ' ' * n
        return '\n'.join((pad + l) if l.strip() else l for l in text.split('\n'))

    def block(self, bid, num=1):
        v = self.b[bid]; t = v.get('type'); p = v.get('properties') or {}; f = v.get('format') or {}
        title = p.get('title')
        cur = self.cur
        if t == 'text':
            txt = plain(title)
            if txt.strip().startswith('Companion repo on GitHub'):
                log['dropped'].append((self.name, txt[:80])); return None
            s = rich(title, cur)
            kids = self.render_children(bid)
            if kids: s += '\n\n' + self.indent(kids, 4) if False else ('\n\n' + kids)
            return s if s.strip() else None
        if t in ('header', 'sub_header', 'sub_sub_header'):
            lvl = {'header': '##', 'sub_header': '##', 'sub_sub_header': '###'}[t]
            s = f'{lvl} {rich(title, cur)}'
            kids = self.render_children(bid)
            return s + ('\n\n' + kids if kids else '')
        if t in ('bulleted_list', 'numbered_list', 'to_do'):
            if t == 'bulleted_list': mark = '- '
            elif t == 'numbered_list': mark = f'{num}. '
            else:
                chk = plain(p.get('checked')) == 'Yes'
                mark = '- [x] ' if chk else '- [ ] '
            s = mark + rich(title, cur)
            kids = self.render_children(bid)
            if kids: s += '\n\n' + self.indent(kids, len(mark) if t != 'to_do' else 2)
            return s
        if t == 'quote':
            s = rich(title, cur)
            kids = self.render_children(bid)
            if kids: s += '\n\n' + kids
            return '\n'.join('> ' + l if l else '>' for l in s.split('\n'))
        if t == 'callout':
            icon = f.get('page_icon') or ''
            if icon.startswith('http') or icon.startswith('/'): icon = ''
            s = rich(title, cur) if title else ''
            kids = self.render_children(bid)
            body = '\n\n'.join(x for x in [s, kids] if x.strip())
            if icon:
                body = icon + ' ' + body
            return '\n'.join('> ' + l if l.strip() else '>' for l in body.split('\n'))
        if t == 'code':
            code = ''.join(seg[0] for seg in (title or []))
            lang = plain(p.get('language')).strip().lower()
            lang = LANG.get(lang, lang.replace(' ', ''))
            n = 3
            while '`' * n in code: n += 1
            fence = '`' * n
            s = f'{fence}{lang}\n{code.rstrip(chr(10))}\n{fence}'
            cap = p.get('caption')
            if cap and plain(cap).strip(): s += '\n\n*' + rich(cap, cur).strip() + '*'
            return s
        if t == 'divider':
            return '---'
        if t == 'image':
            return self.image(bid, v)
        if t == 'file' or t == 'pdf':
            src = plain(p.get('source'))
            nm = plain(p.get('title')) or src.split(':')[-1]
            log['files'].append((self.name, nm))
            if nm.endswith('.zip'):
                return f'The study archive is on the [Notion main page]({MAIN_URL}); it is not copied into this repo.'
            if 'class_inventory' in nm:
                rel = posixpath.relpath('analysis/class_inventory.txt', posixpath.dirname(cur))
                return f'Download: [{nm}]({rel}) (in this repo as `analysis/class_inventory.txt`)'
            return f'Attachment on the Notion page: {nm} ([open the page]({SITE + nid(self.root)}))'
        if t == 'page':
            pid = nid(bid)
            ttl = plain(title)
            target = map_link('/' + pid, cur)
            return f'- [{esc_text(ttl, False)}]({target})'
        if t == 'alias':
            pid = nid(f.get('alias_pointer', {}).get('id', ''))
            return f'- [{esc_text(TITLES.get(pid, "linked page"), False)}]({map_link("/" + pid, cur)})'
        if t == 'table':
            return self.table(bid, v)
        if t == 'toggle':
            kids = self.render_children(bid)
            return f'<details>\n<summary>{rich(title, cur)}</summary>\n\n{kids}\n\n</details>'
        if t == 'equation':
            return f'$$\n{plain(title)}\n$$'
        if t in ('bookmark', 'embed', 'video'):
            src = plain(p.get('source')) or plain(p.get('link'))
            return f'[{src}]({src})'
        if t in ('column_list', 'column'):
            return self.render_children(bid) or None
        if t == 'table_of_contents':
            return None
        log['unknown_types'].add(t)
        s = rich(title, cur) if title else ''
        return s or None

    def table(self, bid, v):
        f = v.get('format') or {}
        cols = f.get('table_block_column_order') or []
        hdr = f.get('table_block_column_header', False)
        rows = []
        for r in self.children(bid):
            rp = self.b[r].get('properties') or {}
            rows.append([rich(rp.get(c), self.cur, True).strip() or ' ' for c in cols])
        if not rows: return None
        if not hdr:
            head = [' '] * len(cols)
            body = rows
        else:
            head, body = rows[0], rows[1:]
        lines = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(cols)) + '|']
        for r in body:
            lines.append('| ' + ' | '.join(r) + ' |')
        return '\n'.join(lines)

    def image(self, bid, v):
        p = v.get('properties') or {}
        src = plain(p.get('source'))
        cap_rt = p.get('caption')
        cap_plain = plain(cap_rt).strip()
        rel = fetch_image(bid, v, src, self.adir, self.name)
        alt = re.sub(r'\s+', ' ', cap_plain).replace('[', '(').replace(']', ')') or os.path.basename(src)
        if rel is None:
            log['failed'].append((self.name, src))
            return f'*Image not available here: see it on the [Notion page]({SITE + nid(self.root)}). {rich(cap_rt, self.cur)}*'
        relp = posixpath.relpath(rel, posixpath.dirname(self.cur))
        s = f'![{alt}]({relp})'
        if cap_plain:
            s += '\n\n*' + rich(cap_rt, self.cur).strip() + '*'
        return s

    def render(self, ttl):
        head = (f'> **Read in Notion:** [{ttl}]({SITE + nid(self.root)}) · Part of '
                f'[Lusion.co Decoded: Frontend Handbook]({MAIN_URL}) · [Repo home]({REPO_URL})')
        body = self.render_children(self.root)
        body = re.sub(r'\n{3,}', '\n\n', body)
        return f'{head}\n\n# {ttl}\n\n{body.strip()}\n'

# ---------- images ----------
EXISTING = {}
def index_existing():
    base = os.path.join(REPO, 'handbook', 'assets')
    for dp, _, fs in os.walk(base):
        for fn in fs:
            fp = os.path.join(dp, fn)
            EXISTING.setdefault(hashlib.md5(open(fp, 'rb').read()).hexdigest(), []).append(os.path.relpath(fp, REPO))

SPACE = None
def signed_url(src, bid, space):
    body = json.dumps({'urls': [{'url': src, 'permissionRecord': {'table': 'block', 'id': bid, 'spaceId': space}}]}).encode()
    req = urllib.request.Request(SITE + 'api/v3/getSignedFileUrls', data=body, headers={'content-type': 'application/json', 'user-agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(req, timeout=60))['signedUrls'][0]

USED = {}
def fetch_image(bid, v, src, adir, page):
    fname = src.split(':')[-1] if src.startswith('attachment:') else os.path.basename(src.split('?')[0])
    fname = re.sub(r'[^\w.\-]', '_', fname)
    cpath = os.path.join(CACHE, nid(bid) + '_' + fname)
    if not os.path.exists(cpath) or os.path.getsize(cpath) == 0:
        try:
            url = signed_url(src, bid, v.get('space_id')) if src.startswith('attachment:') else src
            r = subprocess.run(['curl', '-sfL', '--retry', '3', '-o', cpath, url], capture_output=True)
            if r.returncode != 0 or not os.path.exists(cpath) or os.path.getsize(cpath) == 0:
                raise RuntimeError('curl %d' % r.returncode)
        except Exception as e:
            print('IMG FAIL', page, src, e, file=sys.stderr)
            if os.path.exists(cpath): os.remove(cpath)
            return None
    h = hashlib.md5(open(cpath, 'rb').read()).hexdigest()
    if h in EXISTING:
        # prefer one in the same chapter dir
        cands = EXISTING[h]
        pick = next((c for c in cands if f'/assets/{adir}/' in c), cands[0])
        log['images'].append((page, fname, pick, 'reused'))
        USED[pick] = h
        return pick
    target = f'handbook/assets/{adir}/{fname}'
    tp = os.path.join(REPO, target)
    if os.path.exists(tp) and hashlib.md5(open(tp, 'rb').read()).hexdigest() != h:
        stem, ext = os.path.splitext(fname)
        target = f'handbook/assets/{adir}/{stem}_notion{ext}'
        tp = os.path.join(REPO, target)
    os.makedirs(os.path.dirname(tp), exist_ok=True)
    open(tp, 'wb').write(open(cpath, 'rb').read())
    EXISTING.setdefault(h, []).append(target)
    USED[target] = h
    log['images'].append((page, fname, target, 'new'))
    return target

def main():
    index_existing()
    # titles
    for nm, pid, path, adir in PAGES + [('main', MAIN_ID, 'README.md', '')]:
        d = json.load(open(os.path.join(HERE, 'raw', nm + '.json')))
        for k, v in d['blocks'].items():
            if v.get('type') == 'page':
                TITLES[nid(k)] = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain((v.get('properties') or {}).get('title')))
    out_titles = {}
    for nm, pid, path, adir in PAGES:
        c = Conv(nm, pid, path, adir)
        ttl = TITLES[pid]
        md = c.render(ttl)
        open(os.path.join(REPO, path), 'w').write(md)
        out_titles[path] = ttl
        print('wrote', path, len(md))
    json.dump({'titles': out_titles, 'used': USED,
               'images': log['images'], 'failed': log['failed'], 'unknown': sorted(log['unknown_types']),
               'dropped': log['dropped'], 'files': log['files']},
              open(os.path.join(HERE, 'log.json'), 'w'), indent=1)
    print('failed', log['failed']); print('unknown', log['unknown_types']); print('dropped', len(log['dropped']))

if __name__ == '__main__':
    main()
