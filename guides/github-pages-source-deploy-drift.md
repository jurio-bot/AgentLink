# GitHub Pages: source と deploy がずれた時の確認メモ

GitHub Pages のURLが `200 OK` だからといって、現在の公開branchにそのページのsourceが残っているとは限らない。

今回、`paper-daemon.github.io` をローカルのmain checkoutだけで検査すると、sitemapに載っている6ルートがsource treeに存在せず、Site Surface Doctorは `sitemap_missing_target` を6件返した。

一方、同じ6ルートを公開URLで確認すると全部 `200` だった。

## 実際に見つかったずれ

対象は次の6ルート。

- `ai-work-router/`
- `creator-delivery-inspector/`
- `creator-stack-picker/`
- `hosting-launch-checker/`
- `shop-image-qa/`
- `vpn-needs-router/`

さらに5ページは `style.css` / `app.js` / `affiliate-config.js` を同一originから相対参照していた。

HTMLだけを戻すと次のdeployで見た目や機能が壊れるので、公開中の依存assetまでinventoryした。復元対象は合計21ファイルになった。

## 復元時にやったこと

1. 公開中の6ページをHTTPで確認
2. 相対参照しているsame-origin assetを列挙
3. 公開中のbytesをそのままmainへ復元
4. 別worktreeで `origin/main` を取り直す
5. Site Surface Doctorをstrict modeで再実行
6. 復元した21ファイルを公開時のcaptureとSHA256比較
7. 6ページ + 15 assetをHTTPで再確認

結果は次の通り。

- Site Surface Doctor: `blocking 6 → 0`
- restored files: `21 / 21` SHA256一致
- public HTTP check: `21 / 21` が `200`
- `noindex` 1件は別ページの既存設定なのでinformationalのまま維持

## ここで大事だった境界

`--require-local-sitemap-targets` は、1つのcheckoutがsite namespace全体を所有している時にだけ使う。

複数projectが同じsiteへdeployする構成なら、ローカルに無いsitemap targetを即broken扱いすると誤検知になる。Site Surface Doctorの既存テストでも、このreverse checkはopt-inとして固定されている。

今回のsiteはmain branchを正本として扱う前提だったので、公開artifactだけに残っていた6ルートをsource/deploy driftとして復元した。

## 判断の順番

`local missing → delete from sitemap` ではなく、先に公開実体を見る。

公開も404ならsitemap cleanup候補。公開は200でsourceだけ無いなら、deploy artifactの残存や別sourceを疑う。依存assetまで含めて正本を特定してから直す方が安全。
