> **Read in Notion:** [15.2 About](https://shifatmasud.notion.site/3fe48559569d810a98a2ee47788dcbb5) · Part of [Lusion.co Decoded](https://shifatmasud.notion.site/Lusion-co-Decoded-Client-Side-Handbook-3fd48559569d81dd80b4c7407caf27cc) · [Repo home](https://github.com/shifatmasud/lusion-decoded)

<callout icon="🗺️" color="blue_bg">
	The about page opens with a big WebGL hero: a figure, rocks, fog, particles, light, halo, faces and letters, about 15 modules in all (079 to 094). Next is a sideways-scrolling "who" story with the team, then clients, awards and capabilities.
</callout>

**Sections in scroll order:** `AboutHero` WebGL scene (behind the first screen of `#about-who`, no DOM section) → `#about-who` → `#about-clients` → `#about-award` → `#about-capability` → shared tail (`#end-section`, `#footer-section`, `#scroll-nav-section`, documented on [15.1 Home](https://shifatmasud.notion.site/3fe48559569d817bb6bfdc1a46b69d91))

**How to read this page:** each section has one image (desktop 1440×900 frames on top, mobile 390×844 row below). Numbers in the image match the callout table. Values in code blocks and tables are exact (from the shipped CSS, module source or measured computed styles); anything written as *inferred* is a reading, not a measured value. Screenshots come from a headless browser with software WebGL, so glow and colour can look flatter than on a real GPU.

**Tokens every section below uses (exact, from `:root` in the shipped CSS)**
```css
--color-blue: #1a2ffb;  --color-dark-blue: #071bdf;  --header-color: #0016ec;
--color-black: #000000; --color-white: #fff;  --color-off-white: #f0f1fa;  --color-dark-white: #e4e6ef;
--color-grey-blue: #2b2e3a; --color-green: #c1ff00; --color-red: #ff4c41; --color-purple: #8832f7;
--grid-gap: 2vw;            /* 4vw at max-width 812px */
--grid-space: calc((100% - 11 * var(--grid-gap)) / 12);   /* 12 columns; 6 on mobile */
--base-padding-x: max(5vw, 40px);        /* 25px <=812px, 15px <=400px, max(6vw,60px) at >=21:9 */
--base-padding-y: clamp(30px, 4vw, 50px); /* 25px <=812px, 15px <=400px */
--global-border-radius: 20px;             /* 10px at <=812px */
--header-size: clamp(1rem, 1vw, 2rem);  --cross-size: clamp(0.875rem, 1vw, 2rem);
```
Fonts: Aeonik 400 / 500 / 400 italic (body and display), IBMPlexMono 400 / 500 and LusionMono 400 (labels, counters, crosses), all `font-display: block` from `/assets/fonts/`. Background state is a class on `<html>`: `is-black-bg`, `is-blue-bg` or `is-white-bg`; under the first two the header text and scroll bar turn white.

## 1. Hero (WebGL figure scene)  `AboutHero` (no DOM section of its own)

*There is no `#about-hero` element in the page. The hero is the `AboutHero` WebGL scene (modules 079 to 094) drawn behind the first viewport of `#about-who`; the HTML on top of it belongs to `#about-who`, which is why the callouts below name `#about-who` elements.*

![Hero (WebGL figure scene): desktop frames with numbered callouts, mobile row underneath](../assets/15/about__about-hero.jpg)

**Rebuild spec**
This first screen is almost all WebGL. `AboutHero` puts together a person model, rocks, ground, fog, a particle simulation (GPU ping-pong), a light field, a halo, faces and 3D letters. It also runs its own pre-pass and effects pass (`AboutPageHeroEfxPrepass` and `AboutPageHeroEfx`) before the shared post stack. The intro plays in with `fit(introRatio, 0.01, 0.1, 0, 1, ease.cubicOut)`. Scrolling moves the camera and scene down 0 to -10 units with `ease.sineOut`. The HTML on top is only the header and the bottom-left and bottom-right title words, which belong to `#about-who` (next section).

**Mobile (390 wide):** Same scene at lower resolution, with smaller particle counts set by the quality tier (inferred).

**Driven by:** `094_AboutHero`, `084_AboutHeroParticles`, `085_AboutHeroRocks`, `089_AboutHeroFog`, `093_AboutHeroLetters`, `092_AboutPageHeroEfx`. Shaders: `AboutHero__aboutHeroVisualFinalFrag.frag.glsl`, `AboutHeroParticles__fragSd.frag.glsl`, `AboutHeroParticles__lightFieldFrag.frag.glsl`, `AboutHeroParticles__lightFieldVert.vert.glsl`, `AboutHeroParticles__motionFrag.frag.glsl`, `AboutHeroParticles__motionVert.vert.glsl`, `AboutHeroParticles__vertS9.vert.glsl`, `AboutHeroRocks__fragSc.frag.glsl`, `AboutHeroRocks__lightShadowMapFrag.frag.glsl`, `AboutHeroRocks__vertS8.vert.glsl` …. Handbook: [Chapter 7 (Effects and scenes)](https://shifatmasud.notion.site/3fd48559569d81549fa5ff6c49d305fb), [Chapter 8 (Shaders and post-processing)](https://shifatmasud.notion.site/3fd48559569d81daa932c9558ddf8b9a).

**Callouts (measured on the live page at capture time)**
<table header-row="true">
<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>
<tr><td>00 · 1</td><td>`div#about-who-subsection-we-are`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 1440x900</td></tr>
<tr><td>00 · 2</td><td>`div#about-who`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 1440x14580</td></tr>
<tr><td>00 · 3</td><td>`div#about-who-subsection-container`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 5040x900</td></tr>
<tr><td>00 · 4</td><td>`div#about-who-team-faces`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>72,130 907x720</td></tr>
<tr><td>00 · 5</td><td>`div#about-who-team-right`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>1057,150 311x700</td></tr>
<tr><td>00 · 6</td><td>`div#about-crosses`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>79,449 1282x10</td></tr>
<tr><td>00 · 7</td><td>`div#about-who-title-left`</td><td>WE ARE A CREATIVE PRODUCTION STUDIO</td><td>Aeonik 57.6px/66.24px w400 ls normal</td><td>#ffffff / transparent</td><td>72,585 568x265</td></tr>
</table>
*4 more callouts are in the image and in img/about/desktop/legend.json.*

**Driver facts (from the module source)**
- `094_AboutHero`: Easings: `sineOut x3; cubicOut x1; sineInOut x1` · Uniforms: `u_hudRatio; u_introDeltaTime; u_introRatio; u_introTime; u_letterTexture; u_sceneHideRatio; u_sceneRatio`
- `084_AboutHeroParticles`: Uniforms: `u_aspect; u_emissiveRatio; u_isEmissive; u_noiseStableFactor; u_simCurrPosLifeTexture; u_simPrevPosLifeTexture; u_simTextureSize`

## 2. Who we are (horizontal story)  `#about-who`

![Who we are (horizontal story): desktop frames with numbered callouts, mobile row underneath](../assets/15/about__about-who.jpg)

**Rebuild spec**
This is a scroll-jacked horizontal track. `#about-who` gets `padding-bottom: 950vw` so there's a lot of vertical scroll, and inside it `#about-who-subsection-container` (350vw wide, 100vh tall) moves sideways. Its position is a chain of `fit(t, e[i], e[i+1], i, i+1, ease.cubicInOut)` steps, so it eases from one panel to the next instead of sliding at a constant speed. The panels are: We are (the title words `#about-who-title-left`, 4vw, and `#about-who-title-right`, 4vw italic, sit bottom-left and bottom-right), Details (`#about-who-subsection-details`, 4vw), and Team (`#about-who-team`: a flex row of faces, with a blue round cursor `#about-who-face-cursor`, 8.6rem across, `--color-blue`, that follows the mouse over the faces). Text is white over the dark WebGL background.

**Mobile (390 wide):** There's no sideways track: the container is 100% wide and the panels stack. Padding drops to `calc(var(--vh) * 1125)`, the titles go to 8vw under 560px, and the scroll label is centred at 4vw.

**Driven by:** `100_AboutWhoSection`, `096_WhoSubsectionWeAre`, `097_WhoSubsectionDetails`, `099_WhoSubsectionTeam`, `095_AboutWhoLogo`. Shaders: `WhoSubsectionTeam__letterFrag.frag.glsl`, `WhoSubsectionTeam__letterVert.vert.glsl`, `AboutWhoLogo__fragS4.frag.glsl`, `AboutWhoLogo__vertS1.vert.glsl`. Handbook: [Chapter 5 (Scroll, input and motion)](https://shifatmasud.notion.site/3fd48559569d816d8a50c22e35b3ce7b).

**Callouts (measured on the live page at capture time)**
<table header-row="true">
<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>
<tr><td>01 · 1</td><td>`div#about-who-subsection-we-are`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 1440x900</td></tr>
<tr><td>01 · 2</td><td>`div#about-who`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 1440x14580</td></tr>
<tr><td>01 · 3</td><td>`div#about-who-subsection-container`</td><td>SCROLL TO EXPLORE WE ARE A CREATIVE PROD</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,0 5040x900</td></tr>
<tr><td>01 · 4</td><td>`div#about-who-team-faces`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>72,130 907x720</td></tr>
<tr><td>01 · 5</td><td>`div#about-who-team-right`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>1057,150 311x700</td></tr>
<tr><td>01 · 7</td><td>`div#about-who-title-left`</td><td>WE ARE A CREATIVE PRODUCTION STUDIO</td><td>Aeonik 57.6px/66.24px w400 ls normal</td><td>#ffffff / transparent</td><td>72,585 568x265</td></tr>
<tr><td>01 · 8</td><td>`div#about-who-title-main`</td><td>SCROLL TO EXPLORE</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>72,586 1296x264</td></tr>
</table>
*38 more callouts are in the image and in img/about/desktop/legend.json.*

**Driver facts (from the module source)**
- `100_AboutWhoSection`: DOM hooks: `#about-crosses ; #about-who; #about-who-subsection-container` · Easings: `cubicInOut x4`
- `096_WhoSubsectionWeAre`: DOM hooks: `#about-who-subsection-we-are; #about-who-title-main-scroll; .about-who-title-right-text` · Easings: `cubicOut x4; cubicInOut x1`

**Exact CSS (desktop rules, then 812px / 560px overrides)**
```css
#about-who { position: relative; display: block; color: var(--color-white); width: 100vw; padding: 0; padding-bottom: 950vw; font-size: clamp(0.875rem, 1vw, 1.75rem); }
#about-who-subsection-container { position: relative; width: 350vw; height: calc(var(--vh, 1vh) * 100); will-change: transform; }
#about-who-subsection-we-are, #about-who-subsection-details { margin-right: 25vw; }
#about-who-face-cursor { background: var(--color-blue); width: 8.6rem; height: 8.6rem; border-radius: 100%; position: absolute; top: calc(var(--base-padding-y) * -1); left: 0; transform: scale(0); display: flex; justify-content: center; align-items: center; pointer-events: none; }
#about-who-face-cursor svg { height: 30%; width: 30%; }
#about-who-title-main { position: absolute; width: calc(100% - var(--base-padding-x) * 2); bottom: calc(var(--base-padding-y)); }
#about-who-title-main-logo { width: 100%; }
@media (max-width: 812px) | #about-who { width: 100%; height: auto; padding-bottom: calc(var(--vh, 1vh) * 1125); font-size: clamp(0.95rem, 1vw, 1.75rem); }
@media (max-width: 812px) | #about-who-subsection-container { width: 100%; height: calc(var(--vh, 1vh) * 100); }
@media (max-width: 812px) | #about-who-subsection-we-are, #about-who-subsection-details { margin-right: 0; }
@media (max-width: 812px) | #about-who-title-main { bottom: calc(var(--base-padding-y) * 3); }
```
*73 more matching rules in lusion_pretty.css.*

**DOM outline (served HTML, 2 levels)**
```
div#about-who.section
  div#about-who-subsection-container
    div#about-crosses
    div#about-who-subsection-we-are.about-who-subsection
    div#about-who-subsection-details.about-who-subsection
    div#about-who-subsection-team.about-who-subsection
```

## 3. Clients  `#about-clients`

![Clients: desktop frames with numbered callouts, mobile row underneath](../assets/15/about__about-clients.jpg)

**Rebuild spec**
The title `#about-clients-title` is split into words and wrapped in `about-clients-title-word-wrapper`. Under it is the description `#about-clients-desc` (its lines rise 100% to 0 with `ease.lusion`) and a logo carousel `#about-clients-carousel`. It's made of `.about-clients-carousel-line` rows inside wrappers, which drift sideways and slow down with `ease.expoOut`. HTML and CSS only.

**Mobile (390 wide):** The carousel rows shrink and the gutter becomes 4vw.

**Driven by:** `101_AboutClientSection`. No section-specific shader files (HTML + shared Ufx/post passes). Handbook: [Chapter 10 (CSS, layout and DOM state)](https://shifatmasud.notion.site/3fd48559569d81289d5ff6769e1f1d55).

**Callouts (measured on the live page at capture time)**
<table header-row="true">
<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>
<tr><td>07 · 1</td><td>`div#about-clients`</td><td>BRANDS BRANDS BRANDS WE WE WE WORK WORK </td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#f0f1fa / transparent</td><td>0,-50 1440x1049</td></tr>
<tr><td>07 · 2</td><td>`div#about-clients-title`</td><td>BRANDS BRANDS BRANDS WE WE WE WORK WORK </td><td>Aeonik 57.6px/66.24px w400 ls normal</td><td>#f0f1fa / transparent</td><td>72,175 672x66</td></tr>
<tr><td>07 · 3</td><td>`div#about-clients-header`</td><td>BRANDS BRANDS BRANDS WE WE WE WORK WORK </td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#f0f1fa / transparent</td><td>72,175 1296x66</td></tr>
<tr><td>07 · 4</td><td>`div#about-clients-desc`</td><td>TRUSTED BY GLOBAL BRANDS, CULTURAL INSTI</td><td>Aeonik 12.6px/15.12px w400 ls normal uppercase</td><td>#f0f1fa / transparent</td><td>1192,178 176x60</td></tr>
<tr><td>07 · 5</td><td>`div#about-clients-carousel`</td><td></td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#f0f1fa / transparent</td><td>22,259 1440x590</td></tr>
</table>

**Driver facts (from the module source)**
- `101_AboutClientSection`: DOM hooks: `#about-clients; #about-clients-carousel; #about-clients-desc; #about-clients-title; .about-clients-carousel-line` · Easings: `lusion x2; expoOut x1` · Classes toggled: `about-clients-carousel-line-wrapper; about-clients-title-word-wrapper`

**Exact CSS (desktop rules, then 812px / 560px overrides)**
```css
#about-clients { color: var(--color-off-white); align-items: flex-end; padding-top: calc(var(--vh, 1vh) * 25); padding-bottom: calc(var(--vh, 1vh) * 15); font-size: clamp(0.75rem, 1vw, 1.75rem); }
#about-clients-header { display: flex; justify-content: space-between; align-items: center; grid-column: 1 / span 12; }
#about-clients-title { display: flex; grid-gap: 0.3em; overflow: hidden; height: 1.15em; font-size: 4em; will-change: transform; }
#about-clients-title span { display: inline-block; white-space: nowrap; }
#about-clients-desc { font-size: 0.875em; line-height: 1.2; text-transform: uppercase; text-align: right; width: 14em; will-change: transform; }
#about-clients-carousel { position: relative; width: 100vw; margin-top: calc(var(--vh, vh) * 2); margin-bottom: 1em; left: -50px; }
@media (max-width: 812px) | #about-clients { padding-top: var(--base-padding-y); padding-bottom: calc(var(--vh, 1vh) * 10); }
@media (max-width: 812px) | #about-clients-header { flex-direction: column; align-items: flex-start; grid-column: 1 / span 6; }
@media (max-width: 812px) | #about-clients-title { font-size: 14vw; margin-top: 2em; height: inherit; flex-wrap: wrap; justify-content: center; row-gap: 0.1em; }
@media (max-width: 812px) | #about-clients-desc { text-align: center; margin: 4em auto auto; font-size: 1.2em; width: 20em; }
```
*4 more matching rules in lusion_pretty.css.*

**DOM outline (served HTML, 2 levels)**
```
div#about-clients.section
  div#about-clients-header
    div#about-clients-title
    div#about-clients-desc
  div#about-clients-carousel
    div.about-clients-carousel-line  ×3
```

## 4. Awards  `#about-award`

![Awards: desktop frames with numbered callouts, mobile row underneath](../assets/15/about__about-award.jpg)

**Rebuild spec**
The award list. `.about-award-header` holds an SVG badge and title. Each `.about-award-item` is a row of award name and count, with a rule above it (`.about-award-line`). Rows come in with `ease.expoOut`, sliding from 30 to 0 and fading from 100 to 0, staggered `index / 25`. The badge pops with `ease.backOut` between timer values 0.2 and 0.6. Two `UfxMesh` objects draw WebGL parts in the header (inferred: the 3D award badge and a highlight).

**Mobile (390 wide):** Rows wrap. The count moves under the name (inferred from the 812px block).

**Driven by:** `104_AboutAwardSection`. Shaders: `AboutAwardSection__titleFrag.frag.glsl`, `AboutAwardSection__titleVert.vert.glsl`. Handbook: [Chapter 4 (DOM to WebGL sync, Ufx)](https://shifatmasud.notion.site/3fd48559569d816eb890f8d968ec1fae).

**Callouts (measured on the live page at capture time)**
<table header-row="true">
<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>
<tr><td>08 · 1</td><td>`p.about-award-item-wrapper-text`</td><td>Awwwards</td><td>Aeonik 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>706,338 216x21</td></tr>
<tr><td>08 · 2</td><td>`p.about-award-item-wrapper-text`</td><td>001</td><td>IBMPlexMono 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>958,338 33x21</td></tr>
<tr><td>08 · 3</td><td>`p.about-award-item-wrapper-text`</td><td>001</td><td>IBMPlexMono 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>958,370 33x21</td></tr>
<tr><td>08 · 4</td><td>`p.about-award-item-wrapper-text`</td><td>001</td><td>IBMPlexMono 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>958,402 33x21</td></tr>
<tr><td>08 · 5</td><td>`p.about-award-item-wrapper-text`</td><td>010</td><td>IBMPlexMono 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>958,435 33x21</td></tr>
<tr><td>08 · 6</td><td>`p.about-award-item-wrapper-text`</td><td>016</td><td>IBMPlexMono 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>958,467 33x21</td></tr>
<tr><td>08 · 7</td><td>`p.about-award-item-wrapper-text`</td><td>FWA</td><td>Aeonik 18px/20.7px w400 ls normal</td><td>#f0f1fa / transparent</td><td>706,516 216x21</td></tr>
</table>
*19 more callouts are in the image and in img/about/desktop/legend.json.*

**Driver facts (from the module source)**
- `104_AboutAwardSection`: DOM hooks: `#about-award; #about-award-title; #about-capability; .about-award-header; .about-award-header-svg; .about-award-header-text; .about-award-header-title; .about-a` · Easings: `expoOut x5; backOut x1` · Uniforms: `u_gradientTexture; u_invertRatio; u_radius; u_screenPaintTexture; u_screenPaintTextureSize; u_scrollRatio; u_time`

**Exact CSS (desktop rules, then 812px / 560px overrides)**
```css
#about-award { color: var(--color-off-white); padding: var(--base-padding-y) 0; display: flex; flex-direction: column; justify-content: center; min-height: calc(1250 / 1440 * 150vw); gap: calc(var(--vh, 1vh) * 10); font-size: clamp(0.75rem, 1vw, 1.75rem); --margin-left: 44vw; --width-size: 15vw; }
#about-award-title { visibility: hidden; position: absolute; width: 100vw; top: 0; }
```
*3 more matching rules in lusion_pretty.css.*

**DOM outline (served HTML, 2 levels)**
```
div#about-award.section
  div.about-award-category.award-category-awards
    div.about-award-header
    div.about-award-item  ×7
  div.about-award-category.award-category-articles
    div.about-award-header
    div.about-award-item
  div.about-award-category.award-category-talks
    div.about-award-header
    div.about-award-item
```

## 5. Capabilities (flip cards)  `#about-capability`

![Capabilities (flip cards): desktop frames with numbered callouts, mobile row underneath](../assets/15/about__about-capability.jpg)

**Rebuild spec**
The two-line title (`#about-capability-title-line-1` and `-2`) is split into lines and words. Next is a subheader with a small card, then `#about-capability-cards`, a row of `.about-capability-card` cards. As each card enters, it flips in 3D from 180 to 0 degrees: `fit(screenRatio, -0.85 - (p % 2)/10, 0, 180, 0, ease.cubicInOut)`, so odd and even cards are slightly offset. When cards are activated they flip back with `ease.backInOut`. The CSS 3D transforms are plain DOM, not WebGL.

**Mobile (390 wide):** The cards stack in one column and flip as they scroll in.

**Driven by:** `105_AboutCapabilitySection`. No section-specific shader files (HTML + shared Ufx/post passes). Handbook: [Chapter 10 (CSS, layout and DOM state)](https://shifatmasud.notion.site/3fd48559569d81289d5ff6769e1f1d55).

**Callouts (measured on the live page at capture time)**
<table header-row="true">
<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>
<tr><td>10 · 1</td><td>`div#about-capability`</td><td>AREA OF EXPERTISE MULTIDISCIPLINARY EXPE</td><td>Aeonik 14.4px/16.56px w400 ls normal</td><td>#ffffff / transparent</td><td>0,-18 1440x3871</td></tr>
<tr><td>10 · 2</td><td>`div#about-capability-title-line-1`</td><td>AREA OF</td><td>Aeonik 172.8px/172.8px w400 ls normal</td><td>#ffffff / transparent</td><td>72,277 695x173</td></tr>
<tr><td>10 · 3</td><td>`div#about-capability-title`</td><td>AREA OF EXPERTISE</td><td>Aeonik 172.8px/172.8px w400 ls normal</td><td>#ffffff / transparent</td><td>72,277 1296x346</td></tr>
<tr><td>10 · 4</td><td>`div#about-capability-subheader-text`</td><td>MULTIDISCIPLINARY EXPERTISE ACROSS STRAT</td><td>Aeonik 12.6px/15.12px w400 ls normal uppercase</td><td>#ffffff / transparent</td><td>1116,306 252x45</td></tr>
<tr><td>10 · 5</td><td>`div#about-capability-subheader`</td><td>MULTIDISCIPLINARY EXPERTISE ACROSS STRAT</td><td>Aeonik 12.6px/15.12px w400 ls normal uppercase</td><td>#ffffff / transparent</td><td>1116,306 252x110</td></tr>
<tr><td>10 · 6</td><td>`div#about-capability-subheader-cards`</td><td>S D T 3</td><td>Aeonik 12.6px/15.12px w400 ls normal uppercase</td><td>#ffffff / transparent</td><td>1116,376 137x39</td></tr>
<tr><td>10 · 7</td><td>`div#about-capability-title-line-2`</td><td>EXPERTISE</td><td>Aeonik 172.8px/172.8px w400 ls normal</td><td>#ffffff / transparent</td><td>418,450 846x173</td></tr>
</table>
*24 more callouts are in the image and in img/about/desktop/legend.json.*

**Driver facts (from the module source)**
- `105_AboutCapabilitySection`: DOM hooks: `#about-capability; #about-capability-cards; #about-capability-cards-wrapper; #about-capability-subheader; #about-capability-subheader-text; #about-capability-ti` · Easings: `expoOut x3; lusion x3; backInOut x1; expoInOut x1; cubicInOut x1`

**Exact CSS (desktop rules, then 812px / 560px overrides)**
```css
#about-capability { color: var(--color-white); align-content: flex-start; font-size: clamp(0.875rem, 1vw, 1.75rem); }
#about-capability-title { line-height: 1em; grid-column: 1 / span 12; font-size: 12vw; margin-top: calc(2em - 2 * var(--base-padding-y)); display: flex; flex-direction: column; will-change: transform; }
#about-capability-title > div { grid-column: 1 / span 8; position: relative; }
#about-capability-title #about-capability-title-line-2 { left: 2em; }
#about-capability-subheader { position: absolute; right: var(--base-padding-x); top: var(--base-padding-y); font-size: 0.875em; width: 20em; text-transform: uppercase; line-height: 1.2; margin-top: calc(26vw - 2 * var(--base-padding-y)); }
#about-capability-subheader-text { will-change: transform; }
#about-capability-subheader-cards { display: flex; gap: 0.5rem; width: fit-content; margin-top: 2em; overflow: hidden; position: relative; will-change: transform; }
@media (max-width: 812px) | #about-capability { font-size: clamp(1rem, 1vw, 1.75rem); }
@media (max-width: 812px) | #about-capability-title { grid-column: 1 / span 6; font-size: 18vw; }
@media (max-width: 812px) | #about-capability-title > div { grid-column: 1 / span 12; }
@media (max-width: 812px) | #about-capability-title #about-capability-title-line-2 { left: 0; }
```
*13 more matching rules in lusion_pretty.css.*

**DOM outline (served HTML, 2 levels)**
```
div#about-capability.section
  div#about-capability-title
    div#about-capability-title-line-1
    div#about-capability-title-line-2
  div#about-capability-subheader
    div#about-capability-subheader-text
    div#about-capability-subheader-cards
  div#about-capability-cards-wrapper
    div#about-capability-cards
```
