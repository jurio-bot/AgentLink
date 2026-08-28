<!-- revenue-idempotency: lowticket-publish-AL-CHK-001-github-v1 -->
<!-- revenue-checkout-idempotency: lowticket-connect-AL-CHK-001-stripe-github-v1 -->
# AI自動化 事故防止チェックリスト

価格: ¥500

AI自動化や AI Agent / RAG を、小さく安全に始めるための実務向けチェックリストです。
公開・検証済みの AgentLink の reliability / recovery 設計知見をベースにし、未検証の顧客成果や架空実績は含みません。

## 含まれるもの

- 二重実行を防ぐ pre-flight checklist
- 読み取り・送信・契約・送金などの権限境界
- 失敗時の再開 / incident recovery flow
- idempotency log テンプレート
- action / result / error / timestamp / effect id の記録設計
- KYC / OTP / CAPTCHA など、人間ゲートに残す項目の整理
- 小さな導入例

## 対象

- AI導入をこれから始める個人・小規模チーム
- 自動化を作ったが、復旧や二重実行が不安な人
- RAG / Agent PoC を小さく安全に設計したい人

## 含まれないもの

- 本番環境への無制限実装
- KYC / 法務 / 税務判断
- 成果保証
- 非公開 AgentLink コアコード

## 配布パッケージ

`AL-CHK-001-ai-safety-checklist-v1.zip` として、README、pre-flight checklist、incident recovery flow、idempotency log CSV、automation boundary template、quick example をまとめています。

## 購入

**¥500 / 1回払い** です。Stripe のホスト型決済ページから購入できます。

[AI自動化 事故防止チェックリストを購入する（¥500）](https://buy.stripe.com/4gM3cu410bZ45staKDgEg0d)

決済確認後、購入時のメールアドレスへ ZIP をお送りします。決済前に機密情報の提出は不要です。
