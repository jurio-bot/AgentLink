# Services by AI usage

The catalog is split by the customer's starting point. The same deliverable can have very different value depending on whether the customer uses AI at all, uses only free AI, or already pays for a capable model.

## Trials

Trials are not consultation-only products. If the issue is narrow enough, they include one real fix. When the customer continues with the same issue or project, the trial fee is deducted from the main service price.

### PCおためし診断・1修正 — ¥980
Checkout: https://book.stripe.com/7sY6oG9lk0gm6wx8CvgEg0x

One concrete Windows/Linux symptom. Inspect it and, when the cause is narrow enough, apply one safe settings/software fix and verify the basic result.

### Webおためし1か所修正 — ¥1,480
Checkout: https://book.stripe.com/3cIcN4dBA7IOaMNdWPgEg0y

One visible issue on a small site. Reproduce it and, when it is bounded, make one HTML/CSS/JavaScript or publishing-settings fix and verify the page.

### Automationおためし1件修正 — ¥1,980
Checkout: https://book.stripe.com/7sY3cu7dce7caMN2e7gEg0z

One reproducible automation/AI-flow problem. If the cause is narrow, make one small code/configuration fix and run a representative check.

## 1. For people who do not use AI

### PCトラブル解決スプリント — ¥6,800
Checkout: https://book.stripe.com/cNiaEW1SS9QWf336ungEg0o

Windows / Linuxの主要トラブル1件を、状況確認、切り分け、範囲内での設定/ソフトウェア修正、基本動作確認まで進めます。

### 小規模Web修正スプリント — ¥9,800
Checkout: https://book.stripe.com/cNicN4cxwfbg7ABdWPgEg0p

小規模なHTML/CSS/JavaScriptサイトやGitHub Pages等の主要な不具合1〜3件を、再現、修正、公開確認まで進めます。

### 動画仕上げパック — ¥7,800
Checkout: https://book.stripe.com/aFacN4btsd38dYZbOHgEg0q

支給動画1本（目安10分まで）に、簡単なカット、支給字幕、指定箇所の静的ぼかし/モザイク、基本音量調整、書き出しと納品前確認を行います。

## 2. For people who use AI but do not pay for a subscription

These are one-off access products, deliberately below a monthly paid-AI commitment.

### 有料AIリサーチ代行 1回券 — ¥1,980
Checkout: https://buy.stripe.com/7sY7sK2WW2oug772e7gEg0r

テーマ1件を最新Web情報で調べ、主要論点、比較、注意点、参考リンクをまとめます。

### 有料AI文章仕上げ 1回券 — ¥1,480
Checkout: https://buy.stripe.com/eVq00ieFEd38g771a3gEg0s

メモ、下書き、長文テキスト1件を、用途に合わせて整理・推敲し、完成稿へ仕上げます。

### 有料AI発信パック 1回券 — ¥2,480
Checkout: https://buy.stripe.com/fZu7sKapo2oubQRbOHgEg0t

商品・サービス・活動テーマ1件から、紹介文1本、SNS投稿5本、タイトル案10個、FAQ案を一式で作ります。

## 3. For people who already pay for AI

Prompt-only output is not a product for this segment. Fixed-price work stays below ¥10,000 and is intentionally narrow. Larger jobs are scoped after looking at the real code/environment instead of competing with a Pro subscription as a generic checkout item.

### Automation Bug Fix — ¥4,800
Checkout: https://book.stripe.com/28EaEW410gfk6wx05ZgEg0u

One reproducible automation / AI workflow bug. Inspect real code/config/logs, isolate the issue, patch the bounded failure, and run a representative verification test.

### Automation 1-Connection Setup — ¥7,800
Checkout: https://book.stripe.com/14A7sK0OO3sycUV1a3gEg0w

Connect one API, SaaS service, or local process to an existing flow. Implement one trigger or input/output path, configure it, and verify with representative data.

### Agent / RAG Reliability Patch — ¥8,800
Checkout: https://book.stripe.com/4gM00ifJI9QW2gh9GzgEg0v

For one existing Agent/RAG/automation flow, implement only the reliability pieces actually needed: retry boundaries, idempotency, duplicate protection, reconciliation, resume points, or logging, then test a representative failure path.

## Larger work

No fixed ¥30,000 AI checkout. Larger automation, multi-service integration, production deployment, or broad rebuilds are quoted only after the environment, acceptance conditions, and actual work are visible.

## Quality rule

- Trials must include real work when the issue is bounded; diagnosis-only bait is not the goal.
- AI non-users buy completion, not AI education.
- Free-AI users can buy one-off access below a monthly-subscription-sized commitment.
- Paid-AI users are never sold something they can reasonably regenerate in a chat window.
- Fixed-price paid-AI work stays narrow enough that outsourcing one annoying job is cheaper than changing the customer's subscription strategy.
- Larger prices must correspond to real implementation effort after scope is known.
- No fabricated results, reviews, adoption numbers, or performance guarantees.

## Public engineering proof

- [AgentLink](./README.md)
- [RAG Fleet Harness MVP](./CASE_STUDY_RAG_FLEET.md)
- [Receipt Replay Simulator](./demos/receipt-replay-simulator/)
- [Debuggable RAG Operations](./guides/debuggable-rag-operations.md)

Do not put passwords, API keys, private URLs, personal data, or proprietary datasets in a public GitHub Issue.
