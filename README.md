# Moxyra Pharma website

Static bilingual (Arabic RTL / English LTR) corporate site served by a Cloudflare **Worker with static assets**.

## Layout
- `site/`: everything that is published (`wrangler.jsonc` points here).
- `source/`: `build.py` (generates 12 files in `site/`), `verify.py`, `baseline.sha256`, `CHANGELOG.md`. Not published.
- `wrangler.jsonc`: deployment config (`assets.directory: ./site`, `404-page`).
- `maintenance/`: the "under development" page used for maintenance mode (also published at `/maintenance/` through the identical copy in `site/maintenance/`).
- Old root files (`ar/ en/ assets/ cover.jpg logo.jpg ...`): legacy copies, no longer published after the switch; kept until a later, separate cleanup.

## Everyday use
1. Edit `source/build.py` (copy, products, CSS, JS), then run `python3 source/build.py`.
2. Check: `python3 source/verify.py`. After an intentional change, regenerate `source/baseline.sha256` and note it in `source/CHANGELOG.md`.
3. Commit to a branch; Cloudflare builds a preview URL for every non-production branch. Merge to `main` only after review (production runs `npx wrangler deploy`).

## Maintenance mode
Set `"directory": "./maintenance"` in `wrangler.jsonc`. Restore with `"./site"`. If you edit the maintenance page, update both `maintenance/` and `site/maintenance/` (verify.py checks they match).

## Rollback (fastest first)
1. Set `"directory": "./"` in `wrangler.jsonc` (the legacy root files still exist).
2. Use the Revert button of the merged Pull Request.
3. Return to the GitHub tag `backup-before-restructure`.
4. Maintenance mode (above).

## Rules
- Never put master images or other large originals in this public repository.
- Do not change `site/` files by hand without updating the baseline.

## بالعربي باختصار
الفولدر `site/` هو الموقع المنشور فقط. ملف `source/build.py` بيولّد 12 ملف داخله، و`source/verify.py` بيتأكد إن كل الملفات مطابقة للبصمات. للرجوع للوضع القديم: غيّر `"./site"` إلى `"./"` في `wrangler.jsonc`. وضع الصيانة: `"./maintenance"`.
