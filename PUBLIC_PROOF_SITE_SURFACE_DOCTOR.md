# Site Surface Doctor — Public Proof

`tools/site_surface_doctor.py` is a dependency-light, read-only preflight checker for static-site surface integrity.

## What it checks

- missing local links and assets
- responsive assets referenced by `img` / `source` `srcset`
- relative paths that escape the selected site root
- duplicate canonical tags
- stale exact-text markers
- sitemap membership and optional reverse target checks
- `noindex` as informational rather than blocking

## Verified responsive-asset boundary

The checker inspects ordinary local `srcset` candidates while ignoring inline `data:` candidates. A mixed `srcset` such as an inline placeholder plus a local 2x image must still validate the local file. This prevents an inline data URI from hiding a missing responsive asset.

The parser also covers a descriptorless inline data candidate followed by a normal local candidate. The `data:` syntax comma is kept inside the inline candidate without swallowing the next responsive asset.

Relevant public commits:

- `cc4a064191b53032eb0bc4e35f8790c5841e3fae` — initial responsive `srcset` checks
- `b0d0a3e650827e110efa216ce486c5b0bf7afdcf` — responsive asset regression tests
- `5b079797763259105bf4bbc466b3b0b022ab0f0f` — scope documentation
- `a97b835a19519f9e54690489d8995040b3279fa2` — mixed data/local candidate handling
- `0004bbb61052dea5f597103bc9180040d751a08f` — mixed candidate regression test
- `3276a26e4801fcaa18a5052c60e30c4a31d5636c` — boundary documentation
- `a478e89292db6900723374b43edd2e00afa8ff48` — descriptorless data candidate boundary parsing
- `db7f18546a797ae5cef5f333463c351e9c240ebb` — descriptorless boundary regression test

## CI evidence

GitHub Actions workflow: `.github/workflows/site-surface-doctor-tests.yml`

Verified runs:

- `33316330533` — success on the mixed data/local candidate implementation and CI setup
- `33316666276` — success on the descriptorless data URI boundary regression

Local command:

```bash
cd tools
python -m unittest -v test_site_surface_doctor.py
```

## Usage

```bash
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml --require-local-sitemap-targets --json
```

## Boundaries

A clean result means the locally inspectable static surface passed the selected checks. It does not verify external HTTP availability, DNS, CDN behavior, search-engine indexing, browser rendering correctness, accessibility quality, or business/content correctness. The checker does not modify the site or make external network requests.
