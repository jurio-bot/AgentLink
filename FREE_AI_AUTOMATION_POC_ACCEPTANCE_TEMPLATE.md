# Free AI Automation PoC Acceptance Template

A small acceptance checklist for AI automation proofs of concept. Use it before calling a PoC "done".

## 1. Scope

- [ ] One workflow or use case is named clearly.
- [ ] Inputs and expected outputs are documented.
- [ ] Out-of-scope behavior is explicit.
- [ ] Human approval points are identified.

## 2. Success criteria

Write measurable criteria before testing:

| Criterion | Target | Evidence |
|---|---:|---|
| Correct output | ___ | ___ |
| Max processing time | ___ | ___ |
| Manual steps remaining | ___ | ___ |
| Failed-run recovery | ___ | ___ |

## 3. Reliability

- [ ] A repeated request does not accidentally duplicate an external side effect.
- [ ] Retries have a defined limit or backoff rule.
- [ ] Interrupted work can be classified as completed, safe-to-retry, or uncertain.
- [ ] Uncertain actions are reconciled instead of blindly replayed.
- [ ] Failures leave enough evidence to diagnose what happened.

## 4. Human gates and safety

- [ ] Sensitive actions require the intended approval path.
- [ ] Passwords, API keys, payment-card data, OTPs, and private tokens are not stored in ordinary logs.
- [ ] The PoC does not silently expand its authority beyond the agreed scope.
- [ ] A human can stop or disable the workflow.

## 5. Operability

- [ ] A new operator can understand how to run the PoC from its README or handoff notes.
- [ ] Required environment variables and dependencies are listed without exposing secrets.
- [ ] Known limitations are documented.
- [ ] There is a clear next step for production hardening or for deciding not to proceed.

## 6. Evidence table

Record proof, not vibes.

| Test | Result | Evidence / receipt | Notes |
|---|---|---|---|
| Happy path | ___ | ___ | ___ |
| Invalid input | ___ | ___ | ___ |
| Dependency failure | ___ | ___ | ___ |
| Retry / duplicate safety | ___ | ___ | ___ |
| Human-gated action | ___ | ___ | ___ |

## Decision

- **ACCEPT:** all critical criteria passed with evidence.
- **ACCEPT WITH LIMITATIONS:** useful for the agreed PoC scope, with limitations explicitly recorded.
- **REJECT / REWORK:** a critical criterion failed or evidence is insufficient.

---

Need the planning pieces before acceptance testing? The **AI Automation Quickstart Kit** adds a scored readiness worksheet, PoC planning canvas, API preflight checklist, reliability/recovery checklist, and ROI estimator:

https://buy.stripe.com/3cIdR8cxw2ou8EFbOHgEg09

This template is a practical engineering aid, not a security audit, legal/compliance review, or guarantee of business outcomes.
