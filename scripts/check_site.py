from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re

root = Path(__file__).resolve().parents[1] / "dist"
expected = {"/", "/projects/", "/projects/sentinel-work/", "/projects/indigo-relay/", "/projects/sentinel/", "/case-studies/", "/case-studies/agent-session-reliability/", "/case-studies/evaluation-release-gates/", "/case-studies/bounded-retrieval/", "/case-studies/observable-infrastructure/", "/about/", "/resume/"}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.main = 0
        self.robots = False
        self.lang = False
        self.nav = False
    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'nav': self.nav = True
        if tag == 'html': self.lang = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'robots': self.robots = a.get('content','') == 'index, follow'
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag in ('script','img','link','iframe') and a.get('src',a.get('href','')).startswith(('http:','https:','//')):
            raise AssertionError('external resource')

actual = {"/" + str(f.parent.relative_to(root)).replace(".", "", 1).strip("/") + ("/" if f.parent != root else "") for f in root.rglob("index.html")}
assert actual == expected, (actual, expected)
link_count = 0
for route in sorted(expected):
    f = root / route.strip("/") / "index.html"
    html = f.read_text()
    parser = Page()
    parser.feed(html)
    assert parser.h1 == 1 and parser.main == 1 and parser.nav and parser.lang and parser.robots, route
    assert "main" in parser.ids, route
    assert "Engineering portfolio" in html, route
    assert not re.search(r'(?i)(https?://docs\.google\.com/|/home/[^/]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-proj-)', html), route
    for href in parser.links:
        u = urlsplit(href)
        assert not u.scheme and not u.netloc, (route, href)
        if u.path:
            assert u.path in expected, (route, href)
        if u.fragment and not u.path:
            assert u.fragment in parser.ids, (route,href)
        link_count += 1
assert "Allow: /" in (root / "robots.txt").read_text()
assert (root / "favicon.svg").exists()
assert not list(root.rglob("*.pdf"))
print(f"PASS: {len(expected)} routes, {link_count} internal links, heading/landmark/robots checks, targeted privacy checks")
