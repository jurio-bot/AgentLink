# Services by AI usage

The catalog is split by the customer's starting point. The same deliverable can have very different value depending on whether the customer uses AI at all, uses only free AI, or already pays for a capable model.

## 1. For people who do not use AI

These are ordinary done-for-you services. The customer does not need to learn AI or prompt anything.

### PCトラブル解決スプリント — ¥6,800
Checkout: https://book.stripe.com/cNiaEW1SS9QWf336ungEg0o

Windows / Linuxの主要トラブル1件を対象に、状況確認、再現・切り分け、範囲内での設定/ソフトウェア修正、基本動作確認まで行います。物理故障の修理、故障ストレージのデータ復旧、規約回避、無制限対応は対象外です。

### 小規模Web修正スプリント — ¥9,800
Checkout: https://book.stripe.com/cNicN4cxwfbg7ABdWPgEg0p

小規模なHTML/CSS/JavaScriptサイトやGitHub Pages等の主要な不具合1〜3件を、再現、修正、公開確認まで進めます。大規模バックエンド、EC移行、無制限デザイン制作は対象外です。

### 動画仕上げパック — ¥7,800
Checkout: https://book.stripe.com/aFacN4btsd38dYZbOHgEg0q

支給動画1本（目安10分まで）に、簡単なカット、支給字幕の焼き込み、指定箇所の静的ぼかし/モザイク、基本音量調整、書き出しと納品前確認を行います。重いVFX/3D、撮影、無制限修正は対象外です。

## 2. For people who use AI but do not pay for a subscription

These are one-off access products. The price is deliberately kept below a typical monthly paid-AI commitment so the customer can pay only when they need a stronger model or deeper work.

### 有料AIリサーチ代行 1回券 — ¥1,980
Checkout: https://buy.stripe.com/7sY7sK2WW2oug772e7gEg0r

テーマ1件を最新Web情報で調べ、主要論点、比較、注意点、参考リンクを短いレポートにまとめます。目安は主要10ソース前後です。

### 有料AI文章仕上げ 1回券 — ¥1,480
Checkout: https://buy.stripe.com/eVq00ieFEd38g771a3gEg0s

メモ、下書き、長文テキスト1件（目安8,000字程度まで）を、用途に合わせて整理・推敲し、そのまま使える完成稿へ仕上げます。元情報にない実績や事実は作りません。

### 有料AI発信パック 1回券 — ¥2,480
Checkout: https://buy.stripe.com/fZu7sKapo2oubQRbOHgEg0t

商品・サービス・活動テーマ1件から、紹介文1本、SNS投稿5本、見出し/タイトル案10個、FAQ案を一式で作ります。架空の実績、レビュー、数字は作りません。

## 3. For people who already pay for AI

For this segment, prompt-only output is not a product. A paying AI user can already generate drafts, checklists, code snippets, and generic reviews. Paid work must cross the boundary into real code, real environments, integration, recovery, or verification.

### Automation Debug & Recovery Sprint — ¥9,800
Checkout: https://buy.stripe.com/8x214meFE4wC5st7yrgEg0g

For one existing automation / AI workflow with a concrete failure. Reproduce the problem from real code/config/logs, isolate the cause, patch the bounded issue, and run a representative verification test.

### Agent / RAG Reliability Hardening Sprint — ¥14,800
Checkout: https://buy.stripe.com/8x2fZg4104wC9IJ4mfgEg08

For one existing Agent, RAG, or automation flow. Implement the reliability work that is actually needed: retry boundaries, idempotency, duplicate protection, unknown-outcome reconciliation, receipts/logs, resume points, and representative failure-path tests.

### Automation Deployment Sprint — ¥29,800
Checkout: https://buy.stripe.com/eVq9AS8hg8MS6wxbOHgEg07

For one real workflow that should be installed and run in the actual environment. Typical scope is roughly two connected services or one local/server process, trigger and workflow implementation, configuration, basic logging/failure handling, representative test data, and restart/handoff instructions.

## Quality rule

- AI non-users buy completion, not AI education.
- Free-AI users can buy one-off access below a monthly-subscription-sized commitment.
- Paid-AI users are never sold something they can reasonably regenerate in a chat window.
- Higher prices must correspond to environment access, implementation, integration, verification, operational risk, or meaningful production effort.
- No fabricated results, reviews, adoption numbers, or performance guarantees.

## Public engineering proof

- [AgentLink](./README.md)
- [RAG Fleet Harness MVP](./CASE_STUDY_RAG_FLEET.md)
- [Receipt Replay Simulator](./demos/receipt-replay-simulator/)
- [Debuggable RAG Operations](./guides/debuggable-rag-operations.md)
- [RAG Trace Check](./tools/rag_trace_check.py)

Do not put passwords, API keys, private URLs, personal data, or proprietary datasets in a public GitHub Issue. Sensitive setup details belong in an appropriate private delivery channel.
