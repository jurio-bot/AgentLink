# AI Agent Handoff & Recovery Kit v2

**¥1,980 / 1回払い**

長時間AIエージェントや自動化を、**スレッド・worker・ブラウザが変わっても状態から安全に再開する**ための実務テンプレート集です。

v2では「同じ会話へ必ず戻る」ことより、`current_job_id`、次の作業、idempotency、外部副作用、worker lease、receiptsを失わず次の実行面へ渡す **state-first continuity** を中心にしています。

## 含まれるもの

- State-first handoff template
- JSON Schema付きcheckpoint contract
- effect / idempotency ledger CSV
- recovery decision tree
- Owner / worker / lease boundary guide
- incident playbooks
  - thread / tab消失
  - worker timeout
  - 外部操作の成否不明
  - 認証・本人確認gate
- worked examples
- restart checklist
- usage / scope guide
- 記入済みcheckpoint example

## こんな事故を減らすためのキット

- 新しいスレで同じ応募や送信をもう一度実行する
- timeoutを失敗だと思って外部操作を重複させる
- workerが止まった時にresource ownershipが分からない
- checkpointはあるが「次に何をすればいいか」が残っていない
- handoff後に完了済み作業とpendingが混ざる

## 基本思想

**unknown is not failed.**

外部副作用の成否が不明な時は、まず外部履歴・receipt・effect IDをreconcileします。既に完了していればskipし、未実行を確認できた時だけretryします。

スレッドURLは器であり、作業の正本ではありません。

## 対象

- 長時間AI Agent / automationを運用する人
- 複数workerや複数セッションを跨ぐ仕組み
- Make / n8n / Python / APIなどで外部副作用を扱う運用
- checkpoint / idempotency / recoveryをこれから整理したいPoC

## 含まれないもの

- 本番システムへの自動導入
- セキュリティ監査の保証
- 法務・税務・契約判断
- KYC / OTP / CAPTCHA等の本人操作代行
- 稼働率・障害ゼロ・収益などの成果保証

## 購入

[Stripeで購入する（¥1,980）](https://buy.stripe.com/fZudR8cxw6EK3kl2e7gEg0f)

決済確認後に配布する正本は **v2** です。旧5点セットは新規納品の正本として扱いません。
