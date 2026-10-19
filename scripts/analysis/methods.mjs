// Inventory of every app class: fields, getters, methods with parameter lists and size.
import fs from 'fs';
import * as acorn from 'acorn';
import * as walk from 'acorn-walk';
const src = fs.readFileSync('js/hoisted.js','utf8');
const ast = acorn.parse(src,{ecmaVersion:'latest',sourceType:'module'});
const APP_START=532149;
const rows=[];
const libs=[[634675,648531],[677071,704344],[830209,837036],[1106805,1114174],[1206033,1210273],[766485,779481],[1210273,1230517]];
function inLib(p){return libs.some(([a,b])=>p>=a&&p<b)}
walk.full(ast,(n)=>{
  if((n.type==='ClassDeclaration'||n.type==='ClassExpression') && n.start>=APP_START){
    const name=n.id?n.id.name:'(anon)';
    const sup=n.superClass?src.slice(n.superClass.start,n.superClass.end):'';
    const fields=[],methods=[];
    for(const m of n.body.body){
      const key=m.key? (m.key.name||m.key.value||src.slice(m.key.start,m.key.end)):'?';
      if(m.type==='PropertyDefinition'){ let v=m.value?src.slice(m.value.start,Math.min(m.value.end,m.value.start+50)).replace(/\s+/g,' '):''; fields.push(`${m.static?'static ':''}${key}${v?' = '+v:''}`);}
      else if(m.type==='MethodDefinition'){ const ps=m.value.params.map(p=>src.slice(p.start,p.end).replace(/\s+/g,'')).join(', '); methods.push(`${m.static?'static ':''}${m.kind==='get'?'get ':m.kind==='set'?'set ':''}${key}(${ps})  [${m.end-m.start}b]`);}
    }
    rows.push({name,sup,start:n.start,size:n.end-n.start,lib:inLib(n.start),fields,methods});
  }
});
rows.sort((a,b)=>a.start-b.start);
let out='';
for(const r of rows){ out+=`\n## ${r.name}${r.sup?' extends '+r.sup:''}  (byte ${r.start}, ${r.size} bytes${r.lib?', third-party':''})\n`; if(r.fields.length) out+='fields: '+r.fields.join('; ')+'\n'; for(const m of r.methods) out+='  - '+m+'\n'; }
fs.writeFileSync('class_inventory.txt',out);
console.log(rows.length, rows.filter(r=>!r.lib).length, rows.reduce((s,r)=>s+r.methods.length,0));
