// Chapter 15 atlas capture: section-by-section screenshots + DOM/style metadata.
// usage: node cap.mjs <slug> <path> <desktop|mobile> [states]
import puppeteer from 'puppeteer';
import fs from 'fs';
const [slug, path, mode = 'desktop', states = ''] = process.argv.slice(2);
const MOB = mode === 'mobile';
const W = MOB ? 390 : 1440, H = MOB ? 844 : 900;
const out = `raw/${slug}/${mode}`;
fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required', '--mute-audio'] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1, isMobile: MOB, hasTouch: MOB });
if (MOB) await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
const t0 = Date.now();
const client = await page.target().createCDPSession();
const log = []; const _p = log.push.bind(log); log.push = m => { const l = ((Date.now() - t0) / 1000).toFixed(1) + 's ' + m; console.log(l); return _p(l); };
const meta = { slug, path, mode, W, H, frames: [] };
page.goto('https://lusion.co' + path, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(e => log.push('goto ' + e.message));
if (states.includes('loader')) {
  for (const t of [900, 2200, 3800]) { await sleep(t - (Date.now() - t0) > 0 ? t - (Date.now() - t0) : 0); try { await page.screenshot({ path: `${out}/state_loader_${t}.png` }); log.push('loader ' + t); } catch (e) { log.push('loader err ' + e.message); } }
}
// wait for preloader to go away
for (let i = 0; i < 40; i++) {
  await sleep(1000);
  const gone = await page.evaluate(() => { const p = document.getElementById('preloader'); if (!p) return true; const s = getComputedStyle(p); return s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0; }).catch(() => false);
  if (gone && i > 6) break;
}
await sleep(3000);
const collect = () => page.evaluate((W, H) => {
  const vis = r => r.width > 6 && r.height > 6 && r.bottom > 0 && r.top < H && r.right > 0 && r.left < W;
  const st = el => { const s = getComputedStyle(el); return { ff: s.fontFamily.split(',')[0].replace(/"/g, ''), fs: s.fontSize, fw: s.fontWeight, ls: s.letterSpacing, lh: s.lineHeight, color: s.color, bg: s.backgroundColor, tt: s.textTransform, op: s.opacity, pos: s.position, disp: s.display, gtc: s.gridTemplateColumns !== 'none' ? s.gridTemplateColumns.split(' ').length : 0, br: s.borderRadius }; };
  const sec = [...document.querySelectorAll('.page .section, #page-extra-sections > *, #footer, .page > [id]')].map(e => { const r = e.getBoundingClientRect(); return { id: e.id, cls: e.className, top: Math.round(r.top), h: Math.round(r.height) }; });
  const cands = [...document.querySelectorAll('#ui [id], #page-container [id], #page-container h1, #page-container h2, #page-container h3, #page-container p, #page-container a, #page-container button, #page-container li')].filter(e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return vis(r) && (window.__menu || !e.closest('#header')) && s.visibility !== 'hidden' && +s.opacity > 0.05 && !['svg', 'path', 'g', 'use', 'canvas'].includes(e.tagName.toLowerCase()); });
  const items = cands.map(e => { const r = e.getBoundingClientRect(); let d = 0, p = e; while (p && p !== document.body) { d++; p = p.parentElement; } return { el: e, r, d }; });
  const pick = [];
  const iou = (a, b) => { const x = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)), y = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)); const i = x * y; return i / (a.width * a.height + b.width * b.height - i); };
  const score = it => (it.el.id ? 0 : 25) + (it.el.innerText && it.el.innerText.trim().length ? 0 : 20) + Math.min(it.el.getElementsByTagName('*').length, 40) * 1.5 + (it.r.width * it.r.height > W * H * 0.4 ? 100 : 0);
  items.sort((a, b) => score(a) - score(b));
  for (const it of items) { if (pick.length >= 14) break; if (pick.some(p => iou(p.r, it.r) > 0.6)) continue; pick.push(it); }
  pick.sort((a, b) => a.r.top - b.r.top || a.r.left - b.r.left);
  return { sections: sec, els: pick.map(({ el, r }) => ({ tag: el.tagName.toLowerCase(), id: el.id, cls: (typeof el.className === 'string' ? el.className : '').trim().split(/\s+/).slice(0, 4).join(' '), text: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 70), x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), st: st(el) })), headerCls: (document.getElementById('header') || {}).className || '', htmlCls: document.documentElement.className };
}, W, H);
const shot = async (name, extra = {}) => { log.push('pre ' + name); await page.screenshot({ path: `${out}/${name}.png`, optimizeForSpeed: true }); const m = await collect().catch(e => ({ err: e.message })); meta.frames.push({ name, ...extra, ...m }); log.push('shot ' + name); fs.writeFileSync(`${out}/meta.json`, JSON.stringify(meta, null, 1)); };
const rectOf = sel => page.evaluate(s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { y: r.top, h: r.height }; }, sel);
const scrollBy = async dy => {
  if (MOB) { await client.send('Input.synthesizeScrollGesture', { x: W / 2, y: H * 0.6, yDistance: -dy, speed: 2500, gestureSourceType: 'touch', repeatCount: 1 }).catch(e => log.push('gest ' + e.message)); }
  else { await page.mouse.move(W * 0.5, H * 0.5); let left = dy; while (Math.abs(left) > 1) { const s = Math.max(-2000, Math.min(2000, left)); await page.mouse.wheel({ deltaY: s }); left -= s; await sleep(60); } }
};
const scrollToY = async (sel, offset) => {
  for (let i = 0; i < 10; i++) { const r = await rectOf(sel); if (!r) return null; const d = r.y - offset; if (Math.abs(d) < 40) return r; await scrollBy(d); await sleep(1500); }
  return rectOf(sel);
};
await shot('00_loaded');
// hover/cursor trail state on first screen
if (states.includes('cursor') && !MOB) {
  for (let i = 0; i < 14; i++) { await page.mouse.move(300 + i * 60, 300 + Math.sin(i / 2) * 180); } log.push('moved');
  await shot('state_cursor_trail');
}
if (states.includes('menu')) {
  await page.click('#header-right-menu-btn').catch(e => log.push('menu ' + e.message)); await sleep(1600); await page.evaluate(() => window.__menu = 1); await shot('state_menu_open'); await page.evaluate(() => window.__menu = 0);
  await page.click('#header-right-menu-btn').catch(() => {}); await sleep(1200);
}
if (states.includes('heroonly')) { await scrollBy(H * 0.9); await sleep(2500); await shot('01_below'); meta.log = log; fs.writeFileSync(`${out}/meta.json`, JSON.stringify(meta, null, 1)); await browser.close(); process.exit(0); }
let secList = (await collect()).sections.filter(s => s.h > 50 && s.id);
const onlyM = states.match(/only=([a-z0-9-]+)/); if (onlyM) secList = secList.filter(s => s.id === onlyM[1]);
meta.sectionList = secList;
let idx = 1;
for (const s of secList) {
  const r = await scrollToY('#' + s.id, 0);
  if (!r) continue;
  await sleep(2200);
  const frames = r.h > 6 * H && !MOB ? 4 : Math.min(MOB ? 1 : 3, Math.max(1, Math.ceil(r.h / H)));
  for (let f = 0; f < frames; f++) {
    const tall = r.h > 6 * H; const nf = tall ? 4 : frames;
    if (f > 0) { await scrollToY('#' + s.id, tall ? -Math.round((r.h - H) * f / (nf - 1) * 0.92) : -f * H * 0.95); await sleep(2000); }
    await shot(`${String(idx).padStart(2, '0')}_${s.id}_${f}`, { section: s.id, part: f });
    idx++;
  }
  if (states.includes('hover') && !MOB && /featured|projects-main/.test(s.id)) {
    const pr = await page.evaluate(() => { const e = [...document.querySelectorAll('.project-item')].find(e => { const r = e.getBoundingClientRect(); return r.top > 60 && r.bottom < innerHeight; }); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
    if (pr) { await page.mouse.move(pr.x, pr.y, { steps: 8 }); await sleep(1500); await shot(`state_hover_${s.id}`); }
  }
}
const stepsM = states.match(/steps=(\d+)/);
if (stepsM) { for (let k = 1; k <= +stepsM[1]; k++) { await scrollBy(H * 0.9); await sleep(2200); await shot(`${String(idx).padStart(2, '0')}_project-details_${k}`, { section: 'project-details', part: k }); idx++; } }
if (states.includes('transition')) {
  await scrollToY('#' + secList[0].id, 0); await sleep(1200);
  const link = path.startsWith('/about') ? '/projects' : '/about';
  await page.evaluate(l => { const a = [...document.querySelectorAll('a')].find(a => a.getAttribute('href') === l); if (a) a.click(); }, link);
  for (const t of [250, 700, 1400]) { await sleep(t === 250 ? 250 : t === 700 ? 450 : 700); await page.screenshot({ path: `${out}/state_transition_${t}.png` }); log.push('trans ' + t); }
}
meta.log = log; meta.ms = Date.now() - t0;
fs.writeFileSync(`${out}/meta.json`, JSON.stringify(meta, null, 1));
await browser.close();

