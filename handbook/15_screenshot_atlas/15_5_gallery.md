> **Read in Notion:** [15.5 Project pages gallery (the other 18)](https://shifatmasud.notion.site/3fe48559569d817a9a25eb56b9252c63) · Part of [Lusion.co Decoded: Frontend Handbook](https://shifatmasud.notion.site/3fd48559569d81dd80b4c7407caf27cc) · [Repo home](https://github.com/shifatmasud/lusion-decoded)

# 15.5 Project pages gallery (the other 18)

> 🖼️ Every project page uses the same `ProjectPage` template documented in 15.4. This page shows the first screen of each, plus one screen below it, so an agent can check the per-project data (title, description, meta list, media and colour variables) against the template. The values in the table were measured in the live page.

![First screen of each project page, desktop 1440×900, alphabetical by slug](../assets/15/gallery__heroes.jpg)

*First screen of each project page, desktop 1440×900, alphabetical by slug*

![One screen further down on each project page: media items start](../assets/15/gallery__below.jpg)

*One screen further down on each project page: media items start*

## Per-project data (measured)

Every title is Aeonik 72px weight 400 at 1440 wide. The title colour changes per project: it comes from that project's `--project-details-*` colour variables.

| Project | Route | Title size / weight | Title colour | Description (start) | Side list (first item) |
|---|---|---|---|---|---|
| [Atlas Motion](https://lusion.co/projects/atlas_motion) | `/projects/atlas_motion` | 72px 400 | #fffde0 | Atlas is building next generation motion systems for drones, robotics, | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Choo Choo World](https://lusion.co/projects/choo_choo_world) | `/projects/choo_choo_world` | 72px 400 | #000000 | Choo Choo World, a research project by Lusion, aimed to create an enjo | SERVICES Concept Game Design Web Design Web Development 3D D |
| [DDD 2024](https://lusion.co/projects/ddd_2024) | `/projects/ddd_2024` | 72px 400 | #ffffff | Digital Design Days is a 3-day experience that gathers in one place th | SERVICES UI/UX design 3D Visual design Creative Coding Front |
| [Devin AI](https://lusion.co/projects/devin_ai) | `/projects/devin_ai` | 72px 400 | #ffffff | We partnered with Cognition AI to create a modern website for Devin, t | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Everswap](https://lusion.co/projects/everswap) | `/projects/everswap` | 72px 400 | #000000 | We were commissioned by the EverSwap team to create an immersive story | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Infinite Passerella](https://lusion.co/projects/infinite_passerella) | `/projects/infinite_passerella` | 72px 400 | #ffffff | A New Era in Fashion Showcase. Lusion's R&amp;D journey transforms fashion | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Lusion Labs](https://lusion.co/projects/lusion_labs) | `/projects/lusion_labs` | 72px 400 | #ffffff | Lusion's Dedication to Innovation and Exploration. Our dedicated space | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Max Mara: Bearing Gifts](https://lusion.co/projects/maxmara_bearings_gifts) | `/projects/maxmara_bearings_gifts` | 72px 400 | #000000 | Collaborating with LOW: Transforming Digital Experiences. Our partners | SERVICES WebGL |
| [My Little Storybook](https://lusion.co/projects/my_little_story_book) | `/projects/my_little_story_book` | 72px 400 | #000000 | Expanding Boundaries through Cinematic Innovation. An R&amp;D feat by Lusi | SERVICES Concept Web Design Web Development 3D Design WebGL |
| [Of The Oak](https://lusion.co/projects/of_the_oak) | `/projects/of_the_oak` | 72px 400 | #d9f3de | MLF approached us to create a web companion for Of The Oak, their phys | SERVICES Web Design Web Development 3D Design WebGL Animatio |
| [Porsche: Dream Machine](https://lusion.co/projects/porsche_dream_machine) | `/projects/porsche_dream_machine` | 72px 400 | #000000 | Commissioned by Wallpaper\* and Porsche GB, Lusion created a CG short f | SERVICES Concept 3D Design Motion Design Compositing |
| [Soda Experience](https://lusion.co/projects/soda_experience) | `/projects/soda_experience` | 72px 400 | #000000 | Lusion teamed up with GoSpooky to embark on an exciting journey with C | SERVICES 3D Optimization WebGL WebAR |
| [Spaace](https://lusion.co/projects/spaace) | `/projects/spaace` | 72px 400 | #ffece2 | We worked with Spaace to bring this immersive brand website for their | SERVICES Web Design Web Development 3D Design WebGL |
| [Meta: Spatial Fusion](https://lusion.co/projects/spatial_fusion) | `/projects/spatial_fusion` | 72px 400 | #000000 | Lusion partnered with Phoria and Meta to create Spatial Fusion, an imm | SERVICES Web Design Web Development WebGL WebXR |
| [Synthetic Human](https://lusion.co/projects/synthetic_human) | `/projects/synthetic_human` | 72px 400 | #ffffff | We partnered with Fantasy to launch the campaign website for Synthetic | SERVICES Creative Coding Animation Frontend development 3D V |
| [The Turn Of The Screw](https://lusion.co/projects/the_turn_of_the_screw) | `/projects/the_turn_of_the_screw` | 72px 400 | #ffffff | In October 2019, Opera North, alongside the Audiolab of York Universit | SERVICES Web Design Web Development 3D Design WebGL |
| [Worldcoin Globe](https://lusion.co/projects/worldcoin) | `/projects/worldcoin` | 72px 400 | #000000 | In collaboration with Tools for Humanity, we successfully integrated t | SERVICES API Design 3D Design WebGL |
| [Zero Tech](https://lusion.co/projects/zero_tech) | `/projects/zero_tech` | 72px 400 | #ffffff | Zero approached us to design an engaging interactive website for Zero. | SERVICES Concept Web Design Web Development 3D Design WebGL |

## What changes per project and what stays fixed

- **Changes:** the title, description, meta (client, year, services), the media list (images, videos, text panels from `ProjectDetailsData`), the `--project-details-*` colour variables (see the title colours above), whether there's a launch link (`has-cta`), and the next-project target.
- **Fixed:** the layout grid, type scale (title 72px/400 at 1440 wide on every project), title-centred intro (`ease.expoInOut`), media fade-in (`ease.expoOut`), the back button in the header, and the next-project swap at the bottom.
- **To check a rebuild:** render each route from data alone and compare it with the two thumbnails here. The title wrap, the description length and where the first media item sits should match.
