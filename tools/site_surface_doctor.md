# Site Surface Doctor

静的サイトを公開する前に、ローカルHTMLとrepo rootだけで確認できる壊れ方を読むread-only checkerです。外部URLへアクセスしたり、自動で修正したりはしません。

主に次を確認します。

- 相対リンクや画像・script・sourceのmissing asset
- `img` / `source` の `srcset` に含まれるlocal responsive asset
- root外へ抜ける相対path
- duplicate canonical
- stale text
- sitemapの不足や、opt-inのreverse target check
- rootの`LICENSE` / `LICENSE.txt` / `LICENSE.md`が`MIT License`を明示する場合、標準MITのgrant / notice / warranty / liability条項が途中で欠けていないか
- `noindex` はinformationalとして分離

`srcset`ではdata URI候補だけをlocal file検査から除外し、同じ`srcset`に混在する通常のlocal candidateは引き続き内部asset検査へ流します。data URIが1つあるだけでresponsive candidate全体を見逃さないようにしています。

MIT検査は、license fileの先頭が明示的に`MIT License`のときだけ有効です。LICENSEが無いrepo、NOTICE型のshowcase、別ライセンスや独自条件を持つrepoをMITとして推測しません。また法的適合性そのものを判定するものではなく、「MITを名乗っているのに標準本文が途中で切れている」という配布事故をpreflightで検出するための境界チェックです。

```bash
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml
python tools/site_surface_doctor.py ./site --sitemap sitemap.xml --require-local-sitemap-targets --json
```

## Verification

```bash
cd tools
python -m pytest -q test_site_surface_doctor.py
```

clean resultは、ローカルで確認できるsurface integrityが通ったという意味です。外部HTTP、DNS、CDN配信、検索エンジンのindex状態、ライセンスの法的妥当性までは保証しません。
