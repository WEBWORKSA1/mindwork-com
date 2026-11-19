# MindWork.com

A free mental gym and thinking toolkit: nine cognitive tests, six focus tools, 25 mental models,
eight guides, three quizzes, a daily workout, a research radar and a video shelf.
Static HTML, CSS and JavaScript. No server, no database, no build dependencies beyond Python 3.12.

## Layout

| Path | What it is |
| --- | --- |
| `index.html`, `train/`, `focus/`, `models/`, `quizzes/`, `guides/`, `*.html` | The generated site (served as-is by GitHub Pages) |
| `assets/` | `style.css`, `app.js` (shared), `train.js` (tests), `focus.js` (tools), `pages.js` (quizzes and page wiring), `config.js` (settings) |
| `build/` | The generator: `build.py` plus content files (`content_a.py`, `content_b.py`, `pages_static.py`) |
| `scripts/refresh.py` | Fetches research headlines and videos into `data/` |
| `data/` | `feed.json`, `videos.json` (written by the refresh job) |
| `.github/workflows/refresh.yml` | Daily job: refresh data, rebuild pages, commit |
| `docs/` | The phase-wise build prompt and the research log |

## Change something

1. Edit a content file in `build/` (or `assets/` for behaviour and style).
2. Run `python3 build/build.py`.
3. Commit and push to `main`. Pushing a change under `build/` or `scripts/` also triggers the refresh job.

To add a mental model, guide, test description or tool description, add one entry to the matching list
in `build/content_a.py` or `build/content_b.py`. Hubs, site map and `sitemap.xml` update on the next build.

## Settings (`assets/config.js`)

- `adSlots`: paste AdSense ad-unit slot ids to switch on fixed placements. Empty slots stay collapsed. Auto ads need only the publisher id, which is already on every page.
- `consent`: set to `'google'` after enabling Google's consent message in AdSense (Privacy & messaging).
- `formToken`: the alias string the form relay sends after the first submission is confirmed.
- `payLinks`: hosted payment links. When set, the support page shows direct payment buttons.
- `contest`: prize text and closing date for the monthly challenge.

## Publish on GitHub Pages (free plan)

The site is live at `https://webworksa1.github.io/mindwork-com/`. `main` is the source of truth.
GitHub Pages currently serves the `gh-pages` branch, which the workflow keeps identical to `main` after every push
and every daily refresh.

To serve `main` directly: repository **Settings → Pages → Build and deployment → Branch: `main`, folder `/ (root)` → Save.**
The workflow notices the change, stops mirroring, and `gh-pages` can then be deleted. All links are relative, so the
site works on the github.io address and on a custom domain.

Custom domain: in the same Pages screen enter `mindwork.com`, then at the DNS host point the apex at GitHub Pages
(A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) and `www` as a CNAME to
`<account>.github.io`. Tick **Enforce HTTPS** once the certificate is issued. `ads.txt`, `robots.txt` and
`sitemap.xml` are already at the root and use the `https://mindwork.com` address.

## Automation

`refresh.yml` runs every day at 04:23 UTC, on manual dispatch, and when `build/` or `scripts/` change. It reads public
RSS/Atom feeds and YouTube channel feeds, keeps on-topic items, checks every video id against YouTube's oEmbed
endpoint, rebuilds the pages and commits only if something changed. Feed and channel lists are at the top of
`scripts/refresh.py`.

## Forms

Every form posts to one inbox through a form relay. The address is not written anywhere in this repository or on the
site. The relay sends a one-time confirmation email on the first submission; confirm it once and all forms deliver.

## Privacy and policy pages

`privacy.html`, `terms.html`, `disclaimer.html`, `trademark.html`, `editorial.html`, `about.html`, `contact.html`.
MindWork.com is an independent website named after its own domain and is not affiliated with any similarly named
company, product or trademark.
