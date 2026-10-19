// Visual capture for handbook chapters 5-9: loading counter, cursor trail, page transition, pass-by-pass post chain.
import puppeteer from 'puppeteer';
import fs from 'fs';
const out = 'runtime/vis';
fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
const log = [];
page.on('console', m => { if (m.text().startsWith('[vis]')) log.push(m.text()); });
await page.evaluateOnNewDocument(() => {
  window.__cap = { armed: false, shots: [], progs: new Map(), shaderSrc: new Map() };
  const og = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, attrs) {
    const ctx = og.call(this, type, attrs);
    if (ctx && type === 'webgl2' && this.id === 'canvas' && !ctx.__h) {
      ctx.__h = 1; window.__gl2 = ctx; const C = window.__cap; const gl = ctx;
      const oSS = gl.shaderSource.bind(gl); gl.shaderSource = (s, src) => { C.shaderSrc.set(s, src); return oSS(s, src); };
      const oAS = gl.attachShader.bind(gl); gl.attachShader = (p, s) => { if (!C.progs.has(p)) C.progs.set(p, { id: C.progs.size, src: [] }); C.progs.get(p).src.push(C.shaderSrc.get(s) || ''); return oAS(p, s); };
      let cur = null; const oUP = gl.useProgram.bind(gl); gl.useProgram = p => { cur = p; return oUP(p); };
      const oDA = gl.drawArrays.bind(gl);
      gl.drawArrays = function (mode, first, count) {
        const r = oDA(mode, first, count);
        if (C.armed && count === 3 && C.shots.length < 20) {
          try {
            const vp = gl.getParameter(gl.VIEWPORT); const w = vp[2], h = vp[3];
            const fb = gl.getParameter(gl.DRAW_FRAMEBUFFER_BINDING);
            gl.bindFramebuffer(gl.READ_FRAMEBUFFER, fb);
            const rt = gl.getParameter(gl.IMPLEMENTATION_COLOR_READ_TYPE);
            const rf = gl.getParameter(gl.IMPLEMENTATION_COLOR_READ_FORMAT);
            let px; const n = w * h * 4;
            if (rt === gl.FLOAT) { const f = new Float32Array(n); gl.readPixels(0, 0, w, h, gl.RGBA, gl.FLOAT, f); px = new Uint8ClampedArray(n); for (let i = 0; i < n; i++) px[i] = (i % 4 === 3) ? 255 : Math.pow(Math.min(1, Math.max(0, f[i])), 1 / 2.2) * 255; }
            else if (rt === gl.HALF_FLOAT) { px = null; }
            else { px = new Uint8ClampedArray(n); gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px); for (let i = 3; i < n; i += 4) px[i] = 255; }
            const info = C.progs.get(cur); const fs = info ? (info.src[1] || info.src[0] || '') : '';
            const rec = { i: C.shots.length, w, h, fb: !!fb, prog: info ? info.id : -1, rt, rf, frag: fs.replace(/\s+/g, ' ').slice(-600) };
            if (px) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const c2 = cv.getContext('2d'); const id = new ImageData(px, w, h); c2.putImageData(id, 0, 0); const o = document.createElement('canvas'); o.width = w; o.height = h; const c3 = o.getContext('2d'); c3.translate(0, h); c3.scale(1, -1); c3.drawImage(cv, 0, 0); rec.data = o.toDataURL('image/jpeg', 0.85); }
            C.shots.push(rec);
          } catch (e) { C.shots.push({ err: String(e) }); }
        }
        return r;
      };
      const raf = window.requestAnimationFrame;
      window.requestAnimationFrame = cb => raf.call(window, t => { cb(t); if (C.armed && C.shots.length) { C.armed = false; C.done = true; } });
    }
    return ctx;
  };
});
// 1. Loading counter frames
const t0 = Date.now();
page.goto('https://lusion.co/', { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
const loadShots = [];
for (let k = 0; k < 14; k++) {
  await sleep(k < 6 ? 500 : 1000);
  const p = `${out}/load_${k}.png`;
  try { await page.screenshot({ path: p }); const txt = await page.evaluate(() => { const el = document.getElementById('preloader'); return el ? el.innerText.replace(/\s+/g, ' ').slice(0, 80) + ' | ' + getComputedStyle(el).visibility + ' ' + getComputedStyle(el).opacity : 'none'; }); loadShots.push({ k, t: Date.now() - t0, txt }); } catch (e) { loadShots.push({ k, err: String(e) }); }
}
await sleep(6000);
await page.screenshot({ path: `${out}/hero_idle.png` });
// 2. Cursor trail: sweep the mouse across the hero and shoot mid-sweep
await page.mouse.move(300, 600);
for (let a = 0; a <= 40; a++) { const x = 300 + a * 22, y = 450 + Math.sin(a / 4) * 180; await page.mouse.move(x, y, { steps: 2 }); if (a === 28) await page.screenshot({ path: `${out}/trail_a.png` }); }
await page.screenshot({ path: `${out}/trail_b.png` });
await sleep(150); await page.screenshot({ path: `${out}/trail_c.png` });
// 3. Pass-by-pass capture of one frame
await page.mouse.move(700, 450, { steps: 10 });
await page.evaluate(() => { window.__cap.armed = true; });
await sleep(2500);
const shots = await page.evaluate(() => window.__cap.shots);
const meta = [];
shots.forEach((s, i) => { if (s.data) fs.writeFileSync(`${out}/pass_${String(i).padStart(2, '0')}.jpg`, Buffer.from(s.data.split(',')[1], 'base64')); const { data, ...m } = s; meta.push(m); });
fs.writeFileSync(`${out}/passes.json`, JSON.stringify(meta, null, 1));
// 4. Page transition: click a nav link to about and shoot frames
const links = await page.evaluate(() => [...document.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(Boolean).slice(0, 40));
const target = links.find(h => /about/.test(h)) || links.find(h => /projects/.test(h));
const trans = [];
if (target) {
  await page.evaluate(h => { const a = [...document.querySelectorAll('a')].find(a => a.getAttribute('href') === h); a.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true })); a.click(); }, target);
  for (let k = 0; k < 10; k++) { await sleep(k < 6 ? 250 : 700); await page.screenshot({ path: `${out}/trans_${k}.png` }); trans.push({ k, url: page.url(), cls: await page.evaluate(() => document.documentElement.className) }); }
}
fs.writeFileSync(`${out}/capture_log.json`, JSON.stringify({ loadShots, links, target, trans, log }, null, 1));
await browser.close();
console.log('done', shots.length, target);
