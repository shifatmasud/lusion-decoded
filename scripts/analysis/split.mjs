// Split the shipped bundle into study modules and extract every GLSL shader string.
import fs from 'fs';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
const src = fs.readFileSync('js/hoisted.js','utf8');
const ast = acorn.parse(src,{ecmaVersion:'latest',sourceType:'module'});
const APP_START = 532149; // end of the bundled three.js r158 core
fs.mkdirSync('modules',{recursive:true});
fs.mkdirSync('shaders',{recursive:true});
// 1) group top-level nodes into modules
let groups=[]; let cur={name:'00_three_r158_core',parts:[]};
const libMarkers=[[564134,'lib_fbjs_normalizeWheel'],[634675,'lib_splittype'],[677071,'lib_vimeo_player'],[830209,'lib_to_querystring_debug_jsonp'],[1106805,'lib_dayjs'],[1206033,'lib_fflate'],[1210273,'lib_three_EXRLoader']];
let idx=1;
function startGroup(n){ if(cur.parts.length) groups.push(cur); cur={name:String(idx++).padStart(3,'0')+'_'+n,parts:[]}; }
for(const n of ast.body){
  if(n.start>=APP_START){
    const lm=libMarkers.find(m=>Math.abs(m[0]-n.start)<200 && !cur.name.endsWith(m[1]));
    let cname=null;
    if(n.type==='ClassDeclaration') cname=n.id.name;
    else if(n.type==='FunctionDeclaration' && /^(QuickLoader|preRun|isEventSupported\$1|normalizeWheel\$2|getMethodName|unzlibSync)$/.test(n.id.name)) cname=n.id.name;
    const libInternal=['Player','TimingSrcConnector','EXRLoader'];
    if(lm && n.start>=lm[0]-200) { startGroup(lm[1]); }
    else if(cname && !libInternal.includes(cname) && !(cur.name.includes('lib_fbjs')&&['isEventSupported$1','normalizeWheel$2'].includes(cname)) && !(cur.name.includes('lib_fflate')&&cname==='unzlibSync')) startGroup(cname);
  }
  cur.parts.push(n);
}
groups.push(cur);
const index=[];
for(const g of groups){
  const s=g.parts[0].start, e=g.parts.at(-1).end;
  fs.writeFileSync(`modules/${g.name}.js`, `// bytes ${s}-${e} of /_astro/hoisted.CUO_IjfL.js\n`+src.slice(s,e));
  index.push(`${g.name}\t${s}\t${e-s}`);
}
fs.writeFileSync('modules/INDEX.tsv',index.join('\n'));
// 2) shaders: every template literal / string that looks like GLSL, inside app range
const sh=[]; const seen=new Set();
walk.fullAncestor(ast,(node,anc)=>{
  if(node.start<APP_START) return;
  let text=null;
  if(node.type==='TemplateLiteral') text=node.quasis.map(q=>q.value.cooked??q.value.raw).join('${...}');
  else if(node.type==='Literal' && typeof node.value==='string') text=node.value;
  if(!text || text.length<60) return;
  if(!/(void\s+main|gl_FragColor|gl_Position|uniform\s+\w+|varying\s+\w+|#include|precision\s+\w+p)/.test(text)) return;
  // name: nearest VariableDeclarator / Property key
  let name='anon';
  for(let i=anc.length-2;i>=0;i--){const a=anc[i];
    if(a.type==='VariableDeclarator'&&a.id.type==='Identifier'){name=a.id.name;break}
    if(a.type==='Property'&&a.key){name=(a.key.name||a.key.value);
      for(let j=i-1;j>=0;j--){ if(anc[j].type==='ClassDeclaration'){name=anc[j].id.name+'.'+name;break} if(anc[j].type==='VariableDeclarator'&&anc[j].id.type==='Identifier'){name=anc[j].id.name+'.'+name;break} }
      break}
    if(a.type==='AssignmentExpression'){name=src.slice(a.left.start,a.left.end).slice(0,40);
      for(let j=i-1;j>=0;j--){ if(anc[j].type==='ClassDeclaration'){name=anc[j].id.name+'.'+name;break} }
      break}
  }
  if(seen.has(node.start)) return; seen.add(node.start);
  sh.push({name,start:node.start,text});
});
const used={};
const shIndex=[];
for(const s of sh){ let n=s.name.replace(/[^\w.$-]/g,'_').replace(/\$/g,'S'); used[n]=(used[n]||0)+1; if(used[n]>1) n+='_'+used[n];
  const kind=/gl_Position/.test(s.text)?'vert':(/gl_FragColor|gl_FragData|pc_fragColor|out\s+vec4|discard/.test(s.text)?'frag':'chunk');
  fs.writeFileSync(`shaders/${n}.${kind}.glsl`, `// extracted from /_astro/hoisted.CUO_IjfL.js at byte ${s.start}\n`+s.text);
  const uniforms=[...s.text.matchAll(/uniform\s+(\w+)\s+(\w+)/g)].map(m=>m[2]);
  shIndex.push(`${n}.${kind}.glsl\t${s.start}\t${s.text.length}\t${uniforms.join(',')}`);
}
fs.writeFileSync('shaders/INDEX.tsv',shIndex.join('\n'));
console.log('modules',groups.length,'shaders',sh.length);
