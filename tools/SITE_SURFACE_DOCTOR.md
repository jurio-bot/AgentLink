# Site Surface Doctor

`site_surface_doctor.py` is a dependency-free, read-only preflight for small static sites.

It is useful after a rename, page addition, content migration, or before publishing a static site.

## Checks

- missing internal file targets
- paths that escape the selected site root
- duplicate canonical tags
- `noindex` pages as informational findings
- exact stale strings such as an old brand name or domain
- optional local `sitemap.xml` membership for indexable HTML pages

`noindex` is informational because it may be intentional. The other findings are blocking and produce exit code `1`.

## Run

```bash
python tools/site_surface_doctor.py ./site
```

Check for stale names too:

```bash
python tools/site_surface_doctor.py ./site \
  --stale-text 'old-brand' \
  --stale-text 'old.example.com'
```

Check that indexable HTML owned by this checkout appears in the sitemap:

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml
```

If one checkout owns the entire hostname namespace, you can also require every sitemap path to exist locally:

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml \
  --require-local-sitemap-targets
```

Do not enable that strict reverse check when one hostname aggregates sibling deployments, such as multiple GitHub Pages project repositories. In that layout a valid sitemap path may intentionally live outside the selected checkout.

Combine the normal checks and return JSON for CI or another worker:

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml \
  --stale-text 'old-brand' \
  --json
```

The sitemap checks compare URL paths only, so the tool does not need network access or a configured production hostname.

## Real-world example

The companion example documents a live maintenance pass where reverse sitemap validation initially produced false positives because one GitHub Pages hostname aggregated multiple project repositories. The implementation was narrowed after testing against the real deployment instead of assuming one checkout owned every same-origin URL.

- [Read the real-world example](./SITE_SURFACE_DOCTOR_EXAMPLE.md)

## Exit codes

- `0`: no blocking findings
- `1`: one or more blocking findings

## Test

```bash
cd tools
python -m unittest -v test_site_surface_doctor.py
```

The public test suite covers clean sites, stale text, broken internal targets, path escape, duplicate canonical tags, informational `noindex`, valid sitemap membership, missing sitemap entries, malformed sitemap XML, and the opt-in reverse ownership check.

This tool does not modify files, fetch pages, submit sitemaps, or decide whether a `noindex` directive is intentional.