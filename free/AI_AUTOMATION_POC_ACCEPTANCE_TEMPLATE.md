# AI Automation PoC Acceptance Template

A small, reusable acceptance sheet for AI/API automation proofs of concept.

Use this before calling a PoC “done.” Replace bracketed text with project-specific facts.

## 1. Boundary

- Workflow: [one narrow workflow]
- Trigger/input: [what starts the run]
- Expected output: [observable artifact/result]
- Explicitly out of scope: [production deployment, extra integrations, etc.]

## 2. Acceptance criteria

A PoC passes only when every required item below has evidence.

| Criterion | Target | Evidence | Pass? |
|---|---|---|---|
| Happy path | [expected result] | [test/log/receipt] | |
| Invalid input | fails safely with useful error | [test/log] | |
| Duplicate/retry behavior | no unintended duplicate side effect | [test/receipt] | |
| External failure | bounded retry or explicit failure state | [test/log] | |
| Human-only gate | stops before CAPTCHA/2FA/KYC/legal approval | [receipt/screenshot] | |
| Secret handling | no credentials in repo/log/output | [review] | |
| Handoff | another operator can run the documented demo | [README/runbook] | |

## 3. Minimum evidence pack

Keep evidence small and reproducible:

- exact command or trigger used
- input fixture with secrets removed
- expected result
- actual result
- timestamped execution receipt or test output
- failure-case result
- known limitations

Do not substitute claims such as “works reliably” for evidence.

## 4. Recovery decision

For interrupted work, classify the last attempt before retrying:

- **Completed with receipt:** do not repeat the side effect.
- **Definitely not started:** retry is allowed within the PoC boundary.
- **Uncertain:** reconcile external state first. Do not blindly replay.

## 5. Human gate rule

The PoC must stop and request the operator when it reaches biometric approval, CAPTCHA, 2FA, KYC, tax/bank setup, legal attestation, contract acceptance, or another action requiring human authority.

## 6. Final handoff

Record:

- what passed
- what failed
- what remains manual
- what would be required for production
- security/reliability gaps not addressed by the PoC

---

Want the planning worksheets that come before this acceptance step? The **AI Automation Quickstart Kit** includes an automation readiness scorecard, PoC planning canvas, API preflight, reliability/recovery checklist, and ROI estimator:

https://github.com/paper-daemon/AgentLink/blob/main/DIGITAL_PRODUCTS.md

This template is a planning aid, not a security audit, legal/compliance review, or guarantee of business outcomes.
