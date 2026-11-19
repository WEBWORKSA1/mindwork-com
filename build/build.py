#!/usr/bin/env python3
"""Static site generator for MindWork.com. Standard library only.
Run from anywhere:  python3 build/build.py   (writes HTML into the repository root)"""
import datetime, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content_a import GAMES, TOOLS, QUIZZES
from content_b import MODELS, GUIDES, CATS
from pages_static import STATIC

BASE = 'https://mindwork.com'
CLIENT = 'ca-pub-6620975821265271'
CONTACT = 'https://web.works/contact'
VER = '8'
esc = html.escape
BASE404 = "<script>document.write('<base href=\"'+(/github\\.io$/.test(location.hostname)?'/'+location.pathname.split('/')[1]+'/':'/')+'\">')</script>\n"
PAGES = []  # (path, title, priority)

LOGO = '<svg viewBox="0 0 30 30" aria-hidden="true"><rect width="30" height="30" rx="5" fill="#14213D"/><g fill="#EEF1F6"><rect x="5" y="5" width="5.4" height="5.4" rx="1"/><rect x="12.3" y="5" width="5.4" height="5.4" rx="1"/><rect x="19.6" y="5" width="5.4" height="5.4" rx="1"/><rect x="5" y="12.3" width="5.4" height="5.4" rx="1"/><rect x="19.6" y="12.3" width="5.4" height="5.4" rx="1"/><rect x="5" y="19.6" width="5.4" height="5.4" rx="1"/><rect x="12.3" y="19.6" width="5.4" height="5.4" rx="1"/><rect x="19.6" y="19.6" width="5.4" height="5.4" rx="1"/></g><rect x="12.3" y="12.3" width="5.4" height="5.4" rx="1" fill="#F2B01E"/></svg>'
FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap'
NAV = [('train', 'Train', 'train/index.html'), ('focus', 'Focus', 'focus/index.html'), ('think', 'Think', 'models/index.html'), ('learn', 'Learn', 'guides/index.html'), ('', 'Daily workout', 'daily.html'), ('', 'My scores', 'dashboard.html')]


def load(name, default):
    try:
        with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


FEED = load('feed.json', {'updated': None, 'items': []})
VIDEOS = load('videos.json', {'updated': None, 'items': []})


def canonical(path):
    if path == 'index.html':
        return BASE + '/'
    if path.endswith('/index.html'):
        return BASE + '/' + path[:-10]
    return BASE + '/' + path


def page(path, title, desc, body, pillar='', page_id='', game='', tool='', scripts=(), schema='', prio='0.6', index=True):
    r = '../' * path.count('/')
    nav = ''.join('<a %shref="%s%s"%s>%s</a>' % ('data-p="%s" ' % p if p else '', r, href, ' aria-current="page"' if (p and p == pillar) or (not p and href == path) else '', label) for p, label, href in NAV)
    attrs = ''.join(' data-%s="%s"' % (k, v) for k, v in (('page', page_id), ('game', game), ('tool', tool)) if v)
    js = ''.join('<script src="%sassets/%s?v=%s" defer></script>' % (r, s, VER) for s in ('app.js',) + tuple(scripts) + ('pages.js',))
    full_title = title if path == 'index.html' else title + ' | MindWork.com'
    out = f'''<!doctype html>
<html lang="en" data-root="{r}">
<head>
<meta charset="utf-8">
{BASE404 if path == '404.html' else ''}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical(path)}">
{'' if index else '<meta name="robots" content="noindex">'}
<meta name="google-adsense-account" content="{CLIENT}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MindWork.com">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical(path)}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14213D">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{r}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{r}assets/style.css?v={VER}">
<script>try{{var t=localStorage.getItem('mw.theme');if(t)document.documentElement.setAttribute('data-theme',JSON.parse(t));}}catch(e){{}}</script>
<script src="{r}assets/config.js?v={VER}"></script>
<script>(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=(function(){{try{{return((window.MW_CONFIG||{{}}).consent==='google'||localStorage.getItem('mw.consent')==='"all"')?0:1}}catch(e){{return 1}}}})();</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CLIENT}" crossorigin="anonymous"></script>
{schema}
</head>
<body{attrs}>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><a href="{CONTACT}" target="_blank" rel="noopener"><span>Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership</span></a></div></div>
<header class="site-header"><div class="wrap">
<a class="logo" href="{r}index.html" aria-label="MindWork.com home">{LOGO}<span>MindWork<small>.com</small></span></a>
<button id="menu-btn" class="icon-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open the menu"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="2" fill="none"/></svg></button>
<nav id="nav" class="nav" aria-label="Main">{nav}</nav>
<div class="nav-tools"><button id="theme-btn" class="icon-btn" type="button" aria-pressed="false" aria-label="Switch between light and dark"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 2a8 8 0 0 1 0 16z" fill="currentColor"/></svg></button><a class="btn small" href="{r}start.html">Get the free plan</a></div>
</div></header>
<main id="main">
{body.replace('{R}', r)}
</main>
<footer class="site-footer"><div class="wrap">
<div class="fcols">
<div><a class="logo" href="{r}index.html">{LOGO}<span>MindWork<small>.com</small></span></a><p class="muted" style="margin-top:10px;max-width:26em">Free tests, focus tools and thinking models for people who think for a living. Paid for by advertising, sponsors and supporters.</p></div>
<div><h4>Train</h4><ul><li><a href="{r}train/index.html">All nine tests</a></li><li><a href="{r}daily.html">Daily workout</a></li><li><a href="{r}dashboard.html">My scores</a></li><li><a href="{r}contests.html">Monthly challenge</a></li></ul></div>
<div><h4>Focus and think</h4><ul><li><a href="{r}focus/index.html">Focus tools</a></li><li><a href="{r}models/index.html">Mental models</a></li><li><a href="{r}quizzes/index.html">Quizzes</a></li><li><a href="{r}start.html">7-day focus reset</a></li></ul></div>
<div><h4>Learn</h4><ul><li><a href="{r}guides/index.html">Guides</a></li><li><a href="{r}research.html">Research radar</a></li><li><a href="{r}videos.html">Videos</a></li><li><a href="{r}editorial.html">How we write</a></li></ul></div>
<div><h4>This site</h4><ul><li><a href="{r}about.html">About</a></li><li><a href="{r}contact.html">Contact</a></li><li><a href="{r}teams.html">For teams and sponsors</a></li><li><a href="{r}support.html">Support the site</a></li><li><a href="{r}careers.html">Work with us</a></li></ul></div>
</div>
<p class="fine">&copy; <span data-year>{datetime.date.today().year}</span> MindWork.com. <a href="{r}privacy.html">Privacy</a> &nbsp; <a href="{r}terms.html">Terms</a> &nbsp; <a href="{r}disclaimer.html">Disclaimer</a> &nbsp; <a href="{r}trademark.html">Trademark and copyright</a> &nbsp; <a href="{r}sitemap.html">Site map</a><br>
MindWork.com is an independent website named after its own domain. It is not affiliated with, endorsed by or connected to any company, product or registered trademark with a similar name. The tests and tools are for education and entertainment. They are not medical, psychological or professional advice and cannot diagnose anything.</p>
</div></footer>
<div id="consent" class="consent" role="dialog" aria-label="Cookies"><p>This site uses cookies and browser storage to remember your scores and to show advertising. See the <a href="{r}privacy.html">privacy policy</a>.</p><div class="btn-row"><button class="btn small" type="button" data-consent="all">Accept all cookies</button><button class="btn ghost small" type="button" data-consent="limited">Use non-personalised ads only</button></div></div>
{'' if path in ('start.html', '404.html') else f'<div id="leadbar" class="leadbar"><div class="wrap"><p>Free 7-day focus reset: one small change a day, with the tools to do it.</p><a class="btn small" href="{r}start.html">Get the free plan</a><button class="x" type="button" aria-label="Hide this message">&times;</button></div></div>'}
{js}
</body>
</html>
'''
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(out)
    if index and path != '404.html':
        PAGES.append((path, title, prio))


# ---------- helpers ----------
def tile(href, name, text, p, test=''):
    return '<li><a class="tile" data-p="%s"%s href="{R}%s"><b>%s</b><span>%s</span>%s</a></li>' % (p, ' data-test="%s"' % test if test else '', href, name, text, '<em></em>' if test else '')


def crumbs(*items):
    parts = ['<a href="{R}index.html">Home</a>'] + ['<a href="{R}%s">%s</a>' % (h, t) if h else t for h, t in items]
    return '<p class="crumbs">' + ' / '.join(parts) + '</p>'


def ad(slot):
    return '<div class="ad" data-ad="%s"></div>' % slot


def sources(items):
    return '<div class="sources"><b>Sources</b><ul>' + ''.join('<li>%s</li>' % s for s in items) + '</ul></div>'


def form(fid, subject, done, fields, button, consent='I agree to be contacted about this request and have read the <a href="{R}privacy.html">privacy policy</a>.', unlock=False, nxt=''):
    extra = (' data-unlock="1"' if unlock else '') + (' data-next="%s"' % nxt if nxt else '')
    return ('<form class="form mw-form" id="%s" data-form="%s" data-subject="%s" data-done="%s"' + extra + '>'
            '<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">%s'
            '<label class="check"><input type="checkbox" name="consent" value="yes" required> <span>%s</span></label>'
            '<button class="btn" type="submit">%s</button><p class="form-status" role="status" aria-live="polite"></p></form>') % (fid, fid, esc(subject), esc(done), fields, consent, button)


def field(label, name, typ='text', req=True, extra=''):
    return '<label>%s<input type="%s" name="%s"%s %s></label>' % (label, typ, name, ' required' if req else '', extra)


def select(label, name, options):
    return '<label>%s<select name="%s">%s</select></label>' % (label, name, ''.join('<option>%s</option>' % o for o in options))


def lead_block(fid='lead-form-inline'):
    f = form(fid, 'Focus reset sign-up', 'Unlocked.',
             '<div class="row">' + field('First name', 'name', extra='autocomplete="given-name" maxlength="60"') + field('Email', 'email', 'email', extra='autocomplete="email" maxlength="120"') + '</div>',
             'Unlock the 7-day plan', 'Unlock the plan in my browser and email me occasional MindWork.com updates. I can unsubscribe at any time. <a href="{R}privacy.html">Privacy policy</a>.', unlock=True, nxt='start.html')
    return ('<section class="lead"><div><h2>Get the free 7-day focus reset</h2><p>One small change a day for a week: measure your baseline, protect one block, close the exits, batch your messages, sort your list, recover properly, then measure again.</p>'
            '<ul><li>Takes about ten minutes a day</li><li>Uses the free tools on this site</li><li>Unlocks in your browser the moment you sign up</li></ul></div><div>%s</div></section>') % f


def aside_links(title, items):
    return '<div class="panel"><h3>%s</h3><ul style="list-style:none;padding:0;margin:0;display:grid;gap:7px">%s</ul></div>' % (title, ''.join('<li><a href="{R}%s">%s</a></li>' % (h, t) for h, t in items))


def breadcrumb_schema(path, trail):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'}]
    for i, (h, t) in enumerate(trail):
        items.append({'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': canonical(h) if h else canonical(path)})
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}) + '</script>'


def video_cards(items):
    return ''.join('<li class="video"><button type="button" data-yt="%s" aria-label="Play video: %s"><img loading="lazy" src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" width="480" height="360"></button><div><b>%s</b><span>%s</span></div></li>' % (esc(v['id']), esc(v['title']), esc(v['id']), esc(v['title']), esc(v.get('channel', ''))) for v in items)


def feed_rows(items):
    return ''.join('<li><a href="%s" target="_blank" rel="noopener nofollow">%s</a><span>%s, %s</span></li>' % (esc(i['url']), esc(i['title']), esc(i['source']), esc(i.get('date', '')[:10])) for i in items)


DAILY_ASIDE = '<div class="panel ink"><h3>Today’s workout</h3><p class="muted">Three tests, about five minutes. Finish all three to keep your streak.</p><a class="btn small" href="{R}daily.html">Open today’s workout</a></div>'
PLAN_ASIDE = '<div class="panel"><h3>Free 7-day focus reset</h3><p class="muted">One small change a day, built on these tools.</p><a class="btn small ghost" href="{R}start.html">Get the free plan</a></div>'
CAT = dict(CATS)
TEST_TILES = ''.join(tile('train/%s.html' % g['slug'], g['short'], g['blurb'], 'train', g['id']) for g in GAMES)
TOOL_TILES = ''.join(tile('focus/%s.html' % t['slug'], t['name'], t['blurb'], 'focus') for t in TOOLS)
GUIDE_TILES = ''.join(tile('guides/%s.html' % g['slug'], g['title'], '%s min read' % g['minutes'], 'learn') for g in GUIDES)
QUIZ_TILES = ''.join(tile('quizzes/%s.html' % q['slug'], q['name'], q['blurb'], 'think') for q in QUIZZES)


# ---------- home ----------
def home():
    models8 = ''.join(tile('models/%s.html' % m['slug'], m['name'], m['line'], 'think') for m in MODELS[:8])
    latest = FEED['items'][:5]
    radar = ('<ul class="feed">%s</ul>' % feed_rows(latest)) if latest else '<p class="muted">The research radar fills itself once a day from public science feeds.</p>'
    vids = VIDEOS['items'][:3]
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div><h1>Put your mind to work</h1>
<p class="lede">Free tests, focus tools and thinking models for people who think for a living. No sign-up and nothing to download. Start with the reaction test on this page.</p>
<div class="btn-row"><a class="btn" href="{{R}}daily.html">Start today’s workout</a><a class="btn ghost" href="{{R}}train/index.html">See all nine tests</a></div>
</div>
<div id="hero-pad" aria-label="Reaction time warm-up"></div>
</div>
<div class="wrap"><ul class="counts"><li><b>{len(GAMES)}</b><span>cognitive tests</span></li><li><b>{len(TOOLS)}</b><span>focus tools</span></li><li><b>{len(MODELS)}</b><span>mental models</span></li><li><b>{len(GUIDES)}</b><span>guides with sources</span></li><li><b>{len(QUIZZES)}</b><span>quizzes</span></li></ul></div></section>
<div class="wrap">
<section class="section" style="padding-top:8px"><div class="section-head"><div><h2>Today’s five-minute workout</h2><p>Three tests, picked fresh each day and the same for everyone. Finish all three to build a streak. <span id="home-streak"></span></p></div><a class="btn ghost small" href="{{R}}daily.html">Open the workout</a></div>
<ul class="tiles" id="daily-picks"></ul></section>
{ad('top')}
<section class="pillar" data-p="train"><a class="tab" href="{{R}}train/index.html">Train</a><div class="pillar-intro"><div><h2>Measure how sharp you are today</h2><p>Nine short tests of reaction, memory and attention, each based on a task psychologists use. Scores stay in your browser and build a personal record on your dashboard.</p><a class="btn small ghost" href="{{R}}dashboard.html">See my scores</a></div><ul class="tiles">{TEST_TILES}</ul></div></section>
<section class="pillar" data-p="focus"><a class="tab" href="{{R}}focus/index.html">Focus</a><div class="pillar-intro"><div><h2>Tools for getting the work done</h2><p>A timer, a breathing pacer, a noise mixer and three planners. They run in the page, remember your settings and print cleanly.</p><a class="btn small ghost" href="{{R}}focus/index.html">Open the focus tools</a></div><ul class="tiles">{TOOL_TILES}</ul></div></section>
<section class="pillar" data-p="think"><a class="tab" href="{{R}}models/index.html">Think</a><div class="pillar-intro"><div><h2>Models for deciding and solving</h2><p>{len(MODELS)} mental models, each with the steps, a workplace example and the usual way it gets misused. Plus three quizzes.</p><a class="btn small ghost" href="{{R}}models/index.html">Browse all {len(MODELS)} models</a></div><ul class="tiles">{models8}{QUIZ_TILES}</ul></div></section>
<section class="pillar" data-p="learn"><a class="tab" href="{{R}}guides/index.html">Learn</a><div class="pillar-intro"><div><h2>What the research says</h2><p>Plain-language guides with their sources listed, a research radar that refreshes daily, and a video shelf of talks worth your time.</p><a class="btn small ghost" href="{{R}}guides/index.html">Read the guides</a></div><ul class="tiles">{GUIDE_TILES}</ul></div></section>
{ad('mid')}
<section class="section"><div class="two">
<div class="panel"><div class="section-head"><h2>Research radar</h2><a href="{{R}}research.html">All headlines</a></div>{radar}</div>
<div class="panel"><div class="section-head"><h2>Watch</h2><a href="{{R}}videos.html">All videos</a></div><ul class="vgrid" style="grid-template-columns:1fr">{video_cards(vids[:1])}</ul><ul class="feed">{''.join('<li><a href="{R}videos.html">%s</a><span>%s</span></li>' % (esc(v['title']), esc(v.get('channel',''))) for v in vids[1:])}</ul></div>
</div></section>
<section class="section" id="plan">{lead_block('lead-form-home')}</section>
<section class="section"><div class="three">
<div class="panel"><h3>How this site is paid for</h3><p class="muted">Advertising, sponsors and voluntary support keep every tool free. Ads are kept away from the test areas so they cannot be clicked by accident.</p><a href="{{R}}support.html">Support the site</a></div>
<div class="panel"><h3>For teams and sponsors</h3><p class="muted">Run a focus workshop for your team, sponsor a tool or the monthly challenge, or license the tests.</p><a href="{{R}}teams.html">See the options</a></div>
<div class="panel"><h3>This month’s challenge</h3><p class="muted">One featured test a month, ranked entries and a hall of fame. Free to enter.</p><a href="{{R}}contests.html">Enter the challenge</a></div>
</div></section>
<section class="section"><h2>Common questions</h2><div class="two">
<div><h3>Is everything free?</h3><p>Yes. Every test, tool, model and guide is free to use without an account. The site is funded by advertising, sponsors and supporters.</p>
<h3>Where are my scores stored?</h3><p>In your own browser, using local storage. Nothing is sent to a server, which also means your scores do not follow you to another device. You can export or delete them from the dashboard.</p></div>
<div><h3>Do these tests measure intelligence?</h3><p>No. Each one measures a narrow skill on a given day, on your device. They are useful for tracking your own state over time and are not IQ tests or medical assessments.</p>
<h3>Will the tests make me smarter?</h3><p>Practice makes you better at the test you practise. Evidence that this carries over to everyday thinking is weak, and we say so in the <a href="{{R}}guides/does-brain-training-work.html">brain-training guide</a>.</p></div>
</div></section>
</div>'''
    schema = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'MindWork.com', 'url': BASE + '/', 'description': 'Free cognitive tests, focus tools and mental models for knowledge workers.'}) + '</script>'
    page('index.html', 'MindWork.com: free brain tests, focus tools and mental models', 'Put your mind to work: nine free cognitive tests, six focus tools, 25 mental models and evidence-based guides. No sign-up, nothing to download.', body, page_id='home', scripts=('train.js',), schema=schema, prio='1.0')


# ---------- train ----------
def train():
    rows = ''.join('<tr><td><a href="{R}train/%s.html">%s</a></td><td>%s</td></tr>' % (g['slug'], g['short'], g['measures'].split(':')[0]) for g in GAMES)
    body = f'''<div class="wrap">{crumbs(('', 'Train'))}
<div class="page-head"><h1>Nine tests of reaction, memory and attention</h1><p>Each test takes one to three minutes and is based on a task used in psychology research. Scores are saved in your browser, so the second run tells you more than the first.</p></div>
<ul class="tiles">{TEST_TILES}</ul>
{ad('top')}
<section class="section"><div class="two">
<div><h2>How to use the tests</h2><ol class="steps"><li>Take each test once to set a baseline. First runs are usually your worst.</li><li>Retest in the same conditions: same device, same time of day.</li><li>Watch the trend on your <a href="{{R}}dashboard.html">dashboard</a>, not single results. A bad night shows up here before you feel it.</li><li>Use the <a href="{{R}}daily.html">daily workout</a> if you want a routine: three tests, about five minutes.</li></ol></div>
<div><h2>What each test measures</h2><div class="table-scroll"><table><thead><tr><th>Test</th><th>Skill</th></tr></thead><tbody>{rows}</tbody></table></div></div>
</div>
<p class="note">These are browser versions of research tasks, scored on your own hardware. They are not IQ tests, clinical assessments or a diagnosis of anything. If you are worried about your memory or attention, talk to a doctor.</p></section>
<section class="section"><h2>Your MindWork.com score</h2><p style="max-width:44em">The dashboard converts your best result on each test to a 0 to 100 scale and averages them into one number. It is a convenience for tracking yourself over time. It is not a norm-referenced score and should not be compared with anyone else’s.</p><a class="btn" href="{{R}}dashboard.html">Open my dashboard</a></section>
</div>'''
    page('train/index.html', 'Free cognitive tests: reaction, memory and attention', 'Nine free browser tests based on research tasks: reaction time, number memory, Stroop, 2-back, mental math and more. No sign-up; scores saved on your device.', body, pillar='train', scripts=('train.js',), schema=breadcrumb_schema('train/index.html', [('', 'Train')]), prio='0.9')
    for i, g in enumerate(GAMES):
        others = [(('train/%s.html' % o['slug']), o['short']) for o in GAMES if o is not g]
        table = ''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in g['table'])
        body = f'''<div class="wrap">{crumbs(('train/index.html', 'Train'), ('', g['short']))}
<div class="page-head"><h1>{g['name']}</h1><p>{g['blurb']}</p></div>
<div id="stage" class="stage" aria-live="polite"></div>
<div id="result" class="result" hidden></div>
{ad('mid')}
<div class="layout section"><article class="prose">
<h2 style="margin-top:0">What it measures</h2><p>{g['measures']}</p>
<h2>The science behind it</h2>{g['science']}
<h2>How to improve your score</h2><ul>{''.join('<li>%s</li>' % x for x in g['improve'])}</ul>
<h2>Reading your result</h2><div class="table-scroll"><table><thead><tr><th>Result</th><th>What we call it</th></tr></thead><tbody>{table}</tbody></table></div>
<p>These ranges are informal guides for this browser version of the task. They are not clinical norms, and a single run says little; look at your trend.</p>
{sources(g['sources'])}</article>
<aside>{DAILY_ASIDE}{aside_links('More tests', others)}{PLAN_ASIDE}{ad('side')}</aside></div>
</div>'''
        page('train/%s.html' % g['slug'], g['name'] + ': free online test', g['blurb'] + ' Free, no sign-up. ' + g['measures'].split('.')[0] + '.', body, pillar='train', game=g['id'], scripts=('train.js',), schema=breadcrumb_schema('train/%s.html' % g['slug'], [('train/index.html', 'Train'), ('', g['short'])]), prio='0.8')


# ---------- focus ----------
def focus():
    body = f'''<div class="wrap">{crumbs(('', 'Focus'))}
<div class="page-head"><h1>Six tools for focused work</h1><p>Each tool runs in this page, saves its state in your browser and needs no account. Pick the one that fits the problem in front of you.</p></div>
<ul class="tiles">{TOOL_TILES}</ul>
{ad('top')}
<section class="section"><h2>Which tool for which problem</h2><div class="table-scroll"><table><thead><tr><th>If this is the problem</th><th>Use this</th></tr></thead><tbody>
<tr><td>You cannot get started, or you drift after ten minutes</td><td><a href="{{R}}focus/focus-timer.html">Focus timer</a></td></tr>
<tr><td>You feel wound up before a meeting or between tasks</td><td><a href="{{R}}focus/breathing-pacer.html">Breathing pacer</a></td></tr>
<tr><td>The room is noisy and voices keep pulling you away</td><td><a href="{{R}}focus/noise-mixer.html">Noise mixer</a></td></tr>
<tr><td>Everything feels urgent</td><td><a href="{{R}}focus/eisenhower-matrix.html">Eisenhower matrix</a></td></tr>
<tr><td>You are stuck between options</td><td><a href="{{R}}focus/decision-matrix.html">Decision matrix</a></td></tr>
<tr><td>The day disappears into meetings and messages</td><td><a href="{{R}}focus/time-block-planner.html">Time-block planner</a></td></tr>
</tbody></table></div><p>Not sure where to begin? The <a href="{{R}}quizzes/productivity-method.html">productivity method quiz</a> recommends one routine in eight questions, and the <a href="{{R}}guides/deep-work-protocol.html">deep work protocol</a> shows how the tools fit together.</p></section>
{lead_block('lead-form-focus')}
</div>'''
    page('focus/index.html', 'Free focus tools: timer, breathing, noise and planners', 'Six free focus tools that run in your browser: Pomodoro-style timer, breathing pacer, noise mixer, Eisenhower matrix, decision matrix and time-block planner.', body, pillar='focus', schema=breadcrumb_schema('focus/index.html', [('', 'Focus')]), prio='0.9')
    for t in TOOLS:
        others = [(('focus/%s.html' % o['slug']), o['name']) for o in TOOLS if o is not t]
        body = f'''<div class="wrap">{crumbs(('focus/index.html', 'Focus'), ('', t['name']))}
<div class="page-head"><h1>{t['name']}</h1><p>{t['intro']}</p></div>
<div id="tool" class="tool"></div>
{ad('mid')}
<div class="layout section"><article class="prose">
<h2 style="margin-top:0">How to use it</h2><ol>{''.join('<li>%s</li>' % x for x in t['how'])}</ol>
<h2>Why it works</h2>{t['why']}
{sources(t['sources'])}</article>
<aside>{aside_links('More focus tools', others)}{PLAN_ASIDE}{DAILY_ASIDE}{ad('side')}</aside></div>
</div>'''
        page('focus/%s.html' % t['slug'], t['name'] + ': free online tool', t['blurb'] + ' Free, runs in your browser, no sign-up.', body, pillar='focus', tool=t['id'], scripts=('focus.js',), schema=breadcrumb_schema('focus/%s.html' % t['slug'], [('focus/index.html', 'Focus'), ('', t['name'])]), prio='0.8')


# ---------- think: models + quizzes ----------
def think():
    chips = '<button class="chip" type="button" data-cat-btn="all" aria-pressed="true">All</button>' + ''.join('<button class="chip" type="button" data-cat-btn="%s" aria-pressed="false">%s</button>' % c for c in CATS)
    items = ''.join('<li data-cat="%s"><a class="tile" data-p="think" href="{R}models/%s.html"><b>%s</b><span>%s</span><em>%s</em></a></li>' % (m['cat'], m['slug'], m['name'], m['line'], CAT[m['cat']]) for m in MODELS)
    body = f'''<div class="wrap">{crumbs(('', 'Think'))}
<div class="page-head"><h1>{len(MODELS)} mental models for work</h1><p>Compact ideas for deciding, solving and explaining. Each page gives the steps, an example from working life and the usual way the model gets misused.</p></div>
<div class="inline-add" style="margin:0 0 12px;max-width:520px"><input id="model-search" type="search" placeholder="Search the models" aria-label="Search the models"></div>
<div class="chips" data-filter-group="#model-list" data-search="#model-search">{chips}</div>
<ul class="tiles" id="model-list">{items}</ul>
{ad('top')}
<section class="section"><div class="two"><div><h2>How to use this library</h2><p>Do not try to learn all of them. Pick five that match where your work goes wrong, tie each to a situation, and use them for a month. The <a href="{{R}}guides/build-a-thinking-toolkit.html">thinking toolkit guide</a> has a four-week plan.</p></div>
<div><h2>Test yourself</h2><ul class="tiles">{QUIZ_TILES}</ul></div></div></section>
</div>'''
    page('models/index.html', 'Mental models for work: a practical library', '%d mental models for deciding, problem solving, prioritising and communicating, each with steps, a workplace example and common pitfalls.' % len(MODELS), body, pillar='think', schema=breadcrumb_schema('models/index.html', [('', 'Think')]), prio='0.9')
    by = {m['slug']: m for m in MODELS}
    for m in MODELS:
        related = [('models/%s.html' % s, by[s]['name']) for s in m['related'] if s in by]
        same = [('models/%s.html' % o['slug'], o['name']) for o in MODELS if o['cat'] == m['cat'] and o is not m]
        body = f'''<div class="wrap">{crumbs(('models/index.html', 'Think'), ('', m['name']))}
<div class="page-head"><h1>{m['name']}</h1><p>{m['line']}</p></div>
<div class="layout"><article class="prose">
<h2 style="margin-top:0">What it is</h2><p>{m['what']}</p>
<h2>How to use it</h2><ol class="steps">{''.join('<li>%s</li>' % s for s in m['steps'])}</ol>
<h2>At work</h2><p>{m['example']}</p>
<h2>Where it goes wrong</h2><p>{m['trap']}</p>
<h2>Where it comes from</h2><p>{m['origin']}</p>
<p class="note" style="font-family:var(--sans)">Use it today: write one decision you are facing this week and run it through the steps above. Two lines is enough.</p>
</article>
<aside>{aside_links('Related models', related)}{aside_links('More in ' + CAT[m['cat']].lower(), same)}{PLAN_ASIDE}{ad('side')}</aside></div>
{ad('mid')}
</div>'''
        page('models/%s.html' % m['slug'], m['name'] + ': mental model explained', m['line'] + ' ' + m['what'].split('. ')[0] + '.', body, pillar='think', schema=breadcrumb_schema('models/%s.html' % m['slug'], [('models/index.html', 'Think'), ('', m['name'])]), prio='0.7')
    body = f'''<div class="wrap">{crumbs(('models/index.html', 'Think'), ('', 'Quizzes'))}
<div class="page-head"><h1>Quizzes</h1><p>Three short quizzes with explanations for every answer. Nothing to sign up for, and your result appears on the page.</p></div>
<ul class="tiles">{QUIZ_TILES}</ul>{ad('top')}
<section class="section"><p class="note">The quizzes are for learning and reflection. They are not psychological assessments.</p></section></div>'''
    page('quizzes/index.html', 'Quizzes: productivity method, cognitive biases, brain myths', 'Three free quizzes with explained answers: find your productivity method, spot cognitive biases at work, and sort brain myths from facts.', body, pillar='think', prio='0.7')
    for q in QUIZZES:
        others = [('quizzes/%s.html' % o['slug'], o['name']) for o in QUIZZES if o is not q]
        body = f'''<div class="wrap">{crumbs(('models/index.html', 'Think'), ('quizzes/index.html', 'Quizzes'), ('', q['name']))}
<div class="page-head"><h1>{q['name']}</h1><p>{q['intro']}</p></div>
<div class="layout"><div><div id="quiz" class="quiz"><noscript>This quiz needs JavaScript.</noscript></div>{ad('mid')}</div>
<aside>{aside_links('More quizzes', others)}{aside_links('Go deeper', [('models/index.html', 'Mental model library'), ('guides/better-decisions.html', 'Better decisions checklist'), ('guides/does-brain-training-work.html', 'Does brain training work?')])}{PLAN_ASIDE}</aside></div>
<script type="application/json" id="quiz-data">{json.dumps(q['data'], ensure_ascii=False).replace('</', '<\\/')}</script>
</div>'''
        page('quizzes/%s.html' % q['slug'], q['name'], q['blurb'] + ' Free quiz with an explanation for every answer.', body, pillar='think', prio='0.7')


# ---------- learn: guides, research, videos ----------
def learn():
    cards = ''.join('<li><a class="tile" data-p="learn" href="{R}guides/%s.html"><b>%s</b><span>%s</span><em>%s min read</em></a></li>' % (g['slug'], g['title'], g['desc'], g['minutes']) for g in GUIDES)
    body = f'''<div class="wrap">{crumbs(('', 'Learn'))}
<div class="page-head"><h1>Guides that show their sources</h1><p>Practical explanations of how attention, memory and decisions work, written in plain language. Every guide lists the studies it relies on, including the ones that complicate the story.</p></div>
<ul class="tiles" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">{cards}</ul>{ad('top')}
<section class="section"><div class="two"><div class="panel"><h2>Research radar</h2><p class="muted">New headlines on the brain, attention and work, refreshed once a day from public science feeds.</p><a class="btn small ghost" href="{{R}}research.html">Open the radar</a></div>
<div class="panel"><h2>Video shelf</h2><p class="muted">Talks and explainers on focus, memory and thinking, embedded from YouTube.</p><a class="btn small ghost" href="{{R}}videos.html">Watch the videos</a></div></div></section>
</div>'''
    page('guides/index.html', 'Guides to focus, memory and better decisions', 'Evidence-based guides on deep work, memory, brain training, task switching, decisions, the Pomodoro Technique, sleep and exercise. Sources listed on every page.', body, pillar='learn', schema=breadcrumb_schema('guides/index.html', [('', 'Learn')]), prio='0.9')
    for g in GUIDES:
        others = [('guides/%s.html' % o['slug'], o['title']) for o in GUIDES if o is not g][:6]
        art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'mainEntityOfPage': canonical('guides/%s.html' % g['slug']), 'author': {'@type': 'Organization', 'name': 'MindWork.com'}, 'publisher': {'@type': 'Organization', 'name': 'MindWork.com'}}
        body = f'''<div class="wrap">{crumbs(('guides/index.html', 'Learn'), ('', g['title']))}
<div class="page-head"><h1>{g['title']}</h1><p>{g['desc']} About {g['minutes']} minutes to read.</p></div>
<div class="layout"><article class="prose">{g['body'].replace('../', '{R}')}
{sources(g['sources'])}
<p class="note" style="font-family:var(--sans)">This guide is general information, not medical or professional advice. See <a href="{{R}}editorial.html">how we write and correct our pages</a>.</p></article>
<aside>{aside_links('More guides', others)}{PLAN_ASIDE}{DAILY_ASIDE}{ad('side')}</aside></div>
{ad('mid')}
</div>'''
        page('guides/%s.html' % g['slug'], g['title'], g['desc'], body, pillar='learn', schema='<script type="application/ld+json">' + json.dumps(art) + '</script>' + breadcrumb_schema('guides/%s.html' % g['slug'], [('guides/index.html', 'Learn'), ('', g['title'])]), prio='0.8')
    items = FEED['items'][:80]
    stamp = ('Last refreshed %s (UTC).' % FEED['updated'][:16].replace('T', ' ')) if FEED.get('updated') else 'The first refresh has not run yet.'
    lst = '<ul class="feed">%s</ul>' % feed_rows(items) if items else '<p class="note">No headlines yet. This page fills itself once a day; check back shortly.</p>'
    srcs = sorted({i['source'] for i in items})
    body = f'''<div class="wrap">{crumbs(('guides/index.html', 'Learn'), ('', 'Research radar'))}
<div class="page-head"><h1>Research radar</h1><p>New headlines on the brain, attention, memory and work from public science feeds. Each link opens the original publisher. {stamp}</p></div>
<div class="layout"><div>{lst}</div>
<aside><div class="panel"><h3>How to read a study headline</h3><ol style="padding-left:1.1em;margin:0"><li>Find the sample. Twenty students is a hint; twenty thousand adults is evidence.</li><li>Check for a comparison group. Without one, improvement may just be practice.</li><li>Ask what was measured. A lab task is not the same as everyday life.</li><li>Look for the word “associated”. It means the study cannot show cause.</li><li>Wait for a second study. Single findings often shrink when repeated.</li></ol></div>
{('<div class="panel"><h3>Feeds on this page</h3><p class="muted" style="margin:0">' + ', '.join(esc(s) for s in srcs) + '</p></div>') if srcs else ''}{PLAN_ASIDE}{ad('side')}</aside></div>
<p class="muted" style="margin-top:22px;max-width:60em">Headlines belong to their publishers and are listed here as links only. MindWork.com does not copy article text and is not affiliated with the sources. A scheduled job in this site’s repository rebuilds the list every day.</p>
</div>'''
    page('research.html', 'Research radar: daily brain and attention science headlines', 'A daily-refreshed list of new research headlines on the brain, attention, memory and work, linked to the original publishers.', body, pillar='learn', prio='0.7')
    vitems = VIDEOS['items'][:36]
    vstamp = ('Last refreshed %s (UTC).' % VIDEOS['updated'][:16].replace('T', ' ')) if VIDEOS.get('updated') else ''
    body = f'''<div class="wrap">{crumbs(('guides/index.html', 'Learn'), ('', 'Videos'))}
<div class="page-head"><h1>Video shelf</h1><p>Talks and explainers on focus, memory, learning and decisions. Videos play from YouTube when you press play; nothing loads before that. {vstamp}</p></div>
<ul class="vgrid">{video_cards(vitems)}</ul>{ad('mid')}
<p class="muted" style="margin-top:22px;max-width:60em">Videos are embedded from YouTube and remain the property of their creators. MindWork.com is not affiliated with the channels shown. The shelf is refreshed by a scheduled job that checks each video is still available.</p>
</div>'''
    page('videos.html', 'Videos on focus, memory and thinking', 'A refreshed shelf of talks and explainers about focus, memory, learning and decision making, embedded from YouTube.', body, pillar='learn', prio='0.6')


# ---------- static pages, site map, machine files ----------
def static_pages():
    ctx = dict(lead=lead_block('lead-form'), form=form, field=field, select=select, ad=ad, tiles=TEST_TILES, n_models=len(MODELS))
    for p in STATIC:
        body = p['body'](ctx) if callable(p['body']) else p['body']
        page(p['path'], p['title'], p['desc'], '<div class="wrap">%s%s</div>' % (crumbs(('', p.get('crumb', p['title']))) if p['path'] != '404.html' else '', body), page_id=p.get('page', ''), scripts=tuple(p.get('scripts', ())), prio=p.get('prio', '0.5'), index=p.get('index', True))


def machine_files():
    groups = [('Start here', [p for p in PAGES if '/' not in p[0]]), ('Train', [p for p in PAGES if p[0].startswith('train/')]), ('Focus', [p for p in PAGES if p[0].startswith('focus/')]), ('Mental models', [p for p in PAGES if p[0].startswith('models/')]), ('Quizzes', [p for p in PAGES if p[0].startswith('quizzes/')]), ('Guides', [p for p in PAGES if p[0].startswith('guides/')])]
    body = '<div class="wrap">' + crumbs(('', 'Site map')) + '<div class="page-head"><h1>Site map</h1><p>Every page on MindWork.com.</p></div>' + ''.join('<h2>%s</h2><ul>%s</ul>' % (g, ''.join('<li><a href="{R}%s">%s</a></li>' % (p[0], esc(p[1])) for p in ps)) for g, ps in groups) + '</div>'
    page('sitemap.html', 'Site map', 'A list of every page on MindWork.com.', body, prio='0.3')
    dyn = {'research.html': (FEED.get('updated') or '')[:10], 'videos.html': (VIDEOS.get('updated') or '')[:10], 'index.html': (FEED.get('updated') or '')[:10]}
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, _, prio in PAGES:
        lm = '<lastmod>%s</lastmod>' % dyn[path] if dyn.get(path) else ''
        xml.append('<url><loc>%s</loc>%s<priority>%s</priority></url>' % (canonical(path), lm, prio))
    xml.append('</urlset>')
    files = {
        'sitemap.xml': '\n'.join(xml) + '\n',
        'robots.txt': 'User-agent: *\nAllow: /\nDisallow: /build/\nDisallow: /scripts/\nDisallow: /docs/\n\nSitemap: %s/sitemap.xml\n' % BASE,
        'ads.txt': 'google.com, %s, DIRECT, f08c47fec0942fa0\n' % CLIENT.replace('ca-', ''),
        '.nojekyll': '',
        'manifest.webmanifest': json.dumps({'name': 'MindWork.com', 'short_name': 'MindWork', 'start_url': './index.html', 'display': 'standalone', 'background_color': '#EEF1F6', 'theme_color': '#14213D', 'icons': [{'src': 'assets/favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, indent=1) + '\n',
        'assets/favicon.svg': LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ''),
    }
    for name, text in files.items():
        with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
            f.write(text)


if __name__ == '__main__':
    home(); train(); focus(); think(); learn(); static_pages(); machine_files()
    print('built %d pages' % (len(PAGES) + 1))
