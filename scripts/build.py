"""Build a portable Markdown blog for GitHub Pages. No client-side framework."""
from pathlib import Path
from datetime import date
from html import escape
import json
import math
import os
import re
import shutil
import unicodedata
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import markdown
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
BASE = os.environ.get("SITE_BASE_PATH", SITE.get("basePath", "")).strip("/")
BASE = "/" + BASE if BASE else ""
ORIGIN = os.environ.get("SITE_ORIGIN", SITE.get("url", "")).rstrip("/")
if ORIGIN and urlparse(ORIGIN).scheme not in ("https", "http"):
    raise ValueError("site.url / SITE_ORIGIN must begin with https:// or http://")
if BASE and (".." in BASE or not re.fullmatch(r"/[A-Za-z0-9._~/-]+", BASE)):
    raise ValueError("Invalid base path")


def e(value):
    return escape(str(value), quote=True)


def url(path=""):
    return BASE + "/" + path.lstrip("/")


def slug(value):
    value = unicodedata.normalize("NFKD", value.lower().replace("đ", "d"))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "bai-viet"


def frontmatter(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path.name}: missing frontmatter")
    head, body = text[4:].split("\n---\n", 1)
    data = {}
    for line in head.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key, sep, val = line.partition(":")
        if not sep:
            raise ValueError(f"{path.name}: invalid metadata line {line}")
        val = val.strip()
        if val.startswith(("[", '"')) or val in ("true", "false"):
            val = json.loads(val)
        elif len(val) > 1 and val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        data[key.strip()] = val
    for key in ("title", "description", "date", "category"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{path.name}: missing or invalid {key}")
    data["date"] = date.fromisoformat(data["date"])
    if not isinstance(data.get("tags", []), list) or any(not isinstance(x, str) for x in data.get("tags", [])):
        raise ValueError(f"{path.name}: tags must be a JSON array of strings")
    data["tags"] = data.get("tags", [])
    data["slug"] = slug(data.get("slug") or re.sub(r"^\d+-", "", path.stem))
    data["body"] = body.strip()
    data["minutes"] = max(1, math.ceil(len(re.findall(r"\S+", body)) / 220))
    data["path"] = f"posts/{data['slug']}/"
    return data


def render_markdown(body):
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "codehilite", "sane_lists"],
        extension_configs={"codehilite": {"guess_lang": False}, "toc": {"slugify": lambda s, sep: slug(s), "toc_depth": "2-3"}})
    rendered = md.convert(body)
    # Rewrite real HTML attributes only; preserve code examples verbatim.
    def asset_attributes(match):
        return re.sub(r'''(\b(?:src|href)=["'])/?assets/''', lambda attr: attr[1] + url("assets/"), match[0])
    rendered = re.sub(r"<(?:a|img|source|video|audio)\b[^>]*>", asset_attributes, rendered)
    rendered = re.sub(r"<table>(.*?)</table>", r'<div class="table-scroll"><table>\1</table></div>', rendered, flags=re.S)
    return rendered, md.toc if md.toc_tokens else ""


POSTS = [frontmatter(p) for p in sorted((ROOT / "content/posts").glob("*.md"))]
POSTS = sorted((p for p in POSTS if not p.get("draft", False)), key=lambda p: p["date"], reverse=True)
if len({p["slug"] for p in POSTS}) != len(POSTS):
    raise ValueError("Two posts have the same slug; rename the files or set unique slug fields.")
CATEGORIES = list(dict.fromkeys(p["category"] for p in POSTS))


def arrow():
    return '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def mark():
    return '<span class="brand-mark" aria-hidden="true"><span></span><span></span><span></span></span>'


def sidebar(active):
    nav = []
    for key, label, path in [("blog", "Bài viết", ""), ("archive", "Lưu trữ", "archive/"), ("about", "Giới thiệu", "about/")]:
        current = ' aria-current="page"' if active == key else ""
        count = f'<span class="nav-count">{len(POSTS):02d}</span>' if key == "blog" else ""
        nav.append(f'<a href="{url(path)}"{current}>{label}{count}</a>')
    social = []
    github = SITE.get("github", "")
    if github.startswith("https://"):
        social.append(f'<a href="{e(github)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>')
    email = SITE.get("email", "")
    if email and "@" in email:
        social.append(f'<a href="mailto:{e(email)}">Email ↗</a>')
    if ORIGIN:
        social.append(f'<a href="{url("feed.xml")}">RSS ↗</a>')
    return f'''<a class="skip-link" href="#main">Đến nội dung</a>
    <header class="site-header">
      <div class="brand"><a href="{url()}" aria-label="{e(SITE['title'])} — Trang chủ">{mark()}<span>{e(SITE['title'])}<span class="brand-dot">.</span></span></a>
      <p>{e(SITE['tagline'])}</p></div>
      <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span>☰</span></button>
      <nav id="site-nav" aria-label="Điều hướng chính">{''.join(nav)}</nav>
      <div class="header-social">{''.join(social)}</div>
    </header>'''


def page(title, description, content, active="blog", path="", kind="website"):
    canonical = f'<link rel="canonical" href="{e(ORIGIN + url(path))}"><meta property="og:url" content="{e(ORIGIN + url(path))}">' if ORIGIN else ""
    rss = f'<link rel="alternate" type="application/rss+xml" title="{e(SITE["title"])}" href="{url("feed.xml")}">' if ORIGIN else ""
    return f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {e(SITE['title'])}</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#111312"><meta property="og:locale" content="vi_VN"><meta property="og:type" content="{kind}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:site_name" content="{e(SITE['title'])}">
{canonical}{rss}<link rel="icon" type="image/svg+xml" href="{url('assets/favicon.svg')}"><link rel="preload" href="{url('assets/fonts/GeistMono.woff2')}" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{url('assets/style.css')}">
<script src="{url('assets/main.js')}" defer></script></head><body>{sidebar(active)}
<main id="main" tabindex="-1">{content}<footer class="footer"><a class="footer-brand" href="{url()}">{e(SITE['title'])}<span class="accent">.</span></a><div class="footer-bottom"><span>© {max((p['date'].year for p in POSTS), default=date.today().year)} · {e(SITE['tagline'])}</span><span>Cảm hứng từ <a href="https://andersnoren.se/teman/norrsken-wordpress-theme/" target="_blank" rel="noopener noreferrer">Norrsken ↗</a></span><a href="#main">Lên đầu trang ↑</a></div></footer></main>
<div class="toast" role="status" aria-live="polite"></div></body></html>'''


def cover_svg(index):
    colors = [("#65edbb", "#4487cb"), ("#bc9af7", "#4d69ad"), ("#d6ce8e", "#408a73"), ("#e9a5bc", "#614581")]
    glow, secondary = colors[index % 4]
    defs = f'''<defs><radialGradient id="sky"><stop stop-color="{secondary}" stop-opacity=".5"/><stop offset="1" stop-color="#0e181d"/></radialGradient><linearGradient id="aurora" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{glow}" stop-opacity=".05"/><stop offset=".48" stop-color="{glow}" stop-opacity=".7"/><stop offset="1" stop-color="{secondary}" stop-opacity=".1"/></linearGradient><filter id="blur"><feGaussianBlur stdDeviation="22"/></filter></defs>'''
    backdrop = f'''<rect width="800" height="500" fill="#0e181d"/><ellipse cx="420" cy="220" rx="500" ry="360" fill="url(#sky)"/><g filter="url(#blur)" fill="none" stroke="url(#aurora)"><path d="M-90 330Q130-90 340 180T890 10" stroke-width="90"/><path d="M-90 400Q180-80 340 250T890 90" stroke-width="23"/></g>'''
    stars = ''.join(f'<circle cx="{(i * 173 + 31) % 800}" cy="{(i * 79 + 23) % 340}" r="{.6 + (i % 3) * .3}" fill="#d8eee5" opacity="{.2 + (i % 5) * .12}"/>' for i in range(48))
    if index % 4 == 0:
        art = '''<path d="M0 416 85 345 157 381 264 253 364 360 440 300 568 398 683 326 800 410V500H0Z" fill="#101f28"/><path d="m176 359 88-106 100 107-64-40-34-24-20 37-24-14z" fill="#628c97" opacity=".5"/><path d="M0 459 117 419 225 444 387 382 537 454 652 414 800 452V500H0Z" fill="#0a131a"/><path d="M0 475q200-25 400 0t400 0" fill="none" stroke="#65c8a8" opacity=".35"/><text x="40" y="461" fill="#c1e6d4" font-family="monospace" font-size="13" letter-spacing="3">01 / START SOMEWHERE</text>'''
    elif index % 4 == 1:
        art = f'''<g transform="translate(108 89)"><rect width="584" height="330" rx="12" fill="#10151b" stroke="#7d719d" stroke-opacity=".55"/><path d="M0 49H584" stroke="#605f71" stroke-opacity=".4"/><circle cx="25" cy="25" r="5" fill="#db869e"/><circle cx="46" cy="25" r="5" fill="#d8c38a"/><circle cx="67" cy="25" r="5" fill="#8bd3b0"/><text x="40" y="111" fill="{glow}" font-family="monospace" font-size="21">$ decode --follow-the-clue</text><text x="40" y="158" fill="#9ba5b8" font-family="monospace" font-size="17">observe → question → verify</text><text x="40" y="233" fill="#b3d9c8" font-family="monospace" font-size="28">flag&#123;keep_looking&#125;</text><path d="M40 275h14" stroke="{glow}" stroke-width="3"/></g>'''
    elif index % 4 == 2:
        art = f'''<g transform="translate(224 59) rotate(7 176 190)"><rect width="352" height="382" rx="5" fill="#182222" stroke="#a5bdb0" stroke-opacity=".6"/><path d="M43 55h169" stroke="{glow}" stroke-width="6"/><g stroke="#738f81" stroke-width="3" opacity=".7"><path d="M43 99h262M43 122h233M43 145h243M43 198h261M43 221h201M43 244h231M43 297h260M43 320h205"/></g><text x="43" y="358" fill="#9da9a0" font-size="13" font-family="monospace">learn. make. remember.</text></g><circle cx="629" cy="144" r="40" fill="none" stroke="{glow}" stroke-opacity=".7"/><path d="m610 144 13 13 25-28" fill="none" stroke="{glow}" stroke-width="3"/>'''
    else:
        art = f'''<g fill="none" stroke="#99adb8" stroke-opacity=".3"><circle cx="400" cy="250" r="158"/><circle cx="400" cy="250" r="112"/><path d="M78 250h644M400 25v450"/></g><g transform="translate(400 250)"><path d="m0-115 23 91 91 24-91 23-23 92-24-92-91-23 91-24z" fill="{glow}" fill-opacity=".8"/><circle r="37" fill="#19232a" stroke="{glow}" stroke-width="2"/><circle r="7" fill="{glow}"/></g><text x="38" y="455" fill="#cbb7c7" font-family="monospace" font-size="13" letter-spacing="2">SMALL TOOLS / NEW DIRECTIONS</text>'''
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">' + defs + backdrop + stars + art + '</svg>'


def cover_image(post, index):
    cover = post.get("cover", "")
    if cover:
        if not isinstance(cover, str):
            raise ValueError("cover must be a path or HTTPS URL")
        if cover.startswith("https://"):
            return e(cover)
        relative = cover.lstrip("/")
        image = (ROOT / relative).resolve()
        if not relative.startswith("assets/") or not image.is_relative_to((ROOT / "assets").resolve()) or not image.is_file():
            raise ValueError(f"Cover image not found in assets/: {cover}")
        return e(url(relative))
    return url(f"assets/cover-{index % 4}.svg")


def card(post, index):
    search = " ".join([post["title"], post["description"], post["category"], *post["tags"]])
    return f'''<article class="post-card" data-category="{e(post['category'])}" data-search="{e(search)}" style="--card-accent:{['#93e9be','#baa1f8','#e2d390','#e99fbe'][index % 4]}">
      <a class="cover-link" href="{url(post['path'])}" tabindex="-1" aria-hidden="true"><img src="{cover_image(post, index)}" alt="" width="800" height="500" {'loading="lazy"' if index > 2 else 'fetchpriority="high"'}><span class="cover-arrow">{arrow()}</span></a>
      <div class="post-meta"><a href="{url('categories/' + slug(post['category']) + '/')}" class="category">{e(post['category'])}</a><span>{post['minutes']} phút đọc</span></div>
      <h2><a href="{url(post['path'])}">{e(post['title'])}</a></h2><p>{e(post['description'])}</p><time datetime="{post['date'].isoformat()}">{post['date'].strftime('%d.%m.%Y')}</time>
    </article>'''


def home():
    filters = '<a href="' + url() + '" class="filter active" data-filter="" aria-current="true">Tất cả <span>' + str(len(POSTS)) + '</span></a>'
    for cat in CATEGORIES:
        filters += f'<a class="filter" data-filter="{e(cat)}" href="{url("categories/" + slug(cat) + "/")}">{e(cat)} <span>{sum(p["category"] == cat for p in POSTS)}</span></a>'
    cards = ''.join(card(p, i) for i, p in enumerate(POSTS))
    options = ''.join(f'<option value="{e(cat)}">{e(cat)} ({sum(p["category"] == cat for p in POSTS)})</option>' for cat in CATEGORIES)
    return f'''<header class="hero"><p class="eyebrow">BLOG / WRITEUP / NHỮNG ĐIỀU ĐÃ HỌC</p><h1>{e(SITE['title'])}<span class="accent">.</span></h1><div class="aurora-rule" aria-hidden="true"></div><p class="hero-description">{e(SITE['description'])}</p>
    <div class="discovery-tools" hidden data-filter-tools><div class="category-select"><label for="category" class="sr-only">Chuyên mục</label><select id="category"><option value="">Tất cả chuyên mục</option>{options}</select><span aria-hidden="true">⌄</span></div><div class="search-box" hidden data-search-box><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.7"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="1.7"/></svg><label for="search" class="sr-only">Tìm bài viết</label><input id="search" type="search" placeholder="Tìm bài viết…" autocomplete="off"><kbd>/</kbd></div></div>
    <noscript><nav class="filters" aria-label="Chuyên mục">{filters}</nav></noscript></header>
    <section class="journal" aria-label="Bài viết"><div class="section-heading"><h2>Bài viết mới nhất</h2><span class="total-label">{len(POSTS):02d} bài viết <span aria-hidden="true">↘</span></span></div>
    <p class="sr-only" id="search-status" role="status" aria-live="polite"></p><div class="post-grid" data-article-grid>{cards}</div>
    <div class="empty-state" hidden><span aria-hidden="true">⌕</span><h3>Chưa tìm thấy bài viết</h3><p>Thử một từ khóa khác hoặc xem lại tất cả bài viết nhé.</p><button type="button" data-reset>Xem tất cả bài viết {arrow()}</button></div>
    <div class="end-note"><span class="status-dot" aria-hidden="true"></span> Còn nhiều điều hay để ghi lại.</div></section>'''


def article(post, index):
    rendered, toc = render_markdown(post['body'])
    toc_html = f'<details class="toc" open><summary>Trong bài viết này</summary>{toc}</details>' if toc else ""
    tags = ''.join(f'<a href="{url("tags/" + slug(t) + "/")}">#{e(t)}</a>' for t in post["tags"])
    next_post = POSTS[(index + 1) % len(POSTS)] if len(POSTS) > 1 else None
    next_html = f'<a class="next-post" href="{url(next_post["path"])}"><span>ĐỌC TIẾP</span><strong>{e(next_post["title"])}</strong>{arrow()}</a>' if next_post else ""
    return f'''<div class="topline"><a class="back-link" href="{url()}">← Tất cả bài viết</a><span>BLOG & WRITEUP</span></div>
    <article class="article"><header class="article-header"><a class="category" href="{url('categories/' + slug(post['category']) + '/')}">{e(post['category'])}</a><h1>{e(post['title'])}</h1><p class="article-description">{e(post['description'])}</p><div class="article-meta"><span>{e(SITE['author'])}</span><span>·</span><time datetime="{post['date'].isoformat()}">{post['date'].strftime('%d.%m.%Y')}</time><span>·</span><span>{post['minutes']} phút đọc</span></div></header>
    <img class="article-cover" src="{cover_image(post, index)}" width="800" height="500" alt="">
    <div class="article-layout"><div class="prose">{rendered}<div class="article-tags">{tags}</div><div class="article-actions"><button type="button" data-copy-link hidden>Sao chép liên kết ↗</button><span class="copy-status" role="status"></span></div></div><aside class="article-aside">{toc_html}</aside></div>{next_html}</article>'''


def listing(posts, title, description, tag=None):
    years = {}
    for p in posts:
        years.setdefault(p["date"].year, []).append(p)
    rows = ""
    for year, items in years.items():
        rows += f'<section class="archive-year"><h2>{year}<span>{len(items):02d} bài</span></h2><div>'
        for p in items:
            rows += f'<a class="archive-row" href="{url(p["path"])}"><time datetime="{p["date"].isoformat()}">{p["date"].strftime("%d.%m")}</time><span><small>{e(p["category"])}</small><strong>{e(p["title"])}</strong></span>{arrow()}</a>'
        rows += '</div></section>'
    return f'''<div class="topline"><a class="back-link" href="{url()}">← Tất cả bài viết</a><span>{len(posts):02d} BÀI VIẾT</span></div><header class="page-header"><p class="eyebrow">{e(tag or 'THEO DÒNG THỜI GIAN')}</p><h1>{e(title)}<span class="accent">.</span></h1><p>{e(description)}</p></header>{rows}'''


def write(path, text):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def main():
    # Rebuild only the fixed project dist directory, never a user-selected path.
    if OUT.exists():
        if OUT.resolve().parent != ROOT.resolve() or OUT.name != "dist":
            raise ValueError("Refusing to clean output outside project")
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for i in range(4):
        write(f"assets/cover-{i}.svg", cover_svg(i))
    write("assets/highlight.css", HtmlFormatter(style="monokai").get_style_defs(".codehilite"))
    write("index.html", page("Bài viết", SITE['description'], home()))
    paths = [""]
    for i, post in enumerate(POSTS):
        write(post['path'] + 'index.html', page(post['title'], post['description'], article(post, i), path=post['path'], kind='article'))
        paths.append(post['path'])
    write("archive/index.html", page("Lưu trữ", "Tất cả bài viết theo dòng thời gian.", listing(POSTS, "Lưu trữ", "Từng bài viết, từng bước nhỏ trên hành trình học hỏi."), active="archive", path="archive/"))
    paths.append("archive/")
    about_body, _ = render_markdown((ROOT / "content/about.md").read_text(encoding="utf-8"))
    about = f'<div class="topline"><span>VỀ BLOG NÀY</span><span>RẤT VUI VÌ BẠN Ở ĐÂY</span></div><div class="about-intro">{mark()}<p class="eyebrow">XIN CHÀO, MÌNH LÀ {e(SITE["author"].upper())}</p></div><article class="prose about-prose">{about_body}</article>'
    write("about/index.html", page("Giới thiệu", "Một chút về góc nhỏ này.", about, active="about", path="about/"))
    paths.append("about/")
    for kind, values in [("categories", CATEGORIES), ("tags", sorted({t for p in POSTS for t in p["tags"]}))]:
        slugs = {}
        for value in values:
            if slug(value) in slugs and slugs[slug(value)] != value:
                raise ValueError(f"Conflicting {kind} slugs: {value}")
            slugs[slug(value)] = value
            selected = [p for p in POSTS if p['category'] == value] if kind == "categories" else [p for p in POSTS if value in p['tags']]
            path = f"{kind}/{slug(value)}/"
            body = listing(selected, value, "Những bài viết cùng một mối quan tâm.", tag="CHUYÊN MỤC" if kind == "categories" else "CHỦ ĐỀ")
            write(path + "index.html", page(value, f"Các bài viết về {value}.", body, path=path))
            paths.append(path)
    missing = f'<div class="not-found"><span>404</span><h1>Trang này đi lạc rồi.</h1><p>Có thể liên kết đã thay đổi. Những bài viết vẫn đang chờ bạn ở trang chủ.</p><a class="button" href="{url()}">Về trang chủ {arrow()}</a></div>'
    write("404.html", page("Không tìm thấy trang", "Trang bạn tìm không còn ở đây.", missing, active=""))
    write(".nojekyll", "")
    if ORIGIN:
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        for key, val in [("title", SITE['title']), ("link", ORIGIN + url()), ("description", SITE['description']), ("language", "vi")]:
            ET.SubElement(channel, key).text = val
        for p in POSTS:
            item = ET.SubElement(channel, "item")
            for key, val in [("title", p['title']), ("link", ORIGIN + url(p['path'])), ("guid", ORIGIN + url(p['path'])), ("description", p['description']), ("pubDate", p['date'].strftime('%a, %d %b %Y 00:00:00 +0700'))]:
                ET.SubElement(item, key).text = val
        write("feed.xml", '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(rss, encoding="unicode"))
        sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for path in paths:
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = ORIGIN + url(path)
        write("sitemap.xml", '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(sitemap, encoding="unicode"))
        write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}{url('sitemap.xml')}\n")
    else:
        write("robots.txt", "User-agent: *\nAllow: /\n")
    print(f"Built {len(POSTS)} posts and {len(paths)} pages to {OUT}; base path: {BASE or '/'}")


if __name__ == '__main__':
    main()
