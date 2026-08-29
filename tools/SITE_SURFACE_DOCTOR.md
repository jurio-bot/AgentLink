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

Check sitemap membership:

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml
```

Combine the checks and return JSON for CI or another worker:

```bash
python tools/site_surface_doctor.py ./site \
  --sitemap sitemap.xml \
  --stale-text 'old-brand' \
  --json
```

The sitemap check compares URL paths only, so the tool does not need network access or a configured production hostname.

## Exit codes

- `0`: no blocking findings
- `1`: one or more blocking findings

## Test

```bash
cd tools
python -m unittest -v test_site_surface_doctor.py
```

The public test suite covers clean sites, stale text, broken internal targets, path escape, duplicate canonical tags, informational `noindex`, valid sitemap membership, missing sitemap entries, and malformed sitemap XML.

This tool does not modify files, fetch pages, submit sitemaps, or decide whether a `noindex` directive is intentional.