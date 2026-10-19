// Lean chapter 10 capture: mobile layout, then header states while scrolling /about.
import puppeteer from 'puppeteer';
import fs from 'fs';
const out = '/home/sprite/lusion/vis/raw';
const logf = out + '/log10b.json';
const log = { about: [] };
const save = () => fs.writeFileSync(logf, JSON.stringify(log, null, 1));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
async function open(url, w, h, mobile) {
  const p = await b.newPage();
  await p.setViewport({ width: w, height: h, isMobile: !!mobile, hasTouch: !!mobile });
  if (mobile) await p.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(e => console.log('goto', e.message));
  for (let i = 0; i < 60; i++) { if (await p.evaluate(() => document.documentElement.classList.contains('is-ready')).catch(() => false)) break; await sleep(1000); }
  await sleep(3000);
  return p;
}
const st = p => p.evaluate(() => {
  const g = s => document.querySelector(s);
  const c = el => el ? getComputedStyle(el).color : null;
  const r = getComputedStyle(document.documentElement);
  return { html: document.documentElement.className, header: c(g('#header')), logo: c(g('#header-logo')), padX: r.getPropertyValue('--base-padding-x'), gap: r.getPropertyValue('--grid-gap'), useMobile: window.innerWidth <= 812 };
});
// mobile
const m = await open('https://lusion.co/', 390, 844, true);
log.mobile = await st(m); save();
await m.screenshot({ path: out + '/m_hero.png' });
await m.close();
// about page, desktop
const a = await open('https://lusion.co/about', 1440, 900);
await a.mouse.move(720, 450);
let last = '';
for (let i = 0; i < 18; i++) {
  const s = await st(a);
  log.about.push({ i, ...s }); save();
  if (s.html !== last) { await a.screenshot({ path: `${out}/a_${String(i).padStart(2, '0')}.png` }); last = s.html; }
  for (let k = 0; k < 10; k++) { await a.mouse.wheel({ deltaY: 400 }); await sleep(30); }
  await sleep(900);
}
await b.close();
console.log('done');
