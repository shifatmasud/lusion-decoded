// Runtime devtools probe: network log, WebGL context/shader/draw-call instrumentation, DOM state, screenshots.
import puppeteer from 'puppeteer';
import fs from 'fs';
const url = process.argv[2] || 'https://lusion.co/';
const tag = process.argv[3] || 'home';
fs.mkdirSync('runtime', { recursive: true });
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage();
const reqs = [], consoleMsgs = [];
page.on('console', m => consoleMsgs.push(m.type() + ': ' + m.text().slice(0, 300)));
page.on('pageerror', e => consoleMsgs.push('pageerror: ' + e.message.slice(0, 300)));
const t0 = Date.now();
page.on('response', r => { try { const h = r.headers(); reqs.push({ t: Date.now() - t0, status: r.status(), type: r.request().resourceType(), len: +(h['content-length'] || 0), ct: (h['content-type'] || '').slice(0, 40), url: r.url() }); } catch (e) {} });
await page.setViewport({ width: 1440, height: 900 });
await page.evaluateOnNewDocument(() => {
  window.__gl = { contexts: [], shaders: [], programs: 0, draws: 0, frames: 0, dpf: [], textures: 0, fbos: 0, ext: [] };
  const og = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, attrs) {
    const ctx = og.call(this, type, attrs);
    if (ctx && /webgl/.test(type) && !ctx.__hooked) {
      ctx.__hooked = 1;
      window.__gl.contexts.push({ type, attrs: attrs || {}, canvasId: this.id });
      const wrap = (n, f) => { if (!ctx[n]) return; const o = ctx[n].bind(ctx); ctx[n] = function () { f && f.apply(null, arguments); return o.apply(null, arguments); }; };
      wrap('shaderSource', (s, src) => window.__gl.shaders.push(src));
      wrap('linkProgram', () => window.__gl.programs++);
      ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced'].forEach(n => wrap(n, () => window.__gl.draws++));
      wrap('createTexture', () => window.__gl.textures++);
      wrap('createFramebuffer', () => window.__gl.fbos++);
      wrap('getExtension', n => window.__gl.ext.push(n));
    }
    return ctx;
  };
  const raf = window.requestAnimationFrame; let last = 0;
  window.requestAnimationFrame = function (cb) { return raf.call(window, function (t) { window.__gl.frames++; const d = window.__gl.draws - last; last = window.__gl.draws; if (window.__gl.dpf.length < 2000) window.__gl.dpf.push(d); cb(t); }); };
});
await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 }).catch(e => consoleMsgs.push('goto: ' + e.message));
await new Promise(r => setTimeout(r, 8000));
await page.screenshot({ path: `runtime/${tag}_0_loaded.png` });
const afterLoad = await page.evaluate(() => ({ frames: __gl.frames, draws: __gl.draws, programs: __gl.programs }));
const steps = +(process.argv[4] || 10);
for (let i = 0; i < steps; i++) {
  await page.mouse.move(400 + i * 50, 350 + (i % 3) * 90, { steps: 8 });
  await page.mouse.wheel({ deltaY: 650 });
  await new Promise(r => setTimeout(r, 1200));
  if (i % 2 === 1) await page.screenshot({ path: `runtime/${tag}_${i + 1}_scroll.png` });
}
const dom = await page.evaluate(() => ({
  title: document.title, htmlClass: document.documentElement.className, bodyClass: document.body.className,
  canvas: [...document.querySelectorAll('canvas')].map(c => ({ id: c.id, w: c.width, h: c.height, cssW: c.clientWidth, cssH: c.clientHeight })),
  preloader: document.getElementById('preloader') ? getComputedStyle(document.getElementById('preloader')).display + '/' + getComputedStyle(document.getElementById('preloader')).visibility : '',
  pageInnerTransform: document.getElementById('page-container-inner')?.style.transform || '',
  windowScrollY: window.scrollY, bodyOverflow: getComputedStyle(document.body).overflow, htmlOverflow: getComputedStyle(document.documentElement).overflow,
  pageInnerStyle: document.getElementById('page-container-inner')?.getAttribute('style') || '',
  splitWords: document.querySelectorAll('.word,.line,.char').length,
  ufxDomCount: document.querySelectorAll('[data-ufx],[class*=ufx]').length
}));
const gl = await page.evaluate(() => ({ contexts: __gl.contexts, programs: __gl.programs, shaderCount: __gl.shaders.length, draws: __gl.draws, frames: __gl.frames, dpfTail: __gl.dpf.slice(-60), textures: __gl.textures, fbos: __gl.fbos, ext: [...new Set(__gl.ext)] }));
const shaders = await page.evaluate(() => __gl.shaders);
const perf = await page.evaluate(() => ({ nav: performance.getEntriesByType('navigation').map(n => ({ dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd), transfer: n.transferSize }))[0], res: performance.getEntriesByType('resource').map(e => ({ n: e.name, it: e.initiatorType, sz: e.transferSize, dec: e.decodedBodySize, st: Math.round(e.startTime), dur: Math.round(e.duration) })) }));
fs.writeFileSync(`runtime/${tag}_report.json`, JSON.stringify({ url, elapsed: Date.now() - t0, afterLoad, dom, gl, perf, responses: reqs, console: consoleMsgs }, null, 1));
fs.mkdirSync(`runtime/${tag}_compiled_shaders`, { recursive: true });
shaders.forEach((s, i) => fs.writeFileSync(`runtime/${tag}_compiled_shaders/${String(i).padStart(3, '0')}.glsl`, s));
console.log(JSON.stringify({ afterLoad, dom, gl: { ...gl, dpfTail: gl.dpfTail.join(',') }, responses: reqs.length, console: consoleMsgs.slice(0, 15) }, null, 1));
await browser.close();
