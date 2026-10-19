#!/usr/bin/env python3
"""Auto-extract driver facts from a module: DOM hooks, SplitType, easing, ranges, Ufx meshes, uniforms, classes toggled."""
import re, sys, collections

def facts(mod):
    s = open(f'/home/sprite/lusion/modules/{mod}.js').read()
    out = collections.OrderedDict()
    out['DOM hooks'] = sorted(set(re.findall(r'querySelector(?:All)?\("([^"]+)"\)|getElementById\("([^"]+)"\)', s)), key=str)
    out['DOM hooks'] = sorted({a or ('#' + b) for a, b in out['DOM hooks']})
    out['SplitType'] = sorted(set(re.findall(r'new SplitType\([^,]+,\s*\{\s*types:\s*"([^"]+)"', s)))
    out['Easings'] = [f'{k} x{v}' for k, v in collections.Counter(re.findall(r'ease\.([a-zA-Z]+)', s)).most_common()]
    out['Scroll ranges'] = sorted(set(re.findall(r'getDomRange\(([^)]+)\)', s)))[:8]
    out['WebGL objects'] = [f'{k} x{v}' for k, v in collections.Counter(re.findall(r'new (UfxMesh|UfxTextMesh|Mesh|InstancedMesh|Points|ShaderMaterial|RawShaderMaterial|VideoTexture|WebGLRenderTarget|PerspectiveCamera|OrthographicCamera|Scene)\(', s)).most_common()]
    out['Uniforms'] = sorted(set(re.findall(r'\b(u_[A-Za-z0-9_]+)\s*:', s)))[:24]
    out['Classes toggled'] = sorted(set(re.findall(r'classList\.(?:add|remove|toggle)\("([^"]+)"', s)))
    out['Audio'] = sorted(set(re.findall(r'(?:audios?|sound)[A-Za-z]*\.(?:play|stop)\("([^"]+)"', s)))[:10]
    sample = re.findall(r'math\.fit\([^;]{0,90}?ease\.[a-zA-Z]+\)', s)[:3]
    out['Motion samples'] = sample
    return {k: v for k, v in out.items() if v}

if __name__ == '__main__':
    for m in sys.argv[1:]:
        print('==', m)
        for k, v in facts(m).items():
            print(f'  {k}: {"; ".join(v)[:400]}')
