// Usage: node snip.mjs Class.method [maxLines]  -> prints prettified method source (from shipped bundle)
import fs from 'fs';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
import * as prettier from 'prettier';
const src = fs.readFileSync('js/hoisted.js','utf8');
const ast = acorn.parse(src,{ecmaVersion:'latest',sourceType:'module'});
const targets = process.argv.slice(2).filter(a=>!/^\d+$/.test(a));
const max = +(process.argv.slice(2).find(a=>/^\d+$/.test(a))||60);
const found={};
walk.full(ast,(n)=>{
  if(n.start<532149) return;
  if(n.type==='ClassDeclaration'||n.type==='ClassExpression'){
    const cn=n.id?n.id.name:'';
    for(const m of n.body.body){ const k=m.key&&(m.key.name||m.key.value); const id=cn+'.'+k; if(targets.includes(id)&&!found[id]) found[id]={s:m.start,e:m.end}; }
    if(targets.includes(cn)&&!found[cn]) found[cn]={s:n.start,e:n.end};
  }
  if(n.type==='FunctionDeclaration'&&targets.includes(n.id.name)&&!found[n.id.name]) found[n.id.name]={s:n.start,e:n.end};
});
for(const t of targets){ const f=found[t]; if(!f){console.log('### '+t+' NOT FOUND');continue;}
  let code=src.slice(f.s,f.e); let pretty;
  try{ pretty=await prettier.format('class __X{'+code+'}',{parser:'babel',printWidth:100}); pretty=pretty.split('\n').slice(1,-2).map(l=>l.replace(/^  /,'')).join('\n'); }catch(e){ try{pretty=await prettier.format(code,{parser:'babel',printWidth:100});}catch(e2){pretty=code;} }
  const lines=pretty.split('\n');
  console.log(`### ${t}  (bytes ${f.s}-${f.e}, ${lines.length} lines)`);
  console.log(lines.slice(0,max).join('\n')+(lines.length>max?`\n// ... ${lines.length-max} more lines`:''));
}
