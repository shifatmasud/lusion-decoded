// Visual captures for handbook chapters 1-4: preloader, DOM-only vs WebGL-only layers, Ufx rect overlays.
import puppeteer from 'puppeteer';
import fs from 'fs';
fs.mkdirSync('runtime/v', { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
const log = [];
page.goto('https://lusion.co/', { waitUntil: 'networkidle2', timeout: 90000 }).catch(e => log.push('goto ' + e.message));
// preloader frames
for (const t of [1200, 2500, 4000]) {
  await sleep(t === 1200 ? 1200 : 1300);
  try {
    const pct = await page.evaluate(() => { const p = document.getElementById('preloader'); return p ? (getComputedStyle(p).display + ' ' + (p.innerText || '').replace(/\s+/g, ' ').slice(0, 60)) : 'none'; });
    log.push('preloader@' + t + ': ' + pct);
    await page.screenshot({ path: `runtime/v/preloader_${t}.png` });
  } catch (e) { log.push('pre ' + e.message); }
}
await sleep(9000);
await page.screenshot({ path: 'runtime/v/hero.png' });
const layers = async (tag) => {
  await page.screenshot({ path: `runtime/v/${tag}_both.png` });
  await page.evaluate(() => { document.getElementById('canvas').style.visibility = 'hidden'; });
  await sleep(300);
  await page.screenshot({ path: `runtime/v/${tag}_dom.png` });
  await page.evaluate(() => { document.getElementById('canvas').style.visibility = ''; const p = document.getElementById('page-container'); p.style.opacity = '0'; const h = document.getElementById('header'); if (h) h.style.opacity = '0'; });
  await sleep(600);
  await page.screenshot({ path: `runtime/v/${tag}_gl.png` });
  await page.evaluate(() => { document.getElementById('page-container').style.opacity = ''; const h = document.getElementById('header'); if (h) h.style.opacity = ''; });
  await sleep(300);
};
await layers('hero');
// scroll to reel, then projects
const rectOf = sel => page.evaluate(s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; }, sel);
const scrollTo = async (sel, targetY = 120) => {
  for (let i = 0; i < 40; i++) {
    const r = await rectOf(sel);
    if (!r) return null;
    if (r.y < targetY + 150 && r.y > -r.h * 0.3) return r;
    await page.mouse.move(700 + (i % 5) * 20, 450);
    await page.mouse.wheel({ deltaY: Math.max(-700, Math.min(700, r.y - targetY)) });
    await sleep(900);
  }
  return rectOf(sel);
};
log.push('reel ' + JSON.stringify(await scrollTo('#home-reel-container-inner', 60)));
await sleep(1500);
await layers('reel');
log.push('proj ' + JSON.stringify(await scrollTo('.project-item-main', 140)));
await sleep(2000);
const rects = await page.evaluate(() => [...document.querySelectorAll('.project-item-main, #home-reel-container-inner, #home-reel-thumb')].map(e => { const r = e.getBoundingClientRect(); return { sel: e.id ? '#' + e.id : '.' + e.className.split(' ')[0], x: r.x, y: r.y, w: r.width, h: r.height }; }).filter(r => r.y < 900 && r.y + r.h > 0));
log.push('rects ' + JSON.stringify(rects));
fs.writeFileSync('runtime/v/rects.json', JSON.stringify(rects));
await layers('proj');
const shell = await page.evaluate(() => { const out = []; const walk = (el, d) => { if (d > 3) return; out.push('  '.repeat(d) + el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '')); [...el.children].filter(c => !['SCRIPT', 'STYLE', 'LINK', 'META'].includes(c.tagName)).slice(0, 8).forEach(c => walk(c, d + 1)); }; walk(document.body, 0); return out.join('\n'); });
fs.writeFileSync('runtime/v/shell.txt', shell);
fs.writeFileSync('runtime/v/log.txt', log.join('\n'));
await browser.close();
console.log(log.join('\n'));
