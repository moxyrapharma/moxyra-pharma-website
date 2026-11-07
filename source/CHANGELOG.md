# Changelog: restructure package (Task 1)

## Added
- `site/`: the only folder that is deployed. It holds byte-identical copies of the files that are public today, at the same URLs:
  `ar/ en/ assets/ index.html home.html en.html 404.html robots.txt sitemap.xml _headers _redirects favicon.png cover.jpg logo.jpg`
  plus `maintenance/index.html` and `maintenance/404.html` (public copies so `/maintenance/` and `/maintenance/404.html` keep working).
- `source/build.py`, `source/verify.py`, `source/baseline.sha256` (SHA-256 of every file in `site/`), this changelog, and `README.md`.

## Changed (the only change to deployment files)
- `wrangler.jsonc`: `"directory": "./"` becomes `"directory": "./site"`. Nothing else in that file changed.

## `source/build.py` cleanup (no functional change)
Line numbers refer to the previous version of the file. Each removed block was assigned and then overwritten before it was ever read, so it could not affect the output:
| Removed | Why it was dead |
|---|---|
| line 29 `PRAR = {...}` | variable never used |
| lines 237-248 first `JS = """..."""` | re-assigned at old line 289 before any use |
| lines 262-270 first `vm()` and `slider()` | both functions are redefined later; only the last definition is called |
| lines 289-306 second `JS = r"""..."""` | re-assigned at old line 440 before any use |
| old lines 462, 480, 492, 504 `VER = ...` | intermediate cache-bust hashes; only the final `VER` (computed after all CSS/JS is built) is read when pages are written |
Also changed: a documentation header; output folder is now `../site` (override with `MOXYRA_OUT`). CSS/JS blocks, copy, product data and templates are untouched, and their order is preserved because it is the cascade.
Result: building with the cleaned file reproduces all 12 generated files **byte-for-byte** (SHA-256 identical).

## Not changed
Every file in the repository root (`ar/ en/ assets/ cover.jpg logo.jpg maintenance/ .assetsignore _headers _redirects ...`) is left exactly as it is. Nothing is deleted. After the switch they are simply no longer deployed. Cleanup is a separate, later Pull Request.
