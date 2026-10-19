> **Read in Notion:** [15.6 Playground findings (note; no Notion sub-page)](https://shifatmasud.notion.site/3fe48559569d81069c7ff759ffc2bb9a) · Part of [Lusion.co Decoded](https://shifatmasud.notion.site/Lusion-co-Decoded-Client-Side-Handbook-3fd48559569d81dd80b4c7407caf27cc) · [Repo home](https://github.com/shifatmasud/lusion-decoded)

# 15.6 Playground: findings (no page created)

Checked 2026-10-18 (PDT).

- `curl https://lusion.co/playground` returns 200, but the body is byte-for-byte the home shell (59,671 bytes, same as html/home.html and as a nonsense path like /zzznotapage). It contains `.page[data-page=home|about|projects]` only, no `#playground-main`.
- The client router still registers the route: `PageManager.pageList = [homePage, aboutPage, projectPage, projectsPage, playgroundPage]`, and `PlaygroundPage.path = "playground"` (modules/112_PlaygroundPage.js).
- Live load in headless Chromium (desktop 1440x900 and mobile 390x844, probe_pg.mjs): `TypeError: Cannot read properties of null (reading 'append')` in `PlaygroundPage.preInit` at 0.5-0.6 s, because `#playground-main-timeline` is not in the served DOM. The preloader stays at 000 for 25 s+; screenshots are black. Raw logs: raw/playground/{desktop,mobile}/probe.log.
- What the dormant code would build: a 300vh black scroll section with a 100vh sticky inner, a full-width clickable timeline at 50% height (line scaled to 0.1 tall, progress bar scaled by scroll ratio), three dated dots (2019-01-25, 2019-09-25, 2022-04-25, formatted `YY MMMM'DD`) that turn `--color-blue` when active or hovered, and a `tunnel.buf` mesh (900 bytes, served) rendered with MeshNormalMaterial. CSS: css/about.css lines 4294-4400 (`#playground-*`, `.playground-main-event*`, `#playground-bottom*`). It is unfinished work, not a public page.
- Other uncovered public pages: none. The router knows only home, about, projects, projects/<slug>, playground. The menu links are Home, About us, Projects and a Contact button (`data-scroll-to="contact"`). /sitemap-index.xml also returns the home shell. labs.lusion.co is a separate site linked as an external link.
