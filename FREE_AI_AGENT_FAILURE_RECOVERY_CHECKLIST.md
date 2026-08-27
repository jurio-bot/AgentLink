# Free AI Agent Failure-Recovery Checklist

A compact checklist for reviewing an AI automation or agent workflow before it becomes an expensive retry machine.

Use this for prototypes, internal tools, RAG pipelines, browser automations, API workers, and multi-agent jobs.

## 1. Define the action boundary

- [ ] Each external side effect has a clear start and finish boundary.
- [ ] Read-only observation is separated from write actions.
- [ ] High-impact actions are isolated from ordinary processing.
- [ ] The system knows which actions are safe to retry automatically.

## 2. Make duplicates boring

- [ ] Important writes have an idempotency key or equivalent duplicate guard.
- [ ] A retry cannot silently create a second payment, message, order, application, or publication.
- [ ] Completed work is recorded before the worker moves on.
- [ ] Duplicate detection is tested, not merely assumed.

## 3. Record receipts

For every meaningful action, keep enough evidence to answer:

- What was attempted?
- When was it attempted?
- Which worker performed it?
- Did the external system confirm success?
- What identifier did the external system return?
- Is another attempt safe?

A receipt can be a database row, durable JSON record, event, transaction ID, message ID, commit SHA, or another verifiable artifact.

## 4. Treat uncertainty as a state

- [ ] `success`, `failed`, and `unknown/uncertain` are distinct outcomes.
- [ ] A timeout after sending a request does not automatically mean failure.
- [ ] Uncertain writes trigger reconciliation before replay.
- [ ] Reconciliation checks the external system when possible.

## 5. Design recovery before scale

- [ ] Workers can resume from durable state rather than conversation memory alone.
- [ ] A crashed worker does not permanently own the job.
- [ ] Leases/locks have expiry or stale-owner recovery.
- [ ] Partial completion can resume without restarting the whole workflow.
- [ ] Recovery behavior is exercised in tests.

## 6. Put humans at the right gates

Require explicit human authority for things such as:

- identity/KYC steps
- CAPTCHA or 2FA
- legal attestations and binding agreements
- bank or payout setup
- irreversible high-impact actions
- actions whose real-world consequences are not safely reversible

Do not turn routine low-risk recovery into approval spam.

## 7. Minimum failure drill

Before calling a workflow reliable, deliberately test at least these cases:

1. Worker crashes before an external write.
2. Worker crashes immediately after an external write.
3. External API returns a timeout with unknown outcome.
4. Same job is delivered twice.
5. Lock/lease owner disappears.
6. One dependency is temporarily unavailable.

The desired result is not “nothing ever fails.” The desired result is **failure without uncontrolled duplicate side effects**.

## Next step

If this checklist exposes gaps, the **AI Automation Quickstart Kit** adds a readiness scorecard, PoC planning canvas, API preflight, reliability/recovery worksheet, and ROI estimator:

https://buy.stripe.com/3cIdR8cxw2ou8EFbOHgEg09

For hands-on architecture review or a small implementation PoC, see `SERVICES.md` in this repository.

---

This checklist is an engineering planning aid, not a security audit, legal/compliance review, or guarantee of reliability.
