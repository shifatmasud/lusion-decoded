import puppeteer from 'puppeteer';
import fs from 'fs';
const dir = '/home/sprite/lusion/vis/html';
const out = '/home/sprite/lusion/vis/png';
fs.mkdirSync(out, { recursive: true });
const only = process.argv.slice(2);
const b = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox'] });
const p = await b.newPage();
await p.setViewport({ width: 1600, height: 900, deviceScaleFactor: 1 });
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
  if (only.length && !only.some(o => f.startsWith(o))) continue;
  await p.setViewport({ width: 1600, height: 900, deviceScaleFactor: 1 });
  await p.goto('file://' + dir + '/' + f, { waitUntil: 'load' });
  const info = await p.evaluate(() => {
    const over = [...document.querySelectorAll('body *')].filter(e => e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== 'hidden' && e.clientWidth > 0).map(e => e.tagName + '.' + e.className + ':' + e.scrollWidth + '>' + e.clientWidth + ' ' + (e.textContent || '').slice(0, 40));
    return { h: Math.ceil(document.body.getBoundingClientRect().height), over: over.slice(0, 8) };
  });
  console.log(f, JSON.stringify(info));
  await p.setViewport({ width: 1600, height: info.h, deviceScaleFactor: 1 });
  await p.screenshot({ path: out + '/' + f.replace('.html', '.png'), fullPage: true });
  console.log('rendered', f);
}
await b.close();
