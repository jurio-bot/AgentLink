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

## 6. active workerを残したままOwnerを差し替えない

新しいthread targetや次のOwner候補が見えても、現在のOwnerにactive workerが残っているなら先にOwner slotを解放しない。

途中でOwnerだけ差し替えると、旧Owner IDを持つworkerのevidence / receiptを安全に統合できなくなる。Company OSのowner syncはこの状態を `owner_rebind_blocked_active_workers` として止める。

rebindが必要な時の順番は次の通り。

1. active workerの実状態を確認する
2. 完了しているworkerはevidence + receiptで閉じる
3. 未完ならcheckpointへ残して、勝手に別Ownerへ付け替えない
4. worker poolが0になってから本当のOwner handoffを行う

same-threadでCDP targetだけ変わったケースは別で、stable conversation URL + PARTが同じならOwnerを維持してbindingだけ更新する。

この境界は、workerが長く残った時に「新しいOwnerへ乗り換えれば直る」と見せかけて、実際にはreceipt ownershipを壊す事故を防ぐためのもの。

## 7. active workerを残したままOwnerをreleaseしない

Owner差し替えだけでなく、manual clock-outや停止処理でも同じ境界を守る。

active child workerが残っている間にOwnerだけreleaseすると、workerはactiveなのに統合先Ownerが存在しない状態になる。そのためCompany OSのrelease境界では、active workerが1件でもあればOwner releaseを拒否する。

clock-outも先にtimecardをinactive化したりsupervisorを止めたりしない。release preflightが通った時だけclock-outをcommitする。blockされた場合は、現在のtimecardとsupervisorを維持してworkerがreceiptを返せる状態を残す。

検証用temp worldでは、Owner + active workerの状態からreleaseを試すとblockされ、Ownerとworkerがそのまま維持された。worker完了後はreleaseが成功した。clock-outのtemp stateでもblock時にtimecardはactiveのまま、supervisor stopは呼ばれなかった。

## 今回の回帰テスト

same-thread Owner bindingとlong-turn modeの関連テストを実行し、`5/5` PASSを確認した。

確認したのは主に以下。

1. ephemeralなCDP targetではなくstable thread URLをOwner ID判定に使う
2. targetだけ開き直した同一threadを同じlogical Ownerとして扱う
3. 本当のthread handoffは同一Owner扱いしない
4. optimistic revision conflictだけbounded retryする
5. long-turn modeはexpiry前だけactiveになる

追加でCompany OSの既存テスト群へOwner-release guardの回帰テストを加えて再実行し、`13/13` PASSを確認した。active worker中のrelease拒否と、worker完了後のrelease成功を同じテストで確認している。

これはスループットのベンチマークではなく、Owner continuity境界の回帰テスト結果。

長時間workerは「ずっと動かす」より、**誰が何を触っていて、何が本当に終わったかを失わない**方が先に効く。
