# -*- coding: utf-8 -*-
"""Resolve internal links inside localized page content.

The hand-written localized pages were written with English slugs behind the
language prefix (e.g. /ko/taxi-skradin-to-split/), but generated route pages
use per-language slugs (/ko/taxi-skradin-split/). This walks every localized
page and repoints each /<lang>/<slug>/ link:

  1. link already valid for that language  -> leave it
  2. slug is the ENGLISH slug of a page that exists in this language
                                           -> repoint to that language's slug
  3. otherwise                             -> fall back to the English page

Safe to re-run; it only rewrites links that are currently wrong.

Usage: python scripts/fix_page_links.py <site-root>
"""
import os, re, io, json, sys

ROOT = os.path.abspath(sys.argv[1])
PAGES = os.path.join(ROOT, "src", "pages")

slug_of = {}      # (pid, lang) -> slug
langs_of = {}     # pid -> set(langs)
for pid in os.listdir(PAGES):
    pd = os.path.join(PAGES, pid)
    if not os.path.isdir(pd):
        continue
    for lang in os.listdir(pd):
        mp = os.path.join(pd, lang, "meta.json")
        if not os.path.isfile(mp):
            continue
        try:
            slug_of[(pid, lang)] = json.load(io.open(mp, encoding="utf-8")).get("slug", "")
            langs_of.setdefault(pid, set()).add(lang)
        except Exception:
            pass

pid_by_en_slug = {}
valid = {}        # lang -> set of slugs
for (pid, lang), slug in slug_of.items():
    valid.setdefault(lang, set()).add(slug)
    if lang == "en":
        pid_by_en_slug[slug] = pid

repointed = 0
fellback = 0
touched = set()

for (pid, lang), _ in list(slug_of.items()):
    if lang == "en":
        continue
    cp = os.path.join(PAGES, pid, lang, "content.html")
    if not os.path.isfile(cp):
        continue
    html = io.open(cp, encoding="utf-8", errors="ignore").read()
    stats = [0, 0]

    def repl(m):
        path = m.group(1)
        slug = path.rstrip("/")
        if slug in valid.get(lang, ()):
            return m.group(0)                      # already correct
        target_pid = pid_by_en_slug.get(slug)
        if target_pid and lang in langs_of.get(target_pid, ()):
            stats[0] += 1
            s = slug_of[(target_pid, lang)]
            return 'href="/%s/%s"' % (lang, s + "/" if s else "")
        if slug in pid_by_en_slug:                 # English page exists
            stats[1] += 1
            return 'href="/%s"' % path
        return m.group(0)                          # unknown, leave alone

    new = re.sub(r'href="/%s/([^"]*)"' % re.escape(lang), repl, html)
    if new != html:
        try:
            io.open(cp, "w", encoding="utf-8").write(new)
        except OSError as e:
            # File busy (an agent may still be writing it). Report and continue;
            # this script is safe to run again.
            print("  SKIPPED (busy):", pid + "/" + lang, e)
            continue
        repointed += stats[0]
        fellback += stats[1]
        touched.add("%s/%s" % (pid, lang))

print("pages updated:", len(touched))
print("links repointed to the localized page:", repointed)
print("links fallen back to English:", fellback)
