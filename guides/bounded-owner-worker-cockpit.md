# Bounded Owner worker cockpit

長時間の自動化を「1個の巨大処理」にすると、どの処理が何を触っているか分からなくなりやすい。

AgentLink Company OSでは、External Ownerの下に `social / content / oss / distribution` の最大4 workerを置き、resource keyが衝突しない範囲だけ並列に動かす。

## 1. Ownerを1つだけ持つ

Ownerは同じ会話・同じPARTの操縦席を持つ。ブラウザのCDP target IDはタブを開き直すと変わるので、target IDだけでOwner世代を切り替えない。

安定したconversation URL + PARTが同じなら、同じlogical Ownerとしてleaseだけrefreshする。

## 2. workerはresource keyでぶつけない

workerごとに「何を触るか」を先にkey化する。

例:

- `x:account:post:...`
- `repo:owner/name:release:...`
- `site:portfolio:...`
- `content:video-qa:...`

同じrepoや同じ公開面を別workerが同時に書くなら、並列化しない。

## 3. idempotencyを副作用より前に決める

投稿、GitHub更新、releaseなどの外部副作用は、実行前にidempotency keyを決める。

完了済みkeyなら再実行しない。結果が不明ならblind retryではなくread-backしてから判断する。

## 4. workerはevidence + receiptで閉じる

「終わりました」だけではOwnerへ返さない。

最低でも次を残す。

- commit / URL / test resultなどのevidence
- external side effectの有無
- idempotency key
- verified / pending / deferredの区別

たとえばPagesへpush済みでも配信URLがまだ404なら、`source_verified=true / delivery_verified=false` のまま閉じる。

## 5. batchが終わったらcheckpoint → rescore

4 workerが終わった時点でactive workerを0へ戻し、Owner checkpointを保存する。その後、次に価値が高いレーンへworkerを再配置する。

待ち時間を伸ばすための空回しはしない。

## 今回の回帰テスト

same-thread Owner bindingとlong-turn modeの関連テストを実行し、`5/5` PASSを確認した。

確認したのは主に以下。

1. ephemeralなCDP targetではなくstable thread URLをOwner ID判定に使う
2. targetだけ開き直した同一threadを同じlogical Ownerとして扱う
3. 本当のthread handoffは同一Owner扱いしない
4. optimistic revision conflictだけbounded retryする
5. long-turn modeはexpiry前だけactiveになる

これはスループットのベンチマークではなく、Owner continuity境界の回帰テスト結果。

長時間workerは「ずっと動かす」より、**誰が何を触っていて、何が本当に終わったかを失わない**方が先に効く。
