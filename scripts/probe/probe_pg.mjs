import puppeteer from 'puppeteer';
import fs from 'fs';
const [mode='desktop', path='/playground'] = process.argv.slice(2);
const MOB = mode==='mobile'; const W=MOB?390:1440, H=MOB?844:900;
const out=`raw/playground/${mode}${path==='/playground'?'':'_ctrl'}`; fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--mute-audio'] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1, isMobile: MOB, hasTouch: MOB });
if (MOB) await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
const logs=[]; const t0=Date.now(); const L=m=>{const s=((Date.now()-t0)/1000).toFixed(1)+'s '+m; logs.push(s); console.log(s);};
page.on('console', m=>L('console.'+m.type()+': '+m.text().slice(0,300)));
page.on('pageerror', e=>L('PAGEERROR: '+(e.stack||e.message).slice(0,600)));
page.on('requestfailed', r=>L('REQFAIL '+r.url()));
page.on('response', r=>{ if(/playground|tunnel/.test(r.url())) L('RESP '+r.status()+' '+r.url()); });
page.goto('https://lusion.co'+path,{waitUntil:'domcontentloaded',timeout:90000}).catch(e=>L('goto '+e.message));
for (const t of [3000,8000,15000,25000]) { await sleep(t-(Date.now()-t0)); 
  const st = await page.evaluate(()=>{ const p=document.getElementById('preloader'); const ps=p?getComputedStyle(p):null;
    return { url: location.href, title: document.title, htmlCls: document.documentElement.className,
      preloader: ps? {d:ps.display, o:ps.opacity, v:ps.visibility}:null,
      pages: [...document.querySelectorAll('.page')].map(e=>({dp:e.dataset.page, inDoc: document.contains(e), h: Math.round(e.getBoundingClientRect().height)})),
      pgMain: !!document.querySelector('#playground-main'),
      pgClasses: [...document.querySelectorAll('[id^=playground],[class*=playground]')].length,
      preloaderText: (document.getElementById('preloader')||{}).innerText?.slice(0,80) };
  }).catch(e=>({err:e.message}));
  L('STATE@'+t+' '+JSON.stringify(st));
  await page.screenshot({path:`${out}/probe_${t}.png`}).catch(e=>L('shot '+e.message));
}
fs.writeFileSync(`${out}/probe.log`, logs.join('\n'));
await browser.close();
