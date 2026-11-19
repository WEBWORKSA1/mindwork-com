# MindWork.com: concept and phase-wise build prompt

## The concept in one line

**MindWork.com is a free, no-login mental gym and thinking toolkit for people who think for a living**: instant
cognitive tests, focus tools, mental models and sourced guides, funded by AdSense, sponsors and supporters.

## Why this idea (from 40 sites read directly)

| Finding | Evidence from the sites | Decision |
| --- | --- | --- |
| The big brain-training brands gate everything behind an app or account and carry no ads | Lumosity, Peak, Elevate, BrainHQ and CogniFit all push sign-up or download; none shows ads on its home page | Own the open lane: instant play in the browser, no account |
| Free, anonymous, ad-funded testing works at scale | 123test states it makes its money from advertising and reports 30M+ users a year; Sporcle shows about 6.9 billion quiz plays with ads plus a remove-ads plan; Pomofocus runs a free ad-supported timer | AdSense as the base revenue, tools as the traffic engine |
| Thinking-tool sites monetise by newsletter and membership, not ads | fs.blog (about 1M subscribers), untools (26 tools, "Get 3 templates"), ModelThinkers (US$8 a month), Mindtools (teams plans) | Give the models away, use them for search traffic and lead capture |
| The best lead magnets are a routine delivered at once | James Clear (30-day course), Huberman Lab (Daily Blueprint), untools (templates), Ness Labs (free chapter) | A 7-day focus reset that unlocks on the page the moment the form is sent |
| Daily sets and streaks drive return visits | Elevate's free tier is one three-game daily workout; Sporcle's Daily Dose; Lumosity's daily workout | A three-test daily workout with a streak |
| Every credible site disclaims diagnosis | Mensa ("entertainment purposes only"), Psychology Today ("not diagnostic"), CogniFit, 123test, BrainMetrix | Plain disclaimers on every test; no IQ or medical claims (also protects AdSense approval) |
| Nobody combines tests, focus tools and models for knowledge workers | The 40 sites split into four separate groups | Combine them under the two words in the domain: mind + work |

Revenue logic: revenue = sessions x pages per session x page RPM / 1000. Tools and tests raise pages per session;
a productivity and education audience attracts software, course and B2B advertisers. Illustrative only, with assumed
inputs: 100,000 sessions a month x 4 pages x US$5 RPM is about US$2,000 a month from ads, before sponsorship and
team leads. The inputs are assumptions to be replaced with real data after launch.

## The prompt

Use the phases in order. Each phase ends with a check that must pass before the next begins.

### Phase 0. Ground rules (apply to every phase)

- Domain: MindWork.com. Site name shown as "MindWork.com". Never use the plural "Mindworks", never brand a meditation,
  course or software product "MindWork", never imitate another party's logo.
- Top of every page: the sentence "Contact, if you are interested in this website / domain name / Sponsorship /
  Advertisement / Partnership", the whole sentence being one link to the business contact page. The link target is
  never shown as text.
- One inbox receives every form. The address is supplied privately and is never written in any file, page, script,
  commit or document. Forms post through a relay; the address is assembled at run time or replaced by the relay's alias.
- AdSense: put this in the head of every page, unchanged:
  `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>`
  plus `ads.txt` with `google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`.
- Static files only, relative links only, hosted on GitHub Pages from the `main` branch root. No frameworks.
- No invented testimonials, user counts, winners or prizes. No medical, IQ or "get smarter" claims.

### Phase 1. Research

Open and read at least 38 sites across four groups: brain training, online tests, thinking tools, focus tools. For
each, record what it does, its calls to action, how it makes money, its forms, and what to borrow or avoid. Check the
name for trademark conflicts and list them. Output: a research log and a decision table.

Check: 38 or more sites read directly; unreadable sites listed separately and not counted.

### Phase 2. Structure and design system

- Four pillars with one colour each: Train (tests), Focus (tools), Think (models and quizzes), Learn (guides,
  research radar, videos).
- Pages: home, four hubs, one page per test, tool, model, quiz and guide, daily workout, dashboard, lead page, teams,
  support, contests, careers, about, contact, privacy, terms, disclaimer, trademark and copyright, editorial policy,
  site map, 404.
- Design: one distinctive direction grounded in the subject (signal colours from the Stroop test, a measuring-bench
  grid, one typeface used through its width axis). The home page hero is a live reaction test, not a stock image.
  Light and dark themes, keyboard focus states, reduced-motion support, responsive to 360 px.

Check: every page reachable in two clicks from the home page; contrast and focus states verified.

### Phase 3. Train: nine tests

Reaction time, number memory, sequence memory, visual memory, Stroop, 2-back, mental math, verbal memory, Schulte
table. Each page: the test above the fold, a result panel (score, plain-language band, personal best, share, next
test), then 300+ words: what it measures, the science with named sources, how to improve, how to read the result.
Scores live in local storage. A dashboard shows bests, a 0 to 100 composite, streak and focus time, with export and
delete.

Check: every test completes with keyboard and touch; scores persist; no console errors.

### Phase 4. Focus: six tools

Focus timer with task list and daily count, breathing pacer, noise mixer generated in the browser, Eisenhower matrix,
weighted decision matrix, time-block planner with print. Each page: the tool, how to use it, why it works, sources.

Check: state survives a reload; print output is clean.

### Phase 5. Think and Learn: the content AdSense reviews

25 mental models (what, steps, workplace example, misuse, origin), three quizzes with explained answers, eight
sourced guides of 500+ words including one that states honestly what brain training does and does not do.

Check: every page has original text, one h1, a meta description and listed sources. No placeholder text anywhere.

### Phase 6. Revenue and leads

- Lead page: a 7-day focus reset. Day 1 open, days 2 to 7 unlock in the browser when the form is sent. The same form
  appears on the home page and the focus hub, with a dismissible sticky bar elsewhere.
- Teams page: workshop, sponsorship, advertising, licensing and partnership inquiry form.
- Support page: pledge form with amounts, frequency and purpose (running costs, contributors, contests and prizes,
  outreach), a published target split, and optional direct payment buttons driven by a settings file.
- Contests: one featured test a month, result codes, entry form, rules, hall of fame. A prize is shown only if set.
- Careers: project-based roles and an application form.
- Ads: Auto ads through the head tag; optional fixed slots that stay collapsed until slot ids are configured; no ads
  inside test areas.

Check: every form delivers through the relay; a failed send shows a retry and a link to the contact page.

### Phase 7. Compliance

Privacy policy with the Google advertising cookie disclosure and opt-out links, cookie notice with a non-personalised
option, terms, disclaimer, trademark and copyright disclosure naming the conflicting marks and third-party marks used,
editorial policy, about and contact pages, `robots.txt`, `sitemap.xml`, canonical tags, structured data.

Check: search the whole repository for the inbox address and for the bare contact host as visible text; both absent.

### Phase 8. Automation

A scheduled GitHub Actions job, daily: read public RSS/Atom feeds for brain, attention and work research (headline,
source, date and link only), read YouTube channel feeds, verify each video id through oEmbed, write JSON, rebuild the
pages, commit only when something changed. The daily workout and monthly challenge rotate by date in the browser.

Check: a failing feed does not fail the run; an empty fetch keeps the previous data.

### Phase 9. Test, push, publish

Headless-browser pass over every page (console errors, banner link, AdSense tag, one h1), a play-through of each test
and tool, a mocked form send. Push to `main` of the repository, enable GitHub Pages from `main` root, confirm the live
URL and the first refresh run.

### Phase 10. After launch (owner)

Point the domain at GitHub Pages, confirm the form relay's activation email, apply for AdSense once the domain
resolves, switch on Google's consent message, add ad-unit slot ids and a payment link in the settings file.
