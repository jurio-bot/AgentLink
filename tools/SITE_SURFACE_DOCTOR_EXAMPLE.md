# Site Surface Doctor: real-world example

A static site can look healthy while still carrying publication mistakes that are easy to miss manually.

During a 2026-08-29 maintenance pass, the checks behind `site_surface_doctor.py` were exercised against the current `paper-daemon.github.io` source.

The useful classes of failure were not limited to broken links. The maintenance work also involved stale naming, canonical hygiene, and sitemap membership for newly added pages.

## What the tool checks

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml \
  --stale-text 'old-brand' \
  --json
```

The current implementation checks:

- missing internal file targets
- path escapes outside the selected root
- duplicate canonical tags
- `noindex` as an informational finding
- exact stale strings
- indexable HTML pages missing from a supplied local sitemap

A stricter reverse sitemap check is available separately for single-checkout sites where every same-origin sitemap URL is expected to exist on disk.

## Why strict sitemap mode is opt-in

The first reverse-check implementation treated every same-origin sitemap URL as belonging to the same checkout. That produced six false positives on the live `paper-daemon.github.io` setup because several paths are served by separate GitHub Pages repositories.

The behavior was changed so normal sitemap membership remains safe for multi-repository Pages setups, while reverse target validation is explicit.

## Verification

After that adjustment:

- the public unit suite passed **8/8 tests**
- the current site source returned **0 blocking findings** in normal sitemap mode
- one intentional `noindex` page remained informational
- strict reverse mode still surfaced the six cross-repository paths, as expected

The point is not that every site needs the same rules. The useful part is turning recurring publication mistakes into a small, read-only preflight instead of rediscovering them by hand each time.
