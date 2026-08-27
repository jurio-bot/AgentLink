# AI Automation Retry Decision Tree

A compact decision aid for deciding whether an interrupted automation should retry, reconcile, stop, or escalate.

## 1. Did the action have an external side effect?

Examples: sending a message, creating a record, charging money, publishing content, submitting an application, changing infrastructure.

- **No** → retry is usually safe after checking the failure cause.
- **Yes or unknown** → continue to step 2.

## 2. Is there a durable completion receipt?

- **Yes, completed** → do **not** retry. Treat the action as complete.
- **Yes, failed before the side effect** → repair the cause, then retry with the same idempotency identity when supported.
- **No receipt / uncertain receipt** → do not blindly retry. Reconcile first.

## 3. Can the destination be queried safely?

Look for the intended effect using stable identifiers such as an idempotency key, external record ID, message ID, order ID, job ID, or unique content fingerprint.

- **Effect exists** → record the recovered receipt and skip duplicate execution.
- **Effect does not exist and absence is reliable** → retry once using the original idempotency identity.
- **Cannot determine reliably** → stop automated mutation and escalate for review.

## 4. Is the failure transient?

Examples: timeout, temporary network loss, 429/rate limit, worker crash.

A transient error does **not** prove that the external action failed. If the action crossed an external boundary before the timeout, reconcile before retrying.

## 5. Human-only gates

Never automate around CAPTCHA, 2FA, biometric approval, KYC, tax/bank verification, legal attestation, or binding contract acceptance. Record the blocker and continue unrelated safe work.

## Minimal receipt fields

```text
job_id:
idempotency_key:
action:
destination:
started_at:
finished_at:
side_effect_state: not_started | completed | failed | uncertain
external_reference:
evidence:
next_action: skip | retry | reconcile | human_review
```

## Rule of thumb

**Completed receipt → skip. Known-not-started → retry. Uncertain → reconcile.**

This template is intentionally conservative. It is a planning aid, not a guarantee that a specific integration is safe.

## Go deeper

The paid **AI Automation Quickstart Kit (¥980)** adds an automation-readiness scorecard, PoC planning canvas, API integration preflight, reliability/recovery checklist, ROI estimator, and usage guide. See [`DIGITAL_PRODUCTS.md`](../DIGITAL_PRODUCTS.md).
