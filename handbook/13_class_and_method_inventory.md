> **Read in Notion:** [13. Class and method inventory](https://shifatmasud.notion.site/3fd48559569d81709a8ecf7dc5c65d23) · Part of [Lusion.co Decoded: Frontend Handbook](https://shifatmasud.notion.site/3fd48559569d81dd80b4c7407caf27cc) · [Repo home](https://github.com/shifatmasud/lusion-decoded)

# 13. Class and method inventory

## The idea in one sentence

This is the **full API surface of Lusion's own code**: all 130 classes they wrote, grouped by layer, with every method signature exactly as it ships in the bundle, a one-line purpose, and whether that purpose is confirmed by reading the code or inferred from names.

> 📌 **How to read the status column.** Class names, parent classes, module numbers and method signatures are always **confirmed**: they come straight from parsing the bundle (chapter 12.6). The *Purpose* column is **Confirmed** only when the class was read in chapters 5 to 11; otherwise it is **Inferred** from the class name, its methods and where it sits in the bundle. Parameter names like `e, t, r` are minified; default values such as `t=1.5` and `!0` (true) are the real shipped defaults.

## 13.1 Numbers

| Measure | Value |
|---|---|
| Classes in the app part of the bundle | 135 (130 Lusion's own, 5 third-party) |
| Methods, getters and setters | 971 |
| Module files after the split | 141 (the Module column below is the file number, for example 136 = 136\_App.js) |
| Purposes confirmed by reading code | 48 of 130 |
| Biggest single method | App.update, 3,045 bytes |

## 13.2 The family tree

![Class family map: every Lusion class grouped by layer, sized by method count, filled when its purpose is confirmed, with the parent classes that have two or more children.](assets/13/13_family.png)

*Class family map: every Lusion class grouped by layer, sized by method count, filled when its purpose is confirmed, with the parent classes that have two or more children.*

Most of the codebase is a few base classes and many small subclasses that fill in the same lifecycle methods.

```mermaid
classDiagram
  class Page { preInit(e) init(e) show(e,t,r) hide(e,t,r) resize(e,t) update(e) }
  class Stage3D { preInit() init() resize(e,t) syncProperties(e) update(e) }
  class PostEffect { init(e) needsRender() setPostprocessing(e) render(e,t) }
  class ScrollPane { init(e) scrollTo(e,t,r) getDomRange(e,t,r) update(e,t) syncDom() }
  class Ufx
  class UfxMesh { syncDom(e,t) syncRect(e,t,r,n,a,l) testViewport(e,t) update(e,t) }
  Page <|-- HomePage
  Page <|-- ProjectPage
  Page <|-- AboutPage
  Page <|-- ProjectsPage
  Page <|-- PlaygroundPage
  Stage3D <|-- HomeBalloons
  Stage3D <|-- GoalTunnels
  Stage3D <|-- AboutHero
  PostEffect <|-- Smaa
  PostEffect <|-- Bloom
  PostEffect <|-- Final
  PostEffect <|-- Fsr
  PostEffect <|-- ScreenPaintDistortion
  PostEffect <|-- GoalTunnelEfx
  PostEffect <|-- AboutPageHeroEfx
  PostEffect <|-- AboutPageHeroEfxPrepass
  PostEffect <|-- Ufx
  Ufx <|-- PreUfx
  Ufx <|-- PostUfx
  ScrollPane <|-- ScrollManager
  UfxMesh <|-- UfxTextMesh
```

Sections (HomeHeroSection, GoalSection, AboutWhoSection and the rest) do not extend a shared base class in the bundle, but almost all of them repeat the same shape: `preInit(e), init(), resize(e, t), update(e)`, often with `_splitText()` and `_reset()`. That is a convention, not inheritance.

## 13.3 Recurring method names and what they mean

| Method | Meaning across the codebase | Status |
|---|---|---|
| preInit() | Build DOM refs, queue file loads; runs before files are in | Confirmed (boot order, chapter 11.2) |
| init() | Create materials and meshes once files are loaded | Confirmed |
| start() | Go live after GPU warm-up | Confirmed |
| resize(e, t) | Width and height in CSS pixels; recompute layout-dependent values | Confirmed |
| update(e) | Per-frame tick; e is delta time in seconds (capped at 1/20) | Confirmed |
| syncProperties(e) | A scene writes its wanted look into properties before effects read it | Confirmed (App.update, chapter 11.4) |
| syncDom() / syncRect() | Copy a DOM element's rect into a WebGL object, or write transforms back to the DOM | Confirmed for ScrollPane; inferred for UfxMesh and project items |
| needsRender() | A pass returns false to skip itself this frame | Confirmed (Postprocessing filters the queue) |
| show(e, t, r) / hide(e, t, r) | Page or section transition in and out | Confirmed for Page and PageManager |
| \_splitText() / \_reset() | Split headings into lines or letters for reveal animations, then reset them | Inferred |
| \_on\*Load(e) | Loader callbacks for models, textures and animations | Inferred from names |

## 13.4 The inventory, by layer

## Core and utilities

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **MathUtils** | 001 | Scalar math helpers: clamp, mix, fit, smoothstep, hash, bezier | Confirmed | linearStep(e, t, r), step(e, t), clamp(e, t, r), mod(e, t), mix(e, t, r), cMix(e, t, r), unMix(e, t, r), cUnMix(e, t, r), saturate(e), fit(e, t, r, n, a, l), unClampedFit(e, t, r, n, a, l), lerp(e, t, r), loop(e, t, r), normalize(e, t, r), smoothstep(e, t, r), fract(e), hash(e), hash2(e, t), sign(e), isPowerOfTwo(e), powerTwoCeilingBase(e), powerTwoCeiling(e), powerTwoFloorBase(e), powerTwoFloor(e), latLngBearing(e, t, r, n), distanceTo(e, t), distanceSqrTo(e, t), distanceTo3(e, t, r), distanceSqrTo3(e, t, r), latLngDistance(e, t, r, n), cubicBezier(e, t, r, n, a), cubicBezierFn(e, t, r, n), normalizeAngle(e), closestAngleTo(e, t), randomRange(e, t), randomRangeInt(e, t), padZero(e, t), lerpColor(e, t, r), getSeedRandomFn(e) |
| **Browser** | 002 | UA/device flags (isMobile, isSafari...) | Inferred | constructor() |
| **Settings** | 003 | Global config flags (DPR, MOBILE\_WIDTH, UP\_SCALE, paths) | Confirmed | constructor(), override(e) |
| **Properties** | 005 | Shared state bag: renderer, camera, sizes, shared uniforms, tuning values | Confirmed | constructor(), reset() |
| **SecondOrderDynamics** | 007 | Spring (frequency, damping, response) used for most motion | Confirmed | constructor(e, t=1.5, r=.8, n=2, a=!0), update(e, t=0), reset(e=null), \_resetVector(`e=this.target0`), \_resetNumber(`e=this.target0`), setFZR(e=this.\_f, t=this.\_z, r=this.\_r), \_computeStableCoefficients(e), \_computeRobustStableCoefficients(e), \_updateVector(`e, t=this.target`), \_updateNumber(`e, t=this.target`) |
| **Ease** | 015 | Easing curves | Inferred | quadIn(e), quadOut(e), quadOutIn(e), quadInOut(e), cubicIn(e), cubicOut(e), cubicOutIn(e), cubicInOut(e), quartIn(e), quartOut(e), quartOutIn(e), quartInOut(e), quintIn(e), quintOut(e), quintOutIn(e), quintInOut(e), sineIn(e), sineOut(e), sineOutIn(e), sineInOut(e), expoIn(e), expoOut(e), expoOutIn(e), expoInOut(e), circIn(e), circOut(e), circOutIn(e), circInOut(e), elasticIn(e), elasticOut(e), elasticOutIn(e), elasticInOut(e), backIn(e), backOut(e), backOutIn(e), backInOut(e), bounceIn(e), bounceOut(e), bounceOutIn(e), bounceInOut(e), lusion(e), cubicBezier(e, t, r, n, a) |
| **Tween** | 010 | Tiny tween, ticked by Tween.autoUpdate(dt) in the loop | Confirmed | constructor(e, t), static autoUpdate(e), restart(), kill(), to(e, t, r=null), fromTo(e, t, r, n), update(e=0, t=!1) |
| **Simple1DNoise** | 043 | 1D value noise | Inferred | constructor(e), getVal(e), getFbm(e, t), get amplitude(), set amplitude(e), get scale(), set scale(e) |
| **BrownianMotion** | 044 | Noise-driven camera/object drift | Inferred | constructor(), rehash(), update(e), get positionAmplitude(), set positionAmplitude(e), get positionFrequency(), set positionFrequency(e), get rotationAmplitude(), set rotationAmplitude(e), get rotationFrequency(), set rotationFrequency(e), get matrix(), set matrix(e) |
| **DomHelper** | 038 | DOM utility helpers | Inferred | clone(e), \_collapseWhiteSpace(e), getLinesFromText(e), getLinesFromTextNode(e) |
| **Support** | 135 | WebGL/browser support check | Confirmed | isSupported(), checkSupportWebGL() |
| **TextAnimationHelper** | 098 | Text reveal helper | Inferred | setMatrixText(e, t, r=0, n=40, a=2, l=1/15), resetMatrixTextTime(e), updateMatrixText(e, t=properties.deltaTime) |
| **SVGParser** | 102 | Parses SVG paths into geometry | Inferred | parse(e), createShapes(e), getStrokeStyle(e, t, r, n, a), pointsToStroke(e, t, r, n), pointsToStrokeWithBuffers(e, t, r, n, a, l, c, u) |

## Engine, GPU and post-processing

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **App** | 136 | Engine: initEngine, frame update, post queue | Confirmed | initEngine(), preInit(), init(), start(), resize(e, t), preUpdate(e=0), update(e=0) |
| **FboHelper** | 011 | Render targets, blits, shader material factory | Confirmed | init(e, t), copy(e, t), uvCopy(e, t), render(e, t), renderGeometry(e, t, r), renderMesh(e, t, r=this.\_camera), debugTo(e, t, r, n, a), parseDefines(e), clearColor(e, t, r, n, a), getColorState(), setColorState(e), createRawShaderMaterial(e), createDataTexture(e, t, r, n=!1, a=!0), createRenderTarget(e, t, r=!1, n=!1, a=0), createMultisampleRenderTarget(e, t, r=!1, n=!1, a=8), clearMultisampleRenderTargetState(e) |
| **ShaderHelper** | 018 | Registers reusable GLSL chunks (#include) | Confirmed | glslifyStrip(e), addChunk(e, t), \_wrapInclude(e), insertBefore(e, t, r, n), insertAfter(e, t, r, n), replace(e, t, r, n) |
| **TextureHelper** | 042 | Texture utilities, channel mixer | Inferred | init(), \_createPixelTexture(e), mixChannels(e, t, r=-1, n=-1, a=-1, l=-1) |
| **BlueNoise** | 019 | Blue-noise texture + shared GLSL chunk | Confirmed | preInit(), update(e) |
| **Blur** | 017 | Separable 9-tap blur pass | Confirmed | getBlur9Material(), blur(e, t, r, n, a, l) |
| **Task** | 012 | One unit of deferred GPU work (compile, init texture) | Confirmed | constructor(e), get isCompleted(), run(), createMultiCallbackFunc(e), \_onComplete(), createCallbackFunc(e), createShaderMaterialFunc(e), createCompileSceneFunc(e), createInitTextureFunc(e) |
| **TaskManager** | 013 | Runs Tasks a few per frame; feeds preloader % | Confirmed | start(), \_start(), add(e), update() |
| **Stage3D** extends Scene | 016 | Base 3D scene (extends three.js Scene) with lifecycle hooks | Confirmed | constructor(e={}), preInit(), init(), resize(e, t), syncProperties(e), update(e) |
| **Visuals** | 025 | Holds all Stage3D scenes; picks currentStage3D | Confirmed | preInit(), init(), start(), resize(e, t), deactivateAll(), syncProperties(e), update(e) |
| **PostEffect** | 045 | Base post-processing pass (render, needsRender) | Confirmed | init(e), needsRender(), warn(e), setPostprocessing(e), render(e, t=!1) |
| **Postprocessing** | 122 | Sorted pass queue, ping-pong targets | Confirmed | init(e), swap(), setSize(e, t), dispose(), \_filterQueue(e), renderMaterial(e, t), checkSceneRt(), render(e, t, r) |
| **Smaa** extends PostEffect | 123 | SMAA anti-aliasing, priority 500 | Confirmed | init(e), setTextures(e, t), updateTextures(), setPostprocessing(e), dispose(), needsRender(), render(e, t), \_createTexture(e) |
| **Bloom** extends PostEffect | 124 | Bloom (convolution on desktop, blur on mobile) | Confirmed | init(e), setDirtTexture(e), setPostprocessing(e), dispose(), needsRender(), renderFFT(e, t, r), render(e, t=!1) |
| **ScreenPaintDistortion** extends PostEffect | 125 | Mouse distortion pass, priority 75 | Confirmed | init(e), needsRender(e), syncCamera(e), render(e, t=!1) |
| **Final** extends PostEffect | 126 | Colour grading/vignette, priority 30 | Confirmed | init(e), needsRender(), render(e, t=!1) |
| **Fsr** extends PostEffect | 127 | FSR upscaler, priority 2000 (the last pass) | Confirmed | init(e), render(e, t=!1) |
| **Ufx** extends PostEffect | 053 | Base for DOM-synced UI effects pass | Confirmed | init(), setPostprocessing(e), render(e, t=!1) |
| **PreUfx** extends Ufx | 054 | UI effects pass, priority 50 | Confirmed | (fields only) |
| **PostUfx** extends Ufx | 103 | Top-layer UI effects pass, priority 100 | Confirmed | (fields only) |
| **UfxMesh** extends Mesh | 032 | Mesh that draws a DOM-aligned UI effect quad | Inferred | constructor(e={}), \_onBeforeRender(), \_initMaterial(e), syncDom(e=0, t=0), syncRect(e, t, r, n, a=0, l=0), testViewport(e=0, t=0), update(e=0, t=0) |
| **UfxTextMesh** extends UfxMesh | 071 | Text variant of UfxMesh | Inferred | constructor(e={}), syncText() |
| **GlPositionOffset** | 134 | Shared vertex offset chunk | Inferred | init(), setOffset(e, t) |
| **(anonymous class)** | 126 | Unnamed helper class in the Final module | Inferred | constructor(), render(e, t) |
| **CameraControls** | 050 | Camera rig: orbit/device orientation, look offset | Inferred | preInit(e), init(), resize(e, t), update(e) |
| **ScreenPaint** | 020 | Paints pointer motion into a GPU velocity texture | Confirmed | init(), resize(e, t), update(e) |

## Input, scroll and motion

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **Input** | 008 | Unified wheel/touch/mouse input, eased pointer values | Confirmed | preInit(), init(), resize(), update(e), addEasedInput(e, t=1.5, r=.8, n=2), postUpdate(e), \_onWheel(e), \_onDown(e), \_onMove(e), \_onUp(e), \_getTouchBound(e, t, r), \_getInputXY(e, t), \_getInputPixelXY(e, t), \_setThroughElementsByEvent(e, t), hasThroughElem(e, t), hasThroughElemWithClass(e, t) |
| **ScrollDomRange** | 009 | Tracks one element's on-screen range vs scroll | Confirmed | constructor(e, t), update(e, t, r, n) |
| **ScrollPane** | 120 | Custom scroll: easing, fling, one transform per frame | Confirmed | init(e={}), \_onResizeObserve(), getDomRange(e, t=0, r=!1), scrollTo(e, t=0, r=!1), scrollToPixel(e=0, t=!1), getEaseInOutOffset(e, t, r=0, n=.5), resize(e, t), \_clampScrollPixel(e), resetScroll(e), update(e, t), syncDom(), get isMoveable() |
| **ScrollManager** extends ScrollPane | 121 | Main page ScrollPane | Confirmed | init(), resize(e, t), update(e), get isMoveable() |

## Loading

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **BufItem** extends XHRItem | 128 | Loads custom .buf binary meshes | Confirmed | constructor(e, t), retrieve(), \_onLoad() |
| **EXRItem** extends AnyItem | 131 | Loads EXR HDR textures | Confirmed | constructor(e, t), retrieve(), \_onLoad(e), loadFunc(), \_onGLTFLoading(e) |
| **TextureItem** extends ImageItem | 132 | Loads textures | Confirmed | constructor(e, t), retrieve(), load(), \_onLoad() |
| **ThreeLoaderItem** extends AnyItem | 133 | Wraps three.js loaders | Confirmed | constructor(e, t), \_loadFunc(e, t, r), \_onLoaderLoad(e, t), \_onLoaderLoading(e, t) |
| **FontItem** extends AnyItem | 140 | Loads web fonts | Confirmed | constructor(e, t), static initDom(), \_loadFunc(e, t, r), \_onLoaderLoad(e, t), \_onLoaderLoading(e, t) |
| **Preloader** | 137 | Preloader counter and timing | Confirmed | preInit(), init(), show(e, t), hide(), resize(e, t, r), update(e) |

The loader item base classes (AnyItem, XHRItem, ImageItem) live inside the QuickLoader module as functions, not top-level classes, so they are not rows here (chapter 9).

## Routing, pages and UI

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **Route** | 067 | One route: path, title, target page | Confirmed | constructor(e), setTitleDom(e, t, r, n), setTarget(e) |
| **RouteManager** | 068 | Custom router: prefetch on hover, history, link capture | Confirmed | get currRoute(), init(), addPath(e, t), \_createRoute(e), \_fetchHtml(e), \_initDom(e, t), \_attachEvents(e), \_onRegularLinkClick(e, t), \_onInternalLinkClick(e, t), \_onDomReady(e), parseUrl(e=loc.href), parsePath(e), setUrl(e=loc.href), setPath(e), preFetch(e), \_onStatePop(e) |
| **PageManager** | 119 | Runs page switch steps: hide, load, show | Confirmed | constructor(), preInit(), get isIdle(), \_onRouteChanged(e), \_onShowTextComplete(), \_onHideTextComplete(), \_onTaskComplete(), init(), \_initPage(), \_onHideComplete(), resize(e, t), start(), \_showPage(), \_onShowComplete(), update(e), \_log(e) |
| **TransitionOverlay** | 118 | Canvas overlay for page transitions | Confirmed | init(), resize(e, t), isReadyToHide(), get activeRatio(), update(e) |
| **Page** | 014 | Base page: preInit/init/show/hide/resize/update | Confirmed | constructor(), get activeRatio(), hasProject(e), get isScrollTarget(), preInit(e), preInitContent(e), init(e), initContent(e), show(e, t, r), hide(e, t, r), resize(e, t), update(e) |
| **HomePage** extends Page | 078 | Home page (extends Page) | Confirmed | preInit(), init(), hasProject(e), show(e, t, r), hide(e, t, r), resize(e, t), update(e) |
| **ProjectPage** extends Page | 076 | Project page | Inferred | preInit(), preInitContent(e), init(), show(e, t, r), hide(e, t, r), resize(e, t), update(e), \_onContentShowComplete(), \_onNextProjectComplete() |
| **AboutPage** extends Page | 107 | About page | Inferred | preInit(), init(), resize(e, t), show(e, t, r), update(e) |
| **ProjectsPage** extends Page | 110 | Projects page | Inferred | preInit(), init(), hasProject(e), show(e, t, r), hide(e, t, r), resize(e, t), update(e) |
| **PlaygroundPage** extends Page | 112 | Playground page | Inferred | preInit(), init(), resize(e, t), update(e), \_onTunnelLoad(e), \_onDomTimelineClick(e), \_onDomDotMouseenter(e), \_onDomDotMouseleave(e) |
| **UI** | 139 | UI root: preload, init, start | Confirmed | preInit(), preload(e, t), init(), start(), resize(e, t, r), update(e) |
| **Header** | 069 | Header UI, recolours per background | Confirmed | preInit(), init(), show(), hideTalkBtn(), changeSection(e), \_onDomRightSoundBtn(), \_onRouteChanged(), \_domRightMenuBtnClick(), \_onDomMenuLinkContact(), \_enableMenu(e), \_domRightMenuListMouseenter(), \_domRightMenuListMouseleave(), \_onWindowClick(e), \_onPageScrollTargetChange(e), resize(e, t), updateSoundWave(e), update(e), \_hexToRgb(e) |
| **Links** | 138 | Link hover effects | Inferred | preInit(), init(), resize(), update(e), \_onLinkMouseenter(e), \_onLinkMouseleave(e) |
| **PageExtraSections** | 117 | Shared extra sections per page | Inferred | preInit(), init(), resize(e, t), update(e) |
| **EndSection** | 115 | Scroll-to-next-page end section | Confirmed | preInit(), init(), resize(e, t), update(e), \_splitText(), \_reset(), \_onDomTitleMouseenter(), \_onDomTitleMouseleave() |
| **ScrollNavSection** | 116 | Scroll nav section | Inferred | preInit(), init(), resize(e, t), update(e) |
| **FooterSection** | 058 | Footer section | Inferred | preInit(), init(), resize(e, t), getDomRange(), update(e), \_splitText(), \_createWrapper(e, t), \_reset(), \_onDomUpBtnClick() |
| **NewletterForm** | 057 | Newsletter form logic (name spelled this way in the bundle) | Inferred | constructor(e, t, r), \_onFormSubmit(e) |
| **VideoOverlay** | 036 | Fullscreen video player overlay (Vimeo) | Inferred | preInit(), initAndPlayVideo(e=VIDEO\_LIST.MAIN\_VIDEO\_REEL, t=!1), init(), resize(), update(e), open(), close() |

## Audio

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **Audios** | 030 | Audio system root, ticked in App.update | Confirmed | preInit(), \_parseCountText(e), init(), on(), off(), toggle(), pause(), resume(), getListener(e), \_onBodyClick(), addHoverClickEvents(e), addHoverEvent(e, t="hover"), addClickEvent(e, t="click"), countPlay(e), fadeBgMusic(e, t=1, r=void0), update(e) |
| **AudioGroup** | 027 | Groups audio items | Inferred | init(e), update(e), add(e), remove(e), play(), stop() |
| **AudioItem** | 028 | One sound with volume/fade | Inferred | preInit(e), init(e), load(e), setFinalVolume(e), activateFilter(), deactivateFilter(), setFilterFrequency(e=MAX\_FREQ), setFilterFrequencyViaRatio(e=1), setPositionObjectParent(e), decodeAudioData(), onEnd(), play(), stop(), setRefDistance(e), setFadeIn(e=1), setFadeOut(e=1), update(e) |
| **GlobalAudios** | 029 | Site-wide sounds (UI, ambience) | Inferred | constructor(), init(), update() |
| **HomePageAudios** | 077 | Home page sounds | Inferred | constructor(), init(), update() |
| **ProjectPageAudios** | 075 | Project page sounds | Inferred | constructor(), init(), update() |
| **AboutPageAudios** | 106 | About page sounds | Inferred | constructor(), init(), update(e) |
| **ProjectsPageAudios** | 109 | Projects page sounds | Inferred | constructor(), init(), update() |

## Site sections and scenes (home, about, projects, playground)

| Class | Module | Purpose | Purpose status | Methods (signatures as shipped) |
|---|---|---|---|---|
| **HomeBalloonsBackground** | 021 | Backdrop behind hero balloons | Inferred | constructor(), preInit(), init(), resize(e, t), update(e) |
| **HomeBalloonsBody** | 022 | Per-balloon body state | Inferred | constructor(e=1, t=1, r=.5, n=.5, a=!1), reset(), applyImpulse(), updateGravity(e), update(e) |
| **HomeBalloonsPhysics** | 023 | Hand-written balloon physics | Confirmed | initWorld(), reset(), update(e) |
| **HomeBalloons** extends Stage3D | 024 | Hero balloons scene: physics, sorting, glass lighting | Confirmed | constructor(), preInit(), init(), onBeforeRenderFront(), onBeforeRenderBack(), resize(e, t), \_sortDist2(e, t), \_sortMeshDist2(e, t), syncProperties(e), updateColor(), updateUniforms(), updateSorting(), updateRenderOrder(), updateTransformations(), update(e) |
| **HomeHeroSection** | 031 | Home hero DOM section | Inferred | preInit(e), init(), initEvent(), resize(e, t), \_updateUi(e), \_onWheel(), update(e), hide(), \_reset() |
| **Line** | 033 | Animated line mesh | Inferred | constructor(e=0), preInit(), init(), resize(e, t), update(e, t, r=0) |
| **HomeReelSection** | 037 | Home showreel section | Inferred | preInit(e), init(), \_onPageHideStarted(), resize(e, t), update(e), \_updateUI(e, t, r), \_onDomVideoButtonClick(), \_onDomVideoButtonMouseenter(), \_onDomVideoButtonMouseleave(), \_onVideoMeshMouseEnter(), \_onVideoMeshMouseLeave(), \_splitText(), \_reset() |
| **ProjectItem** | 039 | One project card (DOM + WebGL) | Inferred | constructor(e, t, r, n), \_onMouseEnter(), \_onMouseLeave(), syncDom(), \_findIndexFromThresholds(e), update(e), preloadImage() |
| **ProjectItemList** | 040 | List of project cards | Inferred | constructor(e, t), hasProject(e), getProjectItemTop(e), \_onDomItemMouseEnter(e), \_onDomItemMouseLeave(e), update(e) |
| **HomeFeaturedSection** | 041 | Featured projects section | Inferred | preInit(e), init(), resize(e, t), update(e), \_reset(), \_splitText() |
| **GoalTunnelEfx** extends PostEffect | 046 | Post pass for the tunnel section | Inferred | init(e), needsRender(e), syncCamera(e), render(e, t=!1) |
| **GoalBlackTunnel** | 047 | Black tunnel mesh | Inferred | preInit(), \_onGeometryLoad(e, t, r), \_onAfterRender(), \_onGreebleTextureLoad(e, t), init(), resize(e, t), update(e) |
| **GoalTunnelAstronauts** | 051 | Astronaut figures in the tunnel | Inferred | preInit(), \_initLedTexture(), initGui(), \_onTextureLoad(e, t, r), \_onGeometryLoad(e, t, r), \_onBeforeRender(e, t, r), \_onAfterRender(e, t, r), \_onAnimationLoad(e), init(), resize(e, t), updateTransforms(e), updateAnimation(e), updateCard(e), update(e) |
| **GoalWhiteTunnel** | 052 | White tunnel mesh | Inferred | preInit(), \_onTunnelBlockLoad(e, t), init(), resize(e, t), update(e) |
| **GoalTunnelGlass** | 055 | Glass in the tunnel | Inferred | preInit(), \_onModelLoad(e), \_onBeforeRender(e, t, r), \_onAfterRender(e, t, r), \_onAnimationLoad(e), init(), resize(e, t), update(e) |
| **GoalSectionRanges** | 059 | Scroll ranges for the goal section | Inferred | init(e), resize(e, t), update(e), getRange(e, t=e) |
| **GoalTunnelsBackground** | 060 | Tunnel background | Inferred | constructor(), preInit(), init(), resize(e, t), update(e) |
| **GoalWhiteTunnelParticles** | 061 | Tunnel particles | Inferred | constructor(), preInit(), init(), resize(e, t), update(e) |
| **GoalWhiteTunnelStickers** | 062 | Tunnel stickers | Inferred | preInit(), init(), resize(e, t), update(e) |
| **GoalTunnels** extends Stage3D | 063 | Tunnel scene (Stage3D) | Inferred | constructor(), preInit(), init(), resize(e, t), updateRatios(), syncProperties(e), resetAstronautLayer(), update(e) |
| **HomeGoalSectionTunnelTitle** | 064 | Title over the tunnel | Inferred | init(e), resize(e, t), \_resetWords(), update(e) |
| **GoalSection** | 065 | Home goal/tunnel section | Inferred | preInit(e), init(), show(), hide(), resize(e, t), update(e), \_splitText(), \_reset() |
| **ProjectDetailsScreen** | 066 | Project details WebGL screen | Inferred | preInit(e), init(), \_onPlantMeshRender(e), resize(), update(e) |
| **ProjectDetailsData** | 070 | Project detail data | Inferred | constructor(e, t) |
| **ProjectDetailsItem** | 072 | One project detail block | Inferred | constructor(e="image"), activate(e), deactivate(), \_initVideo(), \_initImage(), \_initText(), \_onMouseEnter(), \_onMouseLeave(), \_onClick(), resize(e, t, r), syncDom(), playPauseVideo(e), update(e) |
| **ProjectDetailsItems** | 073 | List of detail blocks | Inferred | useItem(e), deactivateAll(), pauseAllVideos(), resizeAll(e, t, r), syncDoms(), update(e, t, r) |
| **ProjectDetailsSection** | 074 | Project page details section | Inferred | preInit(e), preInitContent(e), \_onModelLoad(e), init(), show(e), updatePreviewUI(e, t=!0), \_disposeLayout(), \_initLayout(e), \_onBackBtnClick(), \_splitText(), hide(e, t, r), resize(e, t), update(e, t=!1), \_onWindowWheel() |
| **AboutHeroLight** | 079 | About hero light | Inferred | preInit(), init(), update(e), renderMesh(e), postUpdate(e) |
| **AboutHeroLightField** | 080 | About hero light field | Inferred | preInit(), init(), update(e), renderMesh(e), postUpdate(e) |
| **AboutHeroParticlesSimulation** | 081 | GPU particle simulation | Inferred | preInit(), init(), update(e) |
| **AboutHeroScatter** | 082 | Scatter helper | Inferred | constructor(), init(), update(e) |
| **AboutPageHeroEfxPrepass** extends PostEffect | 083 | About hero pre-pass effect | Inferred | init(e), needsRender(), setPostprocessing(e), renderMotion(e, t, r, n), render(e, t=!1) |
| **AboutHeroParticles** | 084 | About hero particles | Inferred | preInit(), \_onGeometryLoad(e, t), init(), update(e) |
| **AboutHeroRocks** | 085 | Rocks | Inferred | preInit(), loadRock(e), \_onRockLoad(e, t, r), \_onRockAnimationLoad(e, t), init(), update(e) |
| **AboutHeroGround** | 086 | Ground | Inferred | preInit(), init(), update(e) |
| **AboutHeroLines** | 087 | Lines | Inferred | preInit(), \_onLineLoad(e), init(), update(e) |
| **aboutHeroPerson** | 088 | Person figure | Inferred | preInit(), \_onTextureLoad(), \_onModelLoad(e), \_onAnimationLoad(e), init(), update(e) |
| **AboutHeroFog** | 089 | Fog | Inferred | preInit(), init(), onBeforeRender(), resize(e, t), update(e) |
| **AboutHeroHalo** | 090 | Halo | Inferred | preInit(), \_onGeometryLoad(e), init(), resize(e, t), update(e) |
| **AboutHeroFaces** | 091 | Faces | Inferred | preInit(), load(e), \_onModelLoaded(e, t), init(), resize(e, t), update(e) |
| **AboutPageHeroEfx** extends PostEffect | 092 | About hero post effect | Inferred | init(e), needsRender(), render(e, t=!1) |
| **AboutHeroLetters** | 093 | 3D letters | Inferred | preInit(), \_onGeometryLoad(e), init(), \_onBeforeRender(), update(e) |
| **AboutHero** extends Stage3D | 094 | About hero scene (Stage3D) | Inferred | constructor(), preInit(), init(), resize(e, t), syncProperties(e), update(e) |
| **AboutWhoLogo** | 095 | Logo in Who section | Inferred | preInit(e), \_onGeometryLoad(e), init(), resize(e, t), update(e, t, r, n, a) |
| **WhoSubsectionWeAre** | 096 | Who: we are | Inferred | preInit(e), init(), show(), hide(), resize(e, t), update(e, t, r, n, a) |
| **WhoSubsectionDetails** | 097 | Who: details | Inferred | preInit(e), \_parseDomText(e), init(), show(), hide(), resize(e, t), update(e, t, r) |
| **WhoSubsectionTeam** | 099 | Who: team | Inferred | preInit(e), init(), onPageShow(), prev(), next(), \_clearTween(), updateTeamNumberUI(), onTweenComplete(), reset(), resize(e, t), \_updateRect(e, t, r), \_changeFaceUIByIndex(e), \_createUIElements(), syncContainerOffset(), \_splitText(), preUpdate(), onSwipe(), update(e, t, r, n, a, l) |
| **AboutWhoSection** | 100 | About who section | Inferred | preInit(e), init(), resize(e, t), show(), getMoveRatio(), getScrollRatio(), syncSubsectionContainerTransform(), update(e) |
| **AboutClientSection** | 101 | Clients section | Inferred | preInit(e), init(), resize(e, t), update(e), \_createCarousel(), \_splitText(), \_reset() |
| **AboutAwardSection** | 104 | Awards section | Inferred | preInit(e), \_generateEdgeIndices(e), init(), show(), hide(), resize(e, t), update(e), \_splitText(), \_reset() |
| **AboutCapabilitySection** | 105 | Capabilities section | Inferred | preInit(e), init(), resize(e, t), update(e), \_splitText(), \_reset() |
| **ProjectsMainSection** | 108 | Projects list section | Inferred | preInit(e), init(), hasProject(e), resize(e, t), update(e), \_reset(), \_splitText() |
| **FlipSim** | 113 | FLIP fluid/particle simulation (name) | Inferred | constructor(), init(e, t, r, n, a, l), integrateParticles(e, t), pushParticlesApart(e), handleParticleCollisions(e, t, r, n, a, l), updateParticleDensity(), transferVelocities(e, t), solveIncompressibility(e, t, r, n=!0), resetParticles(), simulate(e, t, r, n, a, l, c, u, f, p, g, v, \_) |
| **FlipAnimation** | 114 | Animation driven by FlipSim | Inferred | preInit(), init(), reInitTank(), resize(), convertDomRectToTankRect(e), convertPixelSizeToTankSize(e, t), convertPixelXYToTankXY(e, t), update(e) |

## Third-party classes inside the app range

| Class | Library | Used for | Status |
|---|---|---|---|
| Player, TimingSrcConnector extends EventTarget | Vimeo Player | The showreel and project videos (VideoOverlay) | Library confirmed; usage inferred from VideoOverlay |
| OrbitControls extends EventDispatcher | three.js examples | Camera control helper, likely debug or CameraControls | Inferred |
| DeviceOrientationControls | three.js examples | Tilt-to-look on phones | Inferred |
| EXRLoader extends DataTextureLoader | three.js examples | HDR textures through EXRItem | Confirmed (EXRItem) |

## 13.5 The raw inventory file

The full machine output, including class fields with their initial values and the byte size of every method, is attached here. Search it for any name; the byte offsets point back into the original bundle.

Download: [lusion_class_inventory.txt](../analysis/class_inventory.txt) (in this repo as `analysis/class_inventory.txt`)

## 13.6 How to reuse this

- **Steal the vocabulary, not the code.** The method names are a ready-made API design: `preInit / init / start / resize / update / syncProperties / needsRender / syncDom`. Use the same names in your own engine and every module becomes predictable.
- **Keep base classes few.** Lusion has about five real bases (Page, Stage3D, PostEffect, ScrollPane, UfxMesh). Everything else is a convention. That keeps inheritance shallow and easy to read.
- **Size tells priority.** When you study any bundle, sort methods by byte size and read the top 20 first.

## 13.7 Original example (not Lusion's code)

The recurring signatures written as TypeScript contracts, so your own modules (or Shade DSL output) can be checked by the compiler:

```typescript
export interface Module {
  preInit?(): void;                 // DOM refs, queue loads
  init?(): void;                    // build once assets are ready
  start?(): void;                   // go live after GPU warm-up
  resize?(w: number, h: number): void;
  update?(dt: number): void;        // dt in seconds, capped
}

export interface Page extends Module {
  readonly activeRatio: number;     // 0 hidden .. 1 fully shown
  show(from?: string, done?: () => void): void;
  hide(to?: string, done?: () => void): void;
}

export interface Stage extends Module {
  syncProperties(dt: number): void; // write wanted look into the blackboard
}

export interface PostPass {
  priority: number;                 // lower runs first
  needsRender(): boolean;           // false = skip this frame
  render(input: WebGLTexture, toScreen: boolean): WebGLTexture | null;
}

export interface DomSynced {
  syncDom(scrollY: number): void;   // read element rect, place GPU object
}
```

## 13.8 Confirmed vs inferred

| Point | Status | Evidence |
|---|---|---|
| Class names, parents, module numbers and method signatures | Confirmed | AST parse of the bundle (methods.mjs), class\_inventory.txt |
| 135 classes, 971 methods, 5 third-party | Confirmed | class\_inventory.txt |
| Purposes marked Confirmed (48 classes) | Confirmed | Read in chapters 5 to 11 |
| Purposes marked Inferred (82 classes) | Inferred | Class and method names and bundle position; not read line by line |
| Sections follow a shared shape without a shared base class | Confirmed for the shape | Signatures in the tables above |
| Third-party usage (OrbitControls, DeviceOrientationControls) | Inferred | Present in the bundle; call sites not traced |
