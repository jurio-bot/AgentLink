# Media QA / Subtitle / Privacy-Redaction Services

A small, bounded media-production lane backed by executable QA tools and explicit human review. The goal is not to call ordinary file checks “AI magic”; it is to make repetitive delivery checks reproducible.

## Current public proof

- **[subtitle-workbench](https://github.com/paper-daemon/subtitle-workbench)** — SRT validation, normalization and time shifting
- **[creator-delivery-inspector](https://github.com/paper-daemon/creator-delivery-inspector)** — local ffprobe-based video/audio delivery preflight
- [`tools/srt_doctor.py`](./tools/srt_doctor.py) + regression tests — additional subtitle edge-case checks
- [`tools/video_redaction_filter.py`](./tools/video_redaction_filter.py) + regression tests — reviewable FFmpeg filter-plan generation for bounded static redaction

These are proof of method, not proof of customer outcomes.

## SRT subtitle QA

**Current small-delivery price: ¥3,000**

Typical scope:

- up to 5 SRT files
- numbering and timestamp structure
- start/end ordering
- overlap and empty-cue detection
- malformed timestamp checks
- optional normalization or client-specified time shift
- concise issue summary

Translation, transcription from raw media, major copy rewriting and video editing are outside the base scope.

A matching fixed-scope service is currently published on Coconala.

## Video / audio delivery preflight

**Current small-delivery price: ¥3,000**

Typical scope:

- up to 20 media files
- duration
- width / height
- video and audio codec
- frame rate
- sample rate / channel count
- presence of expected audio/video streams
- CSV manifest for multi-file deliveries

This is metadata and delivery-condition QA. It does not include editing, color work, creative direction, audio repair or a guarantee that a specific platform/client will accept the files.

A matching fixed-scope service is currently published on Coconala.

## Static privacy blur / mosaic assistance

**Reference price: from ¥2,500 for one bounded short clip / reviewed filter plan**

Suitable when the redaction target and time range can be stated explicitly, such as a fixed display region or plate area that stays inside a known rectangle.

The public helper validates time ranges, coordinates, crop size, blur constraints and non-finite values, then emits a reviewable FFmpeg command. It does **not** claim automatic face recognition, person tracking or autonomous censoring decisions.

Moving targets, frame-accurate tracking and long-form/high-volume work require a different scope.

## Quality boundary

Automated checks are first-pass evidence. Final delivery still depends on the client's actual specification and human review where language, visual meaning, privacy judgment or creative quality matters.

## Inquiry

Use the [Media QA / subtitle request form](https://github.com/paper-daemon/AgentLink/issues/new?template=media-qa-request.yml) only for a **non-confidential** scope description.

Do not put private footage, personal data, passwords, API keys, contracts or private download links in a public GitHub Issue. Private transfer details can be agreed after scope is confirmed.

## 日本語まとめ

現在の小規模固定レーンは次の通りです。

- **SRT字幕QA: ¥3,000** — 5ファイルまでを目安に構造・タイムコード・重なり・空字幕を確認
- **動画・音声納品前QA: ¥3,000** — 20ファイルまでを目安にffprobeで基本metadataを確認しCSV manifestを作成
- **静的ぼかし / モザイク補助: ¥2,500〜** — 時間範囲と矩形を明示できる短尺素材向け

公開OSSとテストを技術証拠として使い、自動チェックだけで言語品質・プライバシー判断・納品合格を保証しません。
