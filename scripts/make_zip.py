# -*- coding: utf-8 -*-
"""Package a built site into an upload-ready zip.

Includes the generated HTML, assets, PHP backend, styles/scripts and the
robots/llms/sitemap files. Excludes sources, tooling and anything secret.

Usage: python scripts/make_zip.py <site-root> <output.zip>
"""
import os, sys, zipfile

ROOT = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])

SKIP_DIRS = {"src", "scripts", "docs", ".git", ".claude", "node_modules",
             "__pycache__", ".vscode", ".idea", "tests"}
# config.php holds real DB credentials and lives only on the server.
SKIP_FILES = {"config.php", ".gitignore", ".gitattributes", "build.py",
              "package.json", "package-lock.json"}
SKIP_EXT = (".pyc", ".pyo", ".md", ".zip", ".log")

count = 0
size = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        parts = [] if rel_dir == "." else rel_dir.split(os.sep)
        if parts and parts[0] in SKIP_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn in SKIP_FILES or fn.lower().endswith(SKIP_EXT):
                continue
            full = os.path.join(dirpath, fn)
            arc = os.path.relpath(full, ROOT).replace(os.sep, "/")
            z.write(full, arc)
            count += 1
            size += os.path.getsize(full)

print("wrote %s" % OUT)
print("  files: %d" % count)
print("  uncompressed: %.1f MB" % (size / 1024.0 / 1024.0))
print("  zip size: %.1f MB" % (os.path.getsize(OUT) / 1024.0 / 1024.0))
