import re,csv
txt=open('class_inventory.txt').read()
idx={}
for l in open('modules/INDEX.tsv'):
    n,s,ln=l.strip().split('\t'); idx[n]=(int(s),int(s)+int(ln))
def module_of(b):
    for n,(s,e) in idx.items():
        if s<=b<e and not n.startswith('00_'): return n.split('_',1)[0]
    return '?'
P={ # purpose, status C=confirmed in ch5-10 reading, I=inferred from name/methods
'MathUtils':('Scalar math helpers: clamp, mix, fit, smoothstep, hash, bezier','C'),
'Browser':('UA/device flags (isMobile, isSafari...)','I'),
'Settings':('Global config flags (DPR, MOBILE_WIDTH, UP_SCALE, paths)','C'),
'Properties':('Shared state bag: renderer, camera, sizes, shared uniforms, tuning values','C'),
'SecondOrderDynamics':('Spring (frequency, damping, response) used for most motion','C'),
'Input':('Unified wheel/touch/mouse input, eased pointer values','C'),
'ScrollDomRange':('Tracks one element\'s on-screen range vs scroll','C'),
'Tween':('Tiny tween, ticked by Tween.autoUpdate(dt) in the loop','C'),
'FboHelper':('Render targets, blits, shader material factory','C'),
'Task':('One unit of deferred GPU work (compile, init texture)','C'),
'TaskManager':('Runs Tasks a few per frame; feeds preloader %','C'),
'Page':('Base page: preInit/init/show/hide/resize/update','C'),
'Ease':('Easing curves','I'),
'Stage3D':('Base 3D scene (extends three.js Scene) with lifecycle hooks','C'),
'Blur':('Separable 9-tap blur pass','C'),
'ShaderHelper':('Registers reusable GLSL chunks (#include)','C'),
'BlueNoise':('Blue-noise texture + shared GLSL chunk','C'),
'ScreenPaint':('Paints pointer motion into a GPU velocity texture','C'),
'HomeBalloonsBackground':('Backdrop behind hero balloons','I'),
'HomeBalloonsBody':('Per-balloon body state','I'),
'HomeBalloonsPhysics':('Hand-written balloon physics','C'),
'HomeBalloons':('Hero balloons scene: physics, sorting, glass lighting','C'),
'Visuals':('Holds all Stage3D scenes; picks currentStage3D','C'),
'AudioGroup':('Groups audio items','I'),'AudioItem':('One sound with volume/fade','I'),
'GlobalAudios':('Site-wide sounds (UI, ambience)','I'),'Audios':('Audio system root, ticked in App.update','C'),
'HomeHeroSection':('Home hero DOM section','I'),
'UfxMesh':('Mesh that draws a DOM-aligned UI effect quad','I'),
'Line':('Animated line mesh','I'),
'VideoOverlay':('Fullscreen video player overlay (Vimeo)','I'),
'HomeReelSection':('Home showreel section','I'),
'DomHelper':('DOM utility helpers','I'),
'ProjectItem':('One project card (DOM + WebGL)','I'),'ProjectItemList':('List of project cards','I'),
'HomeFeaturedSection':('Featured projects section','I'),
'TextureHelper':('Texture utilities, channel mixer','I'),
'Simple1DNoise':('1D value noise','I'),'BrownianMotion':('Noise-driven camera/object drift','I'),
'PostEffect':('Base post-processing pass (render, needsRender)','C'),
'GoalTunnelEfx':('Post pass for the tunnel section','I'),
'GoalBlackTunnel':('Black tunnel mesh','I'),
'CameraControls':('Camera rig: orbit/device orientation, look offset','I'),
'GoalTunnelAstronauts':('Astronaut figures in the tunnel','I'),
'GoalWhiteTunnel':('White tunnel mesh','I'),
'Ufx':('Base for DOM-synced UI effects pass','C'),'PreUfx':('UI effects pass, priority 50','C'),
'GoalTunnelGlass':('Glass in the tunnel','I'),
'NewletterForm':('Newsletter form logic','I'),'FooterSection':('Footer section','I'),
'GoalSectionRanges':('Scroll ranges for the goal section','I'),
'GoalTunnelsBackground':('Tunnel background','I'),'GoalWhiteTunnelParticles':('Tunnel particles','I'),
'GoalWhiteTunnelStickers':('Tunnel stickers','I'),'GoalTunnels':('Tunnel scene (Stage3D)','I'),
'HomeGoalSectionTunnelTitle':('Title over the tunnel','I'),'GoalSection':('Home goal/tunnel section','I'),
'ProjectDetailsScreen':('Project details WebGL screen','I'),
'Route':('One route: path, title, target page','C'),
'RouteManager':('Custom router: prefetch on hover, history, link capture','C'),
'Header':('Header UI, recolours per background','C'),
'ProjectDetailsData':('Project detail data','I'),'UfxTextMesh':('Text variant of UfxMesh','I'),
'ProjectDetailsItem':('One project detail block','I'),'ProjectDetailsItems':('List of detail blocks','I'),
'ProjectDetailsSection':('Project page details section','I'),'ProjectPageAudios':('Project page sounds','I'),
'ProjectPage':('Project page','I'),'HomePageAudios':('Home page sounds','I'),
'HomePage':('Home page (extends Page)','C'),
'AboutHeroLight':('About hero light','I'),'AboutHeroLightField':('About hero light field','I'),
'AboutHeroParticlesSimulation':('GPU particle simulation','I'),'AboutHeroScatter':('Scatter helper','I'),
'AboutPageHeroEfxPrepass':('About hero pre-pass effect','I'),'AboutHeroParticles':('About hero particles','I'),
'AboutHeroRocks':('Rocks','I'),'AboutHeroGround':('Ground','I'),'AboutHeroLines':('Lines','I'),
'aboutHeroPerson':('Person figure','I'),'AboutHeroFog':('Fog','I'),'AboutHeroHalo':('Halo','I'),
'AboutHeroFaces':('Faces','I'),'AboutPageHeroEfx':('About hero post effect','I'),
'AboutHeroLetters':('3D letters','I'),'AboutHero':('About hero scene (Stage3D)','I'),
'AboutWhoLogo':('Logo in Who section','I'),'WhoSubsectionWeAre':('Who: we are','I'),
'WhoSubsectionDetails':('Who: details','I'),'TextAnimationHelper':('Text reveal helper','I'),
'WhoSubsectionTeam':('Who: team','I'),'AboutWhoSection':('About who section','I'),
'AboutClientSection':('Clients section','I'),'SVGParser':('Parses SVG paths into geometry','I'),
'PostUfx':('Top-layer UI effects pass, priority 100','C'),
'AboutAwardSection':('Awards section','I'),'AboutCapabilitySection':('Capabilities section','I'),
'AboutPageAudios':('About page sounds','I'),'AboutPage':('About page','I'),
'ProjectsMainSection':('Projects list section','I'),'ProjectsPageAudios':('Projects page sounds','I'),
'ProjectsPage':('Projects page','I'),'PlaygroundPage':('Playground page','I'),
'FlipSim':('FLIP fluid/particle simulation (name)','I'),'FlipAnimation':('Animation driven by FlipSim','I'),
'EndSection':('Scroll-to-next-page end section','C'),'ScrollNavSection':('Scroll nav section','I'),
'PageExtraSections':('Shared extra sections per page','I'),
'TransitionOverlay':('Canvas overlay for page transitions','C'),
'PageManager':('Runs page switch steps: hide, load, show','C'),
'ScrollPane':('Custom scroll: easing, fling, one transform per frame','C'),
'ScrollManager':('Main page ScrollPane','C'),
'Postprocessing':('Sorted pass queue, ping-pong targets','C'),
'Smaa':('SMAA anti-aliasing, priority 500','C'),'Bloom':('Bloom (convolution on desktop, blur on mobile)','C'),
'ScreenPaintDistortion':('Mouse distortion pass, priority 75','C'),'Final':('Colour grading/vignette, priority 30','C'),
'(anon)':('Anonymous class (unnamed in bundle)','I'),'Fsr':('FSR upscaler, priority 2','C'),
'BufItem':('Loads custom .buf binary meshes','C'),'EXRItem':('Loads EXR HDR textures','C'),
'TextureItem':('Loads textures','C'),'ThreeLoaderItem':('Wraps three.js loaders','C'),
'GlPositionOffset':('Shared vertex offset chunk','I'),'Support':('WebGL/browser support check','C'),
'App':('Engine: initEngine, frame update, post queue','C'),'Preloader':('Preloader counter and timing','C'),
'Links':('Link hover effects','I'),'UI':('UI root: preload, init, start','C'),'FontItem':('Loads web fonts','C'),
}
G=[('Core and utilities',['MathUtils','Browser','Settings','Properties','SecondOrderDynamics','Ease','Tween','Simple1DNoise','BrownianMotion','DomHelper','Support','TextAnimationHelper','SVGParser']),
('Engine, GPU and post-processing',['App','FboHelper','ShaderHelper','TextureHelper','BlueNoise','Blur','Task','TaskManager','Stage3D','Visuals','PostEffect','Postprocessing','Smaa','Bloom','ScreenPaintDistortion','Final','Fsr','Ufx','PreUfx','PostUfx','UfxMesh','UfxTextMesh','GlPositionOffset','(anon)','CameraControls','ScreenPaint']),
('Input, scroll and motion',['Input','ScrollDomRange','ScrollPane','ScrollManager']),
('Loading',['BufItem','EXRItem','TextureItem','ThreeLoaderItem','FontItem','Preloader']),
('Routing, pages and UI',['Route','RouteManager','PageManager','TransitionOverlay','Page','HomePage','ProjectPage','AboutPage','ProjectsPage','PlaygroundPage','UI','Header','Links','PageExtraSections','EndSection','ScrollNavSection','FooterSection','NewletterForm','VideoOverlay']),
('Audio',['Audios','AudioGroup','AudioItem','GlobalAudios','HomePageAudios','ProjectPageAudios','AboutPageAudios','ProjectsPageAudios']),
]
blocks=re.split(r'\n(?=## )',txt); rows={}
for b in blocks:
    m=re.match(r'## (\S+)(?: extends (\S+))?  \(byte (\d+), (\d+) bytes(, third-party)?\)',b)
    if not m or m.group(5): continue
    meth=[l.strip()[2:].split('  [')[0] for l in b.split('\n') if l.startswith('  - ')]
    rows[m.group(1)]=(m.group(2) or '',module_of(int(m.group(3))),int(m.group(4)),meth)
used=set(sum([g[1] for g in G],[]))
rest=[k for k in rows if k not in used]
G.append(('Site sections and scenes (home, about, projects, playground)',rest))
esc=lambda s:s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
out=[]
for title,names in G:
    out.append(f'## {title}\n\n<table header-row="true">\n<tr><td>Class</td><td>Module</td><td>Purpose</td><td>Purpose status</td><td>Methods (signatures as shipped)</td></tr>')
    for n in names:
        if n not in rows: print('MISSING',n); continue
        ext,mod,size,meth=rows[n]; p,s=P.get(n,('?','I'))
        cl=f'**{esc(n)}**'+(f' extends {esc(ext.replace("$","").rstrip("0123456789") if "AnyItem" in ext else ext)}' if ext else '')
        out.append(f'<tr><td>{cl}</td><td>{mod}</td><td>{esc(p)}</td><td>{"Confirmed" if s=="C" else "Inferred"}</td><td>{esc(", ".join(meth)) or "(fields only)"}</td></tr>')
    out.append('</table>\n')
open('ch13/tables.md','w').write('\n'.join(out))
print(len(rows), sum(1 for k in rows if P.get(k,('', 'I'))[1]=='C'), len('\n'.join(out)))
