# AI Automation Incident Receipt Template

A small, practical template for recording what actually happened when an automated or AI-assisted workflow fails, times out, or returns an uncertain result.

Use one receipt per incident. Keep claims evidence-based. Do not paste secrets, credentials, private customer data, or sensitive payloads into a public receipt.

## Incident identity

- Incident ID:
- Workflow / agent:
- Environment:
- Started at:
- Detected at:
- Current state: `failed` / `uncertain` / `recovered` / `needs-human-review`
- Owner:

## Intended action

- Goal:
- Expected external side effect:
- Idempotency key or deduplication key, if used:
- Expected success evidence:

## Observed evidence

- Last confirmed completed step:
- Last receipt / event ID:
- Exit code or error class:
- Timeout observed: yes / no
- External system state checked: yes / no
- Evidence links or log references:

## Side-effect certainty

Choose exactly one:

- [ ] **Confirmed not performed** — safe to retry under the normal policy.
- [ ] **Confirmed performed** — do not replay the side effect.
- [ ] **Uncertain** — reconcile with the external system before retrying.

Reason:

## Recovery decision

- Retry / reconcile / compensate / stop / escalate:
- Why this action is safe:
- Retry limit:
- Backoff or cooldown:
- Human approval required before continuing: yes / no

## Recovery result

- Recovery started at:
- Recovery finished at:
- Final state:
- Final receipt / evidence:
- Duplicate side effect detected: yes / no
- Follow-up defect or hardening task:

## Short post-incident review

1. What made the failure detectable?
2. What evidence prevented a blind retry?
3. Was the action actually idempotent, or merely assumed to be?
4. Could a stale worker or delayed callback still complete later?
5. What single change would reduce uncertainty next time?

---

This template is intentionally tool-agnostic. It can be used for API jobs, browser automation, queues, AI agents, scheduled workflows, webhook consumers, and multi-worker systems.

For a broader planning pack with readiness scoring, PoC design, API preflight, reliability checks, and ROI estimation, see the [AI Automation Quickstart Kit](./DIGITAL_PRODUCTS.md).
