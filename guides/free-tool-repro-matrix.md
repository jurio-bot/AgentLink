# Free tool reproducibility matrix

2026-08-30に、ローカル作業treeではなく各repoのfresh `origin/main`を一時ディレクトリへ展開して公開テストを再実行した記録です。後続のcorrectness修正でテスト本数が増えたため、同日中に再検証して現行mainへ更新しています。

| Tool | Verified main | Command | Result | Push CI |
| --- | --- | --- | --- | --- |
| Share Safe Pack | `e97564c` | `python3 -m unittest -v tests.test_share_safe_pack` | 6 / 6 PASS | run `33301098823` success |
| Repo Health Map | `ea62b53` | `python3 -m unittest -v tests.test_repo_health_map` | 4 / 4 PASS | run `33309623237` success |
| Brief to Page | `73bb8f8` | `python3 -m unittest -v tests.test_brief_to_page` | 5 / 5 PASS | run `33297159158` success |
| Creator Stack Picker | `e1487ec` | `node tests/test_usage.js` | 4 assertions PASS | no workflow in current main |
| Creator Gear Router | `8e9dfcd` | `node tests/test_storage.js` | 6 assertions PASS | no workflow in current main |
| Shop Image QA | `3bd1061` | `node tests/test_app.js` | 4 assertions PASS | run `33291769645` success |

合計はPython unittest 15本 + Node assertion 14個 = **29 checks PASS**。

今回の再検証では6repoすべてをfresh `origin/main`からcloneして上記コマンドを実行しました。CIが存在する4repoは、記載したmain SHAに対応するGitHub Actions runが`completed / success`であることもread-backしています。Creator Stack PickerとCreator Gear Routerは現行mainにworkflowが無いため、CIがあるようには記録していません。

この表は「製品品質を保証する数字」ではなく、記載したcommitの公開ソースだけで同じ回帰テストを再現できた、という範囲の証拠です。CI欄も、そのrunで記載コマンドが成功したことだけを示します。

現在このmatrixで確認している境界には、symlink/read scope、secret再掲防止、GitHub credential / dotenv検出、JSON shape、repo-root link boundary、ローカルusage計測、localStorage failure、ローカルファイル名/広告URLのDOM入力が含まれます。
