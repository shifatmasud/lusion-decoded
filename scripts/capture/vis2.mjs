// Visual capture for handbook chapters 5-9: loading counter, cursor trail, page transition, pass-by-pass post chain.
import puppeteer from 'puppeteer';
import fs from 'fs';
const out = 'runtime/vis';
fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800 });
page.setDefaultTimeout(120000);
const mode = process.argv[2];
page.on('error', e => console.log('crash', e.message));
const log = [];
page.on('console', m => { if (m.text().startsWith('[vis]')) log.push(m.text()); });
await page.evaluateOnNewDocument(() => {
  window.__cap = { armed: false, shots: [], progs: new Map(), shaderSrc: new Map() };
  const og = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, attrs) {
    const ctx = og.call(this, type, attrs);
    if (ctx && type === 'webgl2' && !ctx.__h) {
      ctx.__h = 1; window.__gl2 = ctx; const C = window.__cap; const gl = ctx;
      const oSS = gl.shaderSource.bind(gl); gl.shaderSource = (s, src) => { C.shaderSrc.set(s, src); return oSS(s, src); };
      const oAS = gl.attachShader.bind(gl); gl.attachShader = (p, s) => { if (!C.progs.has(p)) C.progs.set(p, { id: C.progs.size, src: [] }); C.progs.get(p).src.push(C.shaderSrc.get(s) || ''); return oAS(p, s); };
      let cur = null; const oUP = gl.useProgram.bind(gl); gl.useProgram = p => { cur = p; return oUP(p); };
      const oDA = gl.drawArrays.bind(gl); C.calls = {};
      gl.drawArrays = function (mode, first, count) {
        const r = oDA(mode, first, count); C.calls[count] = (C.calls[count] || 0) + 1;
        if (C.armed && count === 3 && C.shots.length < 40) { const vp0 = gl.getParameter(gl.VIEWPORT); const key = (C.progs.get(cur) || {id:-1}).id + '_' + vp0[2] + 'x' + vp0[3] + '_' + !!gl.getParameter(gl.DRAW_FRAMEBUFFER_BINDING); C.seen = C.seen || {}; C.order = C.order || []; C.order.push(key); if (C.seen[key]) return r; C.seen[key] = 1;
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
            const rec = { i: C.shots.length, w, h, fb: !!fb, prog: info ? info.id : -1, rt, rf, frag: fs.replace(/\s+/g, ' ').slice(-300), unis: [...new Set((fs.match(/uniform\s+\w+\s+(\w+)/g) || []).map(x => x.split(/\s+/).pop()))].join(','), order: C.order.length };
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

await page.goto('https://lusion.co/', { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
await sleep(+(process.argv[3] || 16000));
if (mode === 'trail') {
  await page.screenshot({ path: `${out}/t_idle.png` });
  await page.mouse.move(250, 600);
  for (let a = 0; a <= 30; a++) { await page.mouse.move(250 + a * 26, 420 + Math.sin(a / 4) * 170); await sleep(30); }
  await page.screenshot({ path: `${out}/t_trail1.png` });
  for (let a = 30; a >= 0; a--) { await page.mouse.move(250 + a * 26, 420 - Math.sin(a / 4) * 170); await sleep(30); }
  await page.screenshot({ path: `${out}/t_trail2.png` });
}
if (mode === 'passes') {
  await page.mouse.move(500, 400); for (let a = 0; a < 12; a++) { await page.mouse.move(500 + a * 25, 400 + a * 10); await sleep(30); }
  await page.evaluate(() => { window.__cap.armed = true; });
  await sleep(4000);
  const shots = await page.evaluate(() => window.__cap.shots); fs.writeFileSync(`${out}/pass_order.json`, JSON.stringify(await page.evaluate(() => window.__cap.order)));
  const meta = [];
  shots.forEach((s, i) => { if (s.data) fs.writeFileSync(`${out}/pass_${String(i).padStart(2, '0')}.jpg`, Buffer.from(s.data.split(',')[1], 'base64')); const { data, ...m } = s; meta.push(m); });
  fs.writeFileSync(`${out}/passes.json`, JSON.stringify(meta, null, 1));
  console.log('passes', shots.length, JSON.stringify(await page.evaluate(() => window.__cap.calls)), await page.evaluate(() => document.documentElement.className));
}
if (mode === 'trans') {
  const links = await page.evaluate(() => [...document.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(Boolean));
  const target = links.find(h => /^\/?about/.test(h)) || links.find(h => /projects/.test(h));
  console.log('target', target, links.slice(0, 20).join(' '));
  await page.evaluate(h => { const a = [...document.querySelectorAll('a')].find(a => a.getAttribute('href') === h); a.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true })); a.dispatchEvent(new MouseEvent('mouseover', { bubbles: true })); }, target);
  await sleep(2000);
  await page.evaluate(h => { const a = [...document.querySelectorAll('a')].find(a => a.getAttribute('href') === h); a.click(); }, target);
  const t0 = Date.now(); const log = [];
  for (let k = 0; k < 8; k++) { await sleep(150); await page.screenshot({ path: `${out}/tr_${k}.png` }); log.push({ k, t: Date.now() - t0, url: page.url(), cls: await page.evaluate(() => document.documentElement.className) }); }
  console.log(JSON.stringify(log));
}
await browser.close();
