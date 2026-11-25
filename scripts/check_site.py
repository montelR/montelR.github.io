from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re

root = Path(__file__).resolve().parents[1] / "dist"
expected = {"/evaluation-lab/", "/", "/projects/", "/projects/sentinel-work/", "/projects/indigo-relay/", "/projects/sentinel/", "/case-studies/", "/case-studies/agent-session-reliability/", "/case-studies/evaluation-release-gates/", "/case-studies/bounded-retrieval/", "/case-studies/observable-infrastructure/", "/about/", "/resume/", "/contact/"}
allowed_contact_links = {"https://www.linkedin.com/in/montel-rice-6b89a544b", "https://github.com/montelR"}
contact_links = set()

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.downloads = []
        self.ids = set()
        self.h1 = 0
        self.main = 0
        self.robots = False
        self.lang = False
        self.nav = False
        self.in_primary_nav = False
        self.primary_nav_links = []
        self.forms = []
        self.fields = {}
    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'nav':
            self.nav = True
            self.in_primary_nav = a.get('aria-label') == 'Primary'
        if tag == 'form': self.forms.append(a)
        if tag in ('input', 'textarea') and a.get('name'): self.fields[a['name']] = a
        if tag == 'html': self.lang = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'robots': self.robots = a.get('content','') == 'index, follow'
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
            if self.in_primary_nav: self.primary_nav_links.append((a['href'], a.get('aria-current')))
            if 'download' in a: self.downloads.append((a['href'], a['download']))
        if tag in ('script','img','link','iframe') and a.get('src',a.get('href','')).startswith(('http:','https:','//')):
            raise AssertionError('external resource')

    def handle_endtag(self, tag):
        if tag == "nav": self.in_primary_nav = False

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
    assert parser.primary_nav_links == [(link, "page" if link == route else None) for link in ("/", "/about/", "/projects/", "/case-studies/", "/evaluation-lab/", "/resume/", "/contact/")], route
    assert parser.downloads == ([("/Montel_Rice_Resume.pdf", "Montel_Rice_Resume.pdf")] if route == "/resume/" else []), route
    if route == "/contact/":
        assert len(parser.forms) == 1
        assert parser.forms[0].get("action") == "https://api.web3forms.com/submit"
        assert parser.forms[0].get("method", "").lower() == "post"
        assert re.fullmatch(r"[0-9a-f-]{36}", parser.fields["access_key"]["value"])
        assert parser.fields["access_key"]["type"] == "hidden"
        assert parser.fields["email"]["type"] == "email"
        assert all("required" in parser.fields[k] for k in ("email", "subject", "message"))
        assert "hidden" in parser.fields["botcheck"]
        assert not re.search(r"mailto:|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html.replace("you@example.com", ""))
    else:
        assert not parser.forms
    assert "Engineering portfolio" in html, route
    assert not re.search(r'(?i)(https?://docs\.google\.com/|/home/[^/]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-proj-)', html), route
    for href in parser.links:
        u = urlsplit(href)
        if u.scheme or u.netloc:
            assert route == "/contact/" and href in allowed_contact_links, (route, href)
            contact_links.add(href)
            continue
        assert not u.scheme and not u.netloc, (route, href)
        if u.path:
            assert u.path in expected or (route == "/resume/" and u.path == "/Montel_Rice_Resume.pdf"), (route, href)
        if u.fragment and not u.path:
            assert u.fragment in parser.ids, (route,href)
        link_count += 1
assert contact_links == allowed_contact_links, contact_links
assert "Allow: /" in (root / "robots.txt").read_text()
assert (root / "favicon.svg").exists()
assert sorted(p.relative_to(root).as_posix() for p in root.rglob("*.pdf")) == ["Montel_Rice_Resume.pdf"]
assert (root / "Montel_Rice_Resume.pdf").read_bytes().startswith(b"%PDF-")
print(f"PASS: {len(expected)} routes, {link_count} internal links, heading/landmark/robots checks, targeted privacy checks, two allowlisted professional profile links")
