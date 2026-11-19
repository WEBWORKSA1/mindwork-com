#!/usr/bin/env python3
"""Daily refresh for MindWork.com. Standard library only.

Reads public RSS/Atom feeds and YouTube channel feeds, keeps on-topic items, and writes
data/feed.json and data/videos.json. Only headline, source, date and link are stored for articles.
Every video id is checked against YouTube's oEmbed endpoint; ids that no longer resolve are dropped.
A feed that fails is skipped, and existing data is kept if nothing could be fetched."""
import datetime, email.utils, html, json, os, re, sys, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = 'Mozilla/5.0 (compatible; MindWorkRefresh/1.0; +https://mindwork.com/editorial.html)'
NOW = datetime.datetime.now(datetime.timezone.utc)

# (source name, url, apply keyword filter)
FEEDS = [
    ('ScienceDaily', 'https://www.sciencedaily.com/rss/mind_brain.xml', False),
    ('PsyPost', 'https://www.psypost.org/feed/', True),
    ('Neuroscience News', 'https://neurosciencenews.com/feed/', True),
    ('Greater Good Magazine', 'https://greatergood.berkeley.edu/site/rss/articles', True),
    ('The Conversation', 'https://theconversation.com/us/topics/psychology-28/articles.atom', True),
    ('Medical Xpress', 'https://medicalxpress.com/rss-feed/psychology-psychiatry-news/', True),
    ('Nature Human Behaviour', 'https://www.nature.com/nathumbehav.rss', True),
]
# (channel name, channel id)
CHANNELS = [
    ('TED-Ed', 'UCsooa4yRKGN_zEE8iknghZA'),
    ('TED', 'UCAuUUnT6oDeKwE6v1NGQxug'),
    ('Big Think', 'UCvQECJukTDE2i6aCoMnS-Vg'),
    ('SciShow Psych', 'UCUdettijNYvLAm4AixZv4RA'),
    ('Andrew Huberman', 'UC2D2CMWXMOVWx7giW1n3LIg'),
    ('Ali Abdaal', 'UCoOae5nYA7VqaXzerajD0lg'),
    ('Thomas Frank', 'UCG-KntY7aVnIGXYEBQvmBAQ'),
    ('Veritasium', 'UCHnyfMqiRRG1u-2MsSQLbXA'),
    ('Kurzgesagt', 'UCsXVk37bltHxD1rDPwtNM8Q'),
]
# Long-lived talks kept on the shelf while they stay available. Titles are replaced by YouTube's own.
CLASSICS = ['arj7oStGLkU', 'Hu4Yvq-g7_Y', '5MgBikgcWnY', 'LNHBMFCzznE', 'BHY0FxzoKZE', '5MuIMqhT8DM', 'qzR62JJCMBQ',
            '8jPQjjsBbIc', '_X0mgOOSpLU', 'U6PoUg7jXsA', 'rrkrvAUbU9Y', 'fxbCHn6gE3U', 'RcGyVTAoXEU', 'H14bBuluwB8']
KEY = re.compile(r'\b(brain|memor|attention|focus|cognit|learn|sleep|decision|decid|mind|think|thought|neuro|stress|productiv|habit|'
                 r'motivat|intelligen|creativ|reasoning|concentrat|procrastinat|multitask|distract|burnout|mental|psycholog|work)', re.I)
SKIP = re.compile(r'#shorts|\bsponsored\b|\bgiveaway\b', re.I)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean(text, limit=170):
    text = html.unescape(re.sub(r'<[^>]+>', '', text or ''))
    text = re.sub(r'\s+', ' ', text).strip()
    return text if len(text) <= limit else text[:limit - 1].rstrip() + '…'


def when(text):
    text = (text or '').strip()
    if not text:
        return None
    try:
        d = email.utils.parsedate_to_datetime(text)
    except Exception:
        try:
            d = datetime.datetime.fromisoformat(text.replace('Z', '+00:00'))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc)


def local(tag):
    return tag.rsplit('}', 1)[-1]


def entries(xml_bytes):
    """Yield (title, link, date, extra) from RSS 2.0, RDF or Atom."""
    root = ET.fromstring(xml_bytes)
    for node in root.iter():
        if local(node.tag) not in ('item', 'entry'):
            continue
        title = link = date = vid = None
        for ch in node:
            name = local(ch.tag)
            if name == 'title' and title is None:
                title = ch.text
            elif name == 'link' and link is None:
                link = ch.attrib.get('href') or (ch.text or '').strip() or None
            elif name in ('pubDate', 'published', 'updated', 'date') and date is None:
                date = when(ch.text)
            elif name == 'videoId':
                vid = ch.text
        if title and (link or vid):
            yield title, link, date, vid


def articles():
    out, seen = [], set()
    for source, url, filtered in FEEDS:
        try:
            got = 0
            for title, link, date, _ in entries(fetch(url)):
                title = clean(title)
                if not link or not link.startswith('http') or not title:
                    continue
                if filtered and not KEY.search(title):
                    continue
                if date is None or (NOW - date).days > 45 or date > NOW + datetime.timedelta(days=1):
                    continue
                key = title.lower()
                if key in seen or link in seen:
                    continue
                seen.update((key, link))
                out.append({'title': title, 'url': link, 'source': source, 'date': date.strftime('%Y-%m-%dT%H:%M:%SZ')})
                got += 1
                if got >= 14:
                    break
            print('feed ok   %-24s %d items' % (source, got))
        except Exception as e:  # one bad feed must not stop the run
            print('feed FAIL %-24s %s' % (source, e))
    out.sort(key=lambda i: i['date'], reverse=True)
    return out[:80]


def oembed(video_id):
    """Return (title, channel) if the video is public and embeddable, None if it is gone, False if we could not tell."""
    url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote('https://www.youtube.com/watch?v=' + video_id, safe='')
    try:
        data = json.loads(fetch(url, 15).decode('utf-8'))
        return clean(data.get('title', ''), 120), clean(data.get('author_name', ''), 60)
    except urllib.error.HTTPError as e:
        return None if e.code in (400, 401, 403, 404) else False
    except Exception:
        return False


def videos(previous):
    fresh = []
    for name, cid in CHANNELS:
        try:
            got = 0
            for title, _, date, vid in entries(fetch('https://www.youtube.com/feeds/videos.xml?channel_id=' + cid)):
                title = clean(title, 120)
                if not vid or SKIP.search(title) or not KEY.search(title):
                    continue
                fresh.append({'id': vid, 'title': title, 'channel': name, 'date': date.strftime('%Y-%m-%d') if date else ''})
                got += 1
                if got >= 4:
                    break
            print('channel ok   %-18s %d videos' % (name, got))
        except Exception as e:
            print('channel FAIL %-18s %s' % (name, e))
    fresh.sort(key=lambda v: v['date'], reverse=True)
    known = {v['id']: v for v in previous}
    pool = fresh + [known.get(i, {'id': i, 'title': '', 'channel': '', 'date': ''}) for i in CLASSICS]
    out, seen = [], set()
    for v in pool:
        if v['id'] in seen or not re.fullmatch(r'[\w-]{11}', v['id']):
            continue
        seen.add(v['id'])
        info = oembed(v['id'])
        if info is None:
            print('video dropped (unavailable): ' + v['id'])
            continue
        if info:
            v = dict(v, title=info[0] or v['title'], channel=info[1] or v['channel'])
        elif not v['title']:
            continue  # could not verify and nothing to show
        v.pop('seed', None)
        out.append(v)
        if len(out) >= 36:
            break
    return out


def write(name, items, previous):
    path = os.path.join(ROOT, 'data', name)
    if not items:
        print(name + ': nothing fetched, keeping existing data')
        return
    if items == previous.get('items'):
        print(name + ': unchanged')
        return
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'updated': NOW.strftime('%Y-%m-%dT%H:%M:%SZ'), 'items': items}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('%s: wrote %d items' % (name, len(items)))


def read(name):
    try:
        with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'updated': None, 'items': []}


if __name__ == '__main__':
    old_feed, old_videos = read('feed.json'), read('videos.json')
    write('feed.json', articles(), old_feed)
    write('videos.json', videos(old_videos.get('items', [])), old_videos)
    sys.exit(0)
