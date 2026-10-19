import fs from 'fs';
import * as acorn from 'acorn';
const src = fs.readFileSync('js/hoisted.js','utf8');
const ast = acorn.parse(src,{ecmaVersion:'latest',sourceType:'module'});
const out=[];
for (const n of ast.body){
  let names=[]; let kind=n.type;
  if(n.type==='ClassDeclaration'){names=[n.id.name]; kind='class'+(n.superClass?' extends '+src.slice(n.superClass.start,n.superClass.end):'');}
  else if(n.type==='FunctionDeclaration'){names=[n.id.name]; kind='function('+n.params.map(p=>src.slice(p.start,p.end)).join(',').slice(0,60)+')';}
  else if(n.type==='VariableDeclaration'){for(const d of n.declarations){ if(d.id.type==='Identifier'){ let k=d.init?d.init.type:''; if(d.init&&d.init.type==='ClassExpression') k='class'+(d.init.superClass?' extends '+src.slice(d.init.superClass.start,d.init.superClass.end):''); if(d.init&&d.init.type==='NewExpression') k='new '+src.slice(d.init.callee.start,d.init.callee.end); names.push(d.id.name+' :'+k);} } kind='var';}
  else if(n.type==='ExpressionStatement'){names=[src.slice(n.start,Math.min(n.end,n.start+80)).replace(/\n/g,' ')]; kind='expr';}
  else names=[n.type];
  out.push(`${n.start}\t${n.end-n.start}\t${kind}\t${names.join(' | ')}`);
}
fs.writeFileSync('toplevel.tsv',out.join('\n'));
console.log(out.length);
