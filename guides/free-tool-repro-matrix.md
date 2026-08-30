# Free tool reproducibility matrix

2026-08-30に、ローカル作業treeではなく各repoのfresh `origin/main`を一時ディレクトリへ展開して公開テストを再実行した記録です。

| Tool | Verified main | Command | Result | Push CI |
| --- | --- | --- | --- | --- |
| Share Safe Pack | `bc3f22f` | `python3 -m unittest -v tests.test_share_safe_pack` | 4 / 4 PASS | run `33293736231` success |
| Repo Health Map | `1b2524f` | `python3 -m unittest -v tests.test_repo_health_map` | 3 / 3 PASS | run `33293741369` success |
| Brief to Page | `7321fa3` | `python3 -m unittest -v tests.test_brief_to_page` | 4 / 4 PASS | run `33293747330` success |
| Creator Stack Picker | `e1487ec` | `node tests/test_usage.js` | 4 assertions PASS | not checked in this batch |
| Creator Gear Router | `8e9dfcd` | `node tests/test_storage.js` | 6 assertions PASS | not checked in this batch |
| Shop Image QA | `71e06be` | `node tests/test_app.js` | 4 assertions PASS | not checked in this batch |

合計はPython unittest 11本 + Node assertion 14個 = **25 checks PASS**。

今回CIを追加した最初の3repoは、workflow追加後のfresh `main`をもう一度cloneして同じ11本を実行し、全件PASSを再確認しました。GitHub Actions側でも各runが`completed / success`になったことをread-backしています。

この表は「製品品質を保証する数字」ではなく、記載したcommitの公開ソースだけで同じ回帰テストを再現できた、という範囲の証拠です。CI欄も、そのrunで記載コマンドが成功したことだけを示します。

特に確認している境界は、symlink/read scope、secret再掲防止、JSON shape、ローカルusage計測、localStorage failure、ローカルファイル名/広告URLのDOM入力です。
