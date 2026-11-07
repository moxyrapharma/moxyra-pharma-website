#!/usr/bin/env python3
"""Compare every file in site/ with source/baseline.sha256 and check that site/maintenance/ equals ../maintenance/.
Run from the repository root:  python3 source/verify.py   (exit code 0 = everything matches)."""
import hashlib, os, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); site = os.path.join(root, "site")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
exp = {}
for l in open(os.path.join(here, "baseline.sha256"), encoding="utf-8"):
    if l.strip():
        d, p = l.rstrip("\n").split("  ", 1); exp[p] = d
act = {os.path.relpath(os.path.join(r, f), site).replace(os.sep, "/"): h(os.path.join(r, f)) for r, _, fs in os.walk(site) for f in fs}
bad = [f"CHANGED {p}" for p in exp if p in act and act[p] != exp[p]] + [f"MISSING {p}" for p in exp if p not in act] + [f"EXTRA {p}" for p in act if p not in exp]
mroot = os.path.join(root, "maintenance")
if os.path.isdir(mroot):
    for f in ("index.html", "404.html"):
        a, b = os.path.join(mroot, f), os.path.join(site, "maintenance", f)
        if not (os.path.exists(a) and os.path.exists(b) and h(a) == h(b)): bad.append(f"MAINTENANCE COPY DIFFERS {f}")
print("\n".join(bad) if bad else f"OK: {len(act)} files match the baseline; maintenance copies identical")
sys.exit(1 if bad else 0)
