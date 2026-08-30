# Site Surface Doctor

静的サイトを公開する前に、ローカルHTMLだけで確認できる壊れ方を読むread-only checkerです。外部URLへアクセスしたり、自動で修正したりはしません。

主に次を確認します。

- 相対リンクや画像・script・sourceのmissing asset
- `img` / `source` の `srcset` に含まれるlocal responsive asset
- root外へ抜ける相対path
- duplicate canonical
- stale text
- sitemapの不足や、opt-inのreverse target check
- `noindex` はinformationalとして分離

`srcset`ではdata URI候補だけをlocal file検査から除外し、同じ`srcset`に混在する通常のlocal candidateは引き続き内部asset検査へ流します。data URIが1つあるだけでresponsive candidate全体を見逃さないようにしています。

```bash
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml --require-local-sitemap-targets --json
```

## Verification

```bash
cd tools
python -m pytest -q test_site_surface_doctor.py
```

clean resultは、ローカルで確認できるsurface integrityが通ったという意味です。外部HTTP、DNS、CDN配信、検索エンジンのindex状態までは保証しません。
