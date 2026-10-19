// Chapter 10 visuals: desktop/mobile captures, grid overlay, header recolouring per section, rolling letters.
import puppeteer from 'puppeteer';
import fs from 'fs';
const out = '/home/sprite/lusion/vis/raw';
fs.mkdirSync(out, { recursive: true });
const args = ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const browser = await puppeteer.launch({ headless: 'shell', args });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const log = {};

async function open(w, h, mobile) {
  const p = await browser.newPage();
  await p.setViewport({ width: w, height: h, isMobile: !!mobile, hasTouch: !!mobile, deviceScaleFactor: 1 });
  if (mobile) await p.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
  await p.goto('https://lusion.co/', { waitUntil: 'networkidle2', timeout: 90000 }).catch(e => console.log('goto', e.message));
  for (let i = 0; i < 40; i++) { const ok = await p.evaluate(() => document.documentElement.classList.contains('is-ready')); if (ok) break; await sleep(1000); }
  await sleep(4000);
  return p;
}
const state = p => p.evaluate(() => {
  const hd = document.querySelector('#header');
  const logo = document.querySelector('#header-logo');
  const cs = el => el ? getComputedStyle(el) : null;
  const root = getComputedStyle(document.documentElement);
  return {
    html: document.documentElement.className,
    headerColor: cs(hd) && cs(hd).color, logoColor: cs(logo) && cs(logo).color,
    padX: root.getPropertyValue('--base-padding-x'), gap: root.getPropertyValue('--grid-gap'), headerVar: root.getPropertyValue('--header-text-color'),
  };
});

// Desktop
const d = await open(1440, 900);
log.desktop0 = await state(d);
await d.screenshot({ path: out + '/d_hero.png' });
// grid overlay using the live tokens
await d.evaluate(() => {
  const g = document.createElement('div');
  g.id = '__grid';
  g.style.cssText = 'position:fixed;inset:0;z-index:99999;pointer-events:none;padding:0 var(--base-padding-x);display:flex;gap:var(--grid-gap);box-sizing:border-box';
  for (let i = 0; i < 12; i++) { const c = document.createElement('div'); c.style.cssText = 'flex:1;background:rgba(255,40,120,.18);border-left:1px solid rgba(255,40,120,.7);border-right:1px solid rgba(255,40,120,.7);display:flex;align-items:flex-end;justify-content:center;font:600 14px monospace;color:#ff2878;padding-bottom:10px'; c.textContent = i + 1; g.append(c); }
  document.body.append(g);
});
await sleep(500);
await d.screenshot({ path: out + '/d_grid.png' });
log.gridCols = await d.evaluate(() => [...document.querySelectorAll('#__grid > div')].map(c => { const r = c.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.width)]; }));
await d.evaluate(() => document.getElementById('__grid').remove());
// scroll through, recording state + header band
log.scroll = [];
await d.mouse.move(720, 450);
for (let i = 0; i < 16; i++) {
  const s = await state(d);
  log.scroll.push({ i, ...s });
  await d.screenshot({ path: `${out}/d_s${String(i).padStart(2, '0')}.png` });
  for (let k = 0; k < 8; k++) { await d.mouse.wheel({ deltaY: 300 }); await sleep(40); }
  await sleep(1200);
  fs.writeFileSync(out + '/log10.json', JSON.stringify(log, null, 1));
}
// rolling letters: find char-wrapper elements
log.chars = await d.evaluate(() => {
  const w = [...document.querySelectorAll('.char-wrapper')];
  return { count: w.length, parents: [...new Set(w.map(x => (x.parentElement && (x.parentElement.id || x.parentElement.className)) || ''))].slice(0, 10) };
});
await d.close();

// Mobile below the 812px breakpoint
const m = await open(390, 844, true);
log.mobile0 = await state(m);
await m.screenshot({ path: out + '/m_hero.png' });
await m.close();
// Just above / just below the breakpoint on desktop UA
for (const w of [813, 812]) {
  const p = await open(w, 900);
  log['w' + w] = await state(p);
  fs.writeFileSync(out + '/log10.json', JSON.stringify(log, null, 1));
  await p.screenshot({ path: `${out}/w${w}.png` });
  await p.close();
}
fs.writeFileSync(out + '/log10.json', JSON.stringify(log, null, 1));
await browser.close();
console.log(JSON.stringify(log).slice(0, 3000));
