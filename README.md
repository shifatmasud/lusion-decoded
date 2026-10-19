# Lusion.co Decoded: companion repo

This is the companion repository for **[Lusion.co Decoded: Frontend Handbook](https://shifatmasud.notion.site/Lusion-co-Decoded-Client-Side-Handbook-3fd48559569d81dd80b4c7407caf27cc)**, a study of how the client side of [lusion.co](https://lusion.co) works: its WebGL engine, post-processing chain, virtual scroll, router, DOM-to-GPU sync, shaders, loading and layout. It also gives you a reusable architecture to build at the same baseline in your own projects.

The Notion handbook is the main, best-formatted version. This repo holds the same chapters as Markdown, the figures and screenshots, the scripts that did the capturing and analysis, and original teaching code.

> **Not affiliated with Lusion.** lusion.co, its design, code, shaders and assets belong to Lusion. This repo contains **no Lusion source code**: no bundle, no split modules, no shader files, no CSS or HTML snapshots and no assets. See [Copyright and fair use](#copyright-and-fair-use).

## Read the handbook

| Chapter | Markdown in this repo | Notion page |
|---|---|---|
| Main page | this README | [Lusion.co Decoded](https://shifatmasud.notion.site/Lusion-co-Decoded-Client-Side-Handbook-3fd48559569d81dd80b4c7407caf27cc) |
| 1. Stack and bundle anatomy | [01_stack_and_bundle_anatomy.md](handbook/01_stack_and_bundle_anatomy.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d8124ab68d56b80867ef5) |
| 2. Boot sequence and main loop | [02_boot_sequence_and_main_loop.md](handbook/02_boot_sequence_and_main_loop.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d811e94b1cd6359ec9594) |
| 3. Rendering engine and post-processing | [03_rendering_engine_and_post_processing.md](handbook/03_rendering_engine_and_post_processing.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d810bb1f9d6e4e072ee8a) |
| 4. DOM to WebGL sync (Ufx) | [04_dom_to_webgl_sync_ufx.md](handbook/04_dom_to_webgl_sync_ufx.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d816eb890f8d968ec1fae) |
| 5. Scroll, input and motion | [05_scroll_input_and_motion.md](handbook/05_scroll_input_and_motion.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d816d8a50c22e35b3ce7b) |
| 6. Routing, pages and sections | [06_routing_pages_and_sections.md](handbook/06_routing_pages_and_sections.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d817280f5e9676aca01db) |
| 7. Effects and scenes | [07_effects_and_scenes.md](handbook/07_effects_and_scenes.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81549fa5ff6c49d305fb) |
| 8. Shaders and the post-processing pipeline | [08_shaders_and_post_processing_pipeline.md](handbook/08_shaders_and_post_processing_pipeline.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81daa932c9558ddf8b9a) |
| 9. Assets and loading | [09_assets_and_loading.md](handbook/09_assets_and_loading.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81b397c9f275470e9b7a) |
| 10. CSS, layout and DOM state | [10_css_layout_and_dom_state.md](handbook/10_css_layout_and_dom_state.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81289d5ff6769e1f1d55) |
| 11. System architecture plan and conceptual model | [11_system_architecture_plan_and_conceptual_model.md](handbook/11_system_architecture_plan_and_conceptual_model.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81c1b174e921471bcaf6) |
| 12. Teardown guide | [12_teardown_guide.md](handbook/12_teardown_guide.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d8160ba22f0f918a83fec) |
| 13. Class and method inventory | [13_class_and_method_inventory.md](handbook/13_class_and_method_inventory.md) | [Notion](https://shifatmasud.notion.site/3fd48559569d81709a8ecf7dc5c65d23) |
| 14. Special: cursor fluid trail (ScreenPaint) | [14_special_cursor_fluid_trail_screenpaint.md](handbook/14_special_cursor_fluid_trail_screenpaint.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d81a98b50c232287e3463) |
| 15. Section-by-section screenshot atlas | [15_screenshot_atlas/](handbook/15_screenshot_atlas/15_0_overview.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d81069c7ff759ffc2bb9a) |
| 15.1 Home | [15_1_home.md](handbook/15_screenshot_atlas/15_1_home.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d817bb6bfdc1a46b69d91) |
| 15.2 About | [15_2_about.md](handbook/15_screenshot_atlas/15_2_about.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d810a98a2ee47788dcbb5) |
| 15.3 Projects | [15_3_projects.md](handbook/15_screenshot_atlas/15_3_projects.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d815884e7f0f2ddd6a104) |
| 15.4 Project page template | [15_4_project_template.md](handbook/15_screenshot_atlas/15_4_project_template.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d816381a1cb2ae37987bd) |
| 15.5 Project pages gallery | [15_5_gallery.md](handbook/15_screenshot_atlas/15_5_gallery.md) | [Notion](https://shifatmasud.notion.site/3fe48559569d817a9a25eb56b9252c63) |
| Playground findings (note) | [15_6_playground_findings.md](handbook/15_screenshot_atlas/15_6_playground_findings.md) | covered in the [chapter 15 overview](https://shifatmasud.notion.site/3fe48559569d81069c7ff759ffc2bb9a) |

Every chapter file starts with a **Read in Notion** link, and every Notion chapter page links back here.

## How it was made

1. **Static analysis.** The single shipped ES module was parsed with acorn and split by top-level class, so each class could be read on its own. The minifier keeps class and method names, which made it possible to inventory 130 app classes and 971 methods ([analysis/class_inventory.txt](analysis/class_inventory.txt)).
2. **Runtime probe.** A headless Chrome (Puppeteer, SwiftShader software GPU, 1440 x 900) loaded the live site, logged the network, counted WebGL programs, textures and render targets, and captured one frame pass by pass ([scripts/probe](scripts/probe), [analysis/runtime_report_home.json](analysis/runtime_report_home.json)).
3. **Captures.** Scripted desktop (1440 wide) and mobile (390 wide) screenshots of every page and section, using simulated wheel and touch input because the site scrolls virtually ([scripts/capture](scripts/capture)).
4. **Figures.** Diagrams, charts and annotated composites were generated with Python (Pillow, matplotlib) and HTML-to-PNG rendering ([scripts/figures](scripts/figures)).
5. **Writing.** Each chapter keeps **Confirmed** (read from shipped code or measured) apart from **Inference** (a reading of intent). Code marked "quoted" is a short excerpt for commentary; code marked "original" is our own.

The screenshots come from a browser with no graphics card, so glow and colour look flatter than on a real screen.

## Folder map

```
handbook/                     chapters 1-14 as Markdown
handbook/15_screenshot_atlas/ chapter 15: overview, Home, About, Projects, project template, gallery, Playground note
handbook/assets/<chapter>/    figures, diagrams, charts and annotated screenshots used by each chapter
teaching/cursor-liquid/       original CursorPaint (three.js) and CursorLiquid (React Three Fiber) teaching code
scripts/capture/              Puppeteer capture scripts (desktop, mobile, wheel and touch scrolling)
scripts/probe/                runtime probe: network, WebGL programs, textures, render targets, frame passes
scripts/analysis/             bundle parsing and class/method inventory tooling
scripts/figures/              chart, diagram, strip and annotation generators
scripts/notion-build/         scripts that assembled the Notion pages for chapter 15
analysis/                     our own outputs: class inventory, top-level class map, DOM outline, runtime report, frame passes
```

The scripts were written for a one-off study and expect a local working folder with the captured site next to them. They don't download or include Lusion's code. Paths inside them point at the original working machine.

### Notes on the Markdown

- The Notion pages were built from these files and then extended. Figures added to Notion later are collected in a **Figures** section at the end of each chapter here; in Notion they sit next to the section they explain.
- Some tables use HTML (`<table>`), and diagrams use Mermaid, which GitHub renders.

## What is not in this repo, and why

The following are Lusion's copyrighted work and are **deliberately left out**:

- the shipped JavaScript bundle (raw and prettified) and the modules split from it
- the shader files (GLSL source and compiled runtime shaders)
- Lusion's CSS and HTML snapshots
- Lusion's assets: textures, meshes, audio, video, fonts
- the study archive zip of all of the above

Raw, unannotated screenshot captures are also left out for size; the annotated composites used in the chapters are included.

## Copyright and fair use

- **lusion.co belongs to Lusion.** Its design, code, shaders, 3D models, textures, video and copy are Lusion's copyright. This project is not affiliated with or endorsed by Lusion.
- **Purpose: study, commentary and teaching.** The handbook explains how a public website works so others can learn the techniques. It quotes short excerpts of shipped client-side code where needed to explain a point, always marked as quoted.
- **No redistribution of Lusion's code.** You will not find their bundle, modules, shaders, stylesheets, markup or assets here. If you want to study them, open lusion.co in your own browser's DevTools.
- **Screenshots** of lusion.co are included at documentation size to illustrate the analysis.
- **Server-side code** was never accessed. Everything here comes from what any browser receives.
- If you represent Lusion and want anything changed or removed, please open an issue.

## License

This license covers **only our own work** in this repo. It does not cover Lusion's site, code, screenshots of it or quoted excerpts.

- **Code** (`scripts/`, `teaching/`): [MIT](LICENSE)
- **Docs and figures** (`handbook/`, `analysis/`, diagrams and charts): [CC BY 4.0](LICENSE-docs.md)

Made by [Shifat Masud](https://github.com/shifatmasud).
