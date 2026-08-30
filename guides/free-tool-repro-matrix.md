# Free tool reproducibility matrix

2026-08-30に、ローカル作業treeではなく各repoのfresh `origin/main`を一時ディレクトリへ展開して公開テストを再実行した記録です。

| Tool | Verified main | Command | Result |
| --- | --- | --- | --- |
| Share Safe Pack | `7c38a2e` | `python3 -m unittest -v tests/test_share_safe_pack.py` | 4 / 4 PASS |
| Repo Health Map | `a81dd41` | `python3 -m unittest -v tests/test_repo_health_map.py` | 3 / 3 PASS |
| Brief to Page | `0a38390` | `python3 -m unittest -v tests/test_brief_to_page.py` | 4 / 4 PASS |
| Creator Stack Picker | `e1487ec` | `node tests/test_usage.js` | 4 assertions PASS |
| Creator Gear Router | `8e9dfcd` | `node tests/test_storage.js` | 6 assertions PASS |
| Shop Image QA | `71e06be` | `node tests/test_app.js` | 4 assertions PASS |

合計はPython unittest 11本 + Node assertion 14個 = **25 checks PASS**。

この表は「製品品質を保証する数字」ではなく、記載したcommitの公開ソースだけで同じ回帰テストを再現できた、という範囲の証拠です。

特に確認している境界は、symlink/read scope、secret再掲防止、JSON shape、ローカルusage計測、localStorage failure、ローカルファイル名/広告URLのDOM入力です。
