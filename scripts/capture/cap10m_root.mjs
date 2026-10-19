import puppeteer from 'puppeteer';
import fs from 'fs';
const out = '/home/sprite/lusion/vis/raw';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage();
await p.setViewport({ width: 390, height: 844 });
await p.goto('https://lusion.co/', { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(e => console.log(e.message));
for (let i = 0; i < 40; i++) {
  await sleep(5000);
  const buf = await p.screenshot({ path: `${out}/m_try.png` });
  const html = await p.evaluate(() => document.documentElement.className);
  const sum = await p.evaluate(async b64 => { const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode(); const c = document.createElement('canvas'); c.width = 39; c.height = 84; const x = c.getContext('2d'); x.drawImage(im, 0, 0, 39, 84); const d = x.getImageData(0, 0, 39, 84).data; let s = 0; for (let k = 0; k < d.length; k += 4) s += d[k]; return s / (d.length / 4); }, buf.toString('base64')).catch(() => -1);
  console.log(i, html, sum.toFixed(1));
  if (sum > 25 && html.includes('is-ready')) { await sleep(3000); await p.screenshot({ path: `${out}/m_hero.png` }); console.log('saved'); break; }
}
await b.close();
