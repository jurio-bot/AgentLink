# read-onlyでも、どこまで読むかは決める

`read-only` は安全の十分条件ではない。

ファイルを書き換えなくても、scan rootの外を読んだり、秘密値をレポートへコピーしたりすれば境界は破れる。

最近の公開OSSで、実際に3種類の境界を修正した。

## 1. repo scannerがsymlinkの外まで読まない

Repo Health Mapでは、repo内のfile symlinkがroot外を指している時、修正前はリンク先まで読めた。

人工fixtureで確認した結果:

- 修正前: `files=3`, `secret_like=1`
- 修正後: `files=2`, `secret_like=0`

対策は、file判定より先にsymlinkをskipすること。

```python
if p.is_symlink() or not p.is_file():
    continue
```

詳細: https://github.com/paper-daemon/repo-health-map/blob/main/docs/symlink-boundary.md

## 2. manifestのhashでもroot外へ出ない

Repro Capsuleは `requirements.txt` や `pyproject.toml` をSHA256で固定する。

内容をレポートへ保存しなくても、repo内の `requirements.txt` がroot外へのsymlinkなら、hash計算のために外部ファイルを読むことになる。

そこでmanifest候補もsymlinkならskipするようにした。

回帰fixtureでは、外部ファイルを指す `requirements.txt` を置いた後のmanifest結果が `{}` になることを確認。関連テストは `2/2` PASS。

Source: https://github.com/paper-daemon/repro-capsule

## 3. 集計用exampleに秘密値をコピーしない

Data Shape Guardは実JSON/JSONLから型と出現率を推定し、scalar exampleを最大3件保持する。

これはdebugには便利だけど、field名が `api_key` や `token` の場合まで値を保存すると、shape report自体が秘密値のコピーになる。

secret-named pathではexampleを値ではなく `<redacted>` にするよう変更した。

実fixture:

```text
$.api_key -> <redacted>
$.token   -> <redacted>
$.name    -> safe
```

関連テストは `2/2` PASS。

Source: https://github.com/paper-daemon/data-shape-guard

## 境界を3つに分けて考える

読み取り系ツールでは最低でも次を別々に見る。

1. **write scope**: 何を書き換えられるか
2. **read scope**: どのroot・リンク先まで読めるか
3. **output scope**: 読んだ値を何として外へ残すか

「書き込まないから安全」ではなく、**読んでいい範囲と、残していい情報も別に制限する**。

ここで書いた数値は人工fixtureと回帰テストの結果で、実顧客環境の事故件数や漏えい実績ではありません。
