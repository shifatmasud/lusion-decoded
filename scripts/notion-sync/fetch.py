#!/usr/bin/env python3
"""Read-only fetch of public Notion pages (block JSON) via notion.site API."""
import json, sys, os, time, urllib.request

BASE = 'https://shifatmasud.notion.site/api/v3/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
os.makedirs(OUT, exist_ok=True)

def post(ep, body):
    for i in range(5):
        try:
            req = urllib.request.Request(BASE + ep, data=json.dumps(body).encode(),
                                         headers={'content-type': 'application/json', 'user-agent': 'Mozilla/5.0'})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            print('retry', ep, e, file=sys.stderr); time.sleep(2 + i * 2)
    raise SystemExit('failed ' + ep)

def dash(i):
    i = i.replace('-', '')
    return f'{i[:8]}-{i[8:12]}-{i[12:16]}-{i[16:20]}-{i[20:]}'

def val(rec):
    v = rec.get('value', {})
    if isinstance(v, dict) and 'value' in v and isinstance(v['value'], dict):
        v = v['value']
    return v

def fetch_page(pid):
    pid = dash(pid)
    blocks = {}
    cursor = {'stack': []}
    n = 0
    while True:
        d = post('loadPageChunk', {'pageId': pid, 'limit': 100, 'cursor': cursor, 'chunkNumber': n, 'verticalColumns': False})
        for k, r in d.get('recordMap', {}).get('block', {}).items():
            v = val(r)
            if v: blocks[k] = v
        cursor = d.get('cursor', {'stack': []})
        n += 1
        if not cursor.get('stack'): break
    # fill missing children (not under child pages)
    for _ in range(10):
        missing = set()
        for k, v in blocks.items():
            if v.get('type') == 'page' and k != pid: continue
            for c in v.get('content', []) or []:
                if c not in blocks: missing.add(c)
        if not missing: break
        ms = list(missing)
        for i in range(0, len(ms), 100):
            d = post('syncRecordValuesMain', {'requests': [{'pointer': {'table': 'block', 'id': x}, 'version': -1} for x in ms[i:i+100]]})
            for k, r in d.get('recordMap', {}).get('block', {}).items():
                v = val(r)
                if v: blocks[k] = v
    return {'root': pid, 'blocks': blocks}

if __name__ == '__main__':
    for a in sys.argv[1:]:
        name, pid = a.split('=')
        d = fetch_page(pid)
        json.dump(d, open(os.path.join(OUT, name + '.json'), 'w'))
        print(name, len(d['blocks']))
