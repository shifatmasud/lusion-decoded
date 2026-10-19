// Mobile capture for pages whose scroll is a custom ScrollPane (project page): raw touch drags.
// usage: node capm_drag.mjs <slug> <path> <shots>
import puppeteer from 'puppeteer';
import fs from 'fs';
const [slug, path, n = '5'] = process.argv.slice(2);
const W = 390, H = 844;
const out = `raw/${slug}/mobile_drag`;
fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--mute-audio'] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
const client = await page.target().createCDPSession();
const t0 = Date.now(); const log = m => console.log(((Date.now() - t0) / 1000).toFixed(1) + 's ' + m);
page.goto('https://lusion.co' + path, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(e => log('goto ' + e.message));
for (let i = 0; i < 40; i++) { await sleep(1000); const gone = await page.evaluate(() => { const p = document.getElementById('preloader'); if (!p) return true; const s = getComputedStyle(p); return s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0; }).catch(() => false); if (gone && i > 6) break; }
await sleep(3000);
const info = () => page.evaluate(() => { const q = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; }; return { meta: q('#project-details-meta'), items: q('#project-details-items-move-container'), preview: q('#project-details-preview'), first: q('.project-details-item'), footer: q('#footer') }; });
const drag = async dy => {
  const x = W / 2, y0 = H * 0.75; const steps = 24;
  await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: y0 }] });
  for (let i = 1; i <= steps; i++) { await client.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: y0 - dy * i / steps }] }); await sleep(16); }
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
};
await page.screenshot({ path: `${out}/00.png` }); log('00 ' + JSON.stringify(await info()));
for (let k = 1; k <= +n; k++) {
  await drag(H * 0.55); await sleep(2500);
  const name = String(k).padStart(2, '0');
  await page.screenshot({ path: `${out}/${name}.png` }); log(name + ' ' + JSON.stringify(await info()));
}
await browser.close();
