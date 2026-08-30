# Site Surface Doctor — Public Proof

`tools/site_surface_doctor.py` is a dependency-light, read-only preflight checker for static-site and repository surface integrity.

## What it checks

- missing local links and assets
- responsive assets referenced by `img` / `source` `srcset`
- embedded media and frame assets referenced by `video` / `audio` / `track` / `iframe` `src`
- local `video poster` assets
- relative paths that escape the selected site root
- duplicate canonical tags
- stale exact-text markers
- sitemap membership and optional reverse target checks
- incomplete standard MIT text when a root license file explicitly identifies itself as `MIT License`
- `noindex` as informational rather than blocking

## Verified responsive-asset boundary

The checker inspects ordinary local `srcset` candidates while ignoring inline `data:` candidates. A mixed `srcset` such as an inline placeholder plus a local 2x image must still validate the local file. This prevents an inline data URI from hiding a missing responsive asset.

The parser also covers a descriptorless inline data candidate followed by a normal local candidate. The `data:` syntax comma is kept inside the inline candidate without swallowing the next responsive asset.

## Verified embedded-media boundary

Static portfolios often link real delivery samples through `<video>`, `<audio>`, `<track>`, or `<iframe>` instead of ordinary anchors and images. Those local references are now checked with the same missing-file and path-escape rules as other assets. A local `video poster` is checked as well.

This matters for proof pages such as a motion sample: the HTML page can exist and all ordinary links can pass while the actual MP4, caption track, poster, or embedded local frame is missing. Site Surface Doctor now fails that case instead of reporting a clean surface.

## Verified cross-repo Pages boundary

A GitHub Pages user site can link root-relative paths that are actually served by sibling project repositories, such as `/creator-gear-router/`. Those files are intentionally absent from the user-site checkout, so treating every such path as a local missing file creates a false positive.

The checker stays strict by default. A sibling project path is exempt from local file-existence checks only when its root-relative prefix is explicitly supplied with `--allow-external-prefix`. Relative links are still treated as local, and path escapes remain blocking. This option does not verify that the external project is online; it only records that the selected checkout does not own that namespace.

## Verified MIT-license completeness boundary

A repository can say `MIT License` while accidentally shipping only the first half of the standard text. That leaves the public licensing surface inconsistent even when application tests remain green.

Site Surface Doctor now inspects root `LICENSE`, `LICENSE.txt`, and `LICENSE.md` files only when the file explicitly starts with `MIT License`. In that case it requires the standard grant, notice-preservation, warranty disclaimer, liability limitation, and software-connection terms to be present. A truncated MIT file becomes a blocking `incomplete_mit_license` finding.

The boundary is deliberately narrow. A missing license file, a NOTICE-style showcase repository, or another/custom license is not guessed to be MIT and is not flagged by this check. This is a distribution-preflight guard against truncated standard MIT text, not a legal-opinion engine.

Relevant public commits:

- `cc4a064191b53032eb0bc4e35f8790c5841e3fae` — initial responsive `srcset` checks
- `b0d0a3e650827e110efa216ce486c5b0bf7afdcf` — responsive asset regression tests
- `5b079797763259105bf4bbc466b3b0b022ab0f0f` — scope documentation
- `a97b835a19519f9e54690489d8995040b3279fa2` — mixed data/local candidate handling
- `0004bbb61052dea5f597103bc9180040d751a08f` — mixed candidate regression test
- `3276a26e4801fcaa18a5052c60e30c4a31d5636c` — boundary documentation
- `a478e89292db6900723374b43edd2e00afa8ff48` — descriptorless data candidate boundary parsing
- `db7f18546a797ae5cef5f333463c351e9c240ebb` — descriptorless boundary regression test
- `cb9085d5e71964a00f6c2e8cd8873f5c45f9c04d` — embedded media, frame, and poster asset checks
- `62d82ccf49128670bf6b5f1f5b6fa6910f01e491` — embedded media regression test
- `43c64e005f5285eee3e8eea1376755ed02b084a5` — explicit sibling Pages prefix allowance
- `aa34b7d4c48430004df014f9cb62743549d7a126` — cross-repo Pages boundary regression tests
- `532227d177d60d59c82331a19ce317299cbbc946` — incomplete MIT license detection
- `00e2e3f9ddb4215d67db0c45179d7c789c65c48e` — complete/truncated/non-MIT regression coverage
- `14791e1ce3b26dd1bf4b289222194cacf241b4ba` — MIT-boundary documentation and verified implementation head

## CI evidence

GitHub Actions workflow: `.github/workflows/site-surface-doctor-tests.yml`

Verified runs:

- `33316330533` — success on the mixed data/local candidate implementation and CI setup
- `33316666276` — success on the descriptorless data URI boundary regression
- `33317730012` — success on embedded media, frame, and poster asset regression coverage
- `33318516143` — success on explicit cross-repo Pages prefix boundary coverage
- `33325783174` — success on the MIT-license completeness boundary at exact head `14791e1ce3b26dd1bf4b289222194cacf241b4ba`

Local command:

```bash
cd tools
python -m unittest -v test_site_surface_doctor.py
```

## Usage

```bash
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml --allow-external-prefix /creator-gear-router/
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml --require-local-sitemap-targets --json
```

## Boundaries

A clean result means the locally inspectable static/repository surface passed the selected checks. It does not verify external HTTP availability, DNS, CDN behavior, search-engine indexing, browser rendering correctness, accessibility quality, business/content correctness, or legal sufficiency of a license. An allowed external prefix means only that the path is intentionally owned outside the selected checkout; availability still requires a separate readback. The MIT check means only that a file explicitly identifying itself as MIT contains the expected standard sections. The checker does not modify the site or make external network requests.
