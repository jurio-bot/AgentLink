# AI Agent Unknown-Outcome Recovery

The hardest failure in automation is often not a clean error. It is an **unknown outcome**: the local process failed, but the external side effect may already have happened.

Examples:

- an email request timed out after the provider accepted it
- a job application page closed after submission but before local confirmation
- a payment API returned no response after the charge was created
- a social post request lost connection after publish
- a GitHub write succeeded but the caller never received the commit SHA

Blind retry turns an uncertain state into a duplicate-effect risk.

## 1. Model unknown explicitly

Do not collapse every incomplete run into `failed`.

Useful states are:

- `pending`
- `confirmed_success`
- `confirmed_failure`
- `unknown_outcome`
- `needs_reconciliation`

`unknown_outcome` means: do not repeat the effect yet.

## 2. Reconcile before retry

When possible, query the external system using stable identifiers and surrounding evidence.

Examples:

- search sent mail for a deterministic subject or message token
- read the application/proposal history
- look up payment intent / transaction state
- inspect the account's newest post
- fetch the target GitHub file or commit

A reconciliation step answers one question: **did the external effect already happen?**

## 3. Keep an effect receipt

A good receipt records provider-side evidence, not just a local success flag.

```json
{
  "job_id": "job-123",
  "idempotency_key": "apply-role-456-v1",
  "effect": "job_application",
  "status": "confirmed_success",
  "provider_receipt_id": "proposal-789",
  "verified_at": "2026-08-28T12:34:56Z"
}
```

Useful receipt fields include URL, message ID, proposal ID, payment ID, commit SHA, or other durable provider identifiers.

## 4. Separate retryable work from non-repeatable effects

A workflow may contain both.

Safe to retry freely:

- local parsing
- scoring
- drafting
- validation
- read-only retrieval

Needs reconciliation before retry:

- sends
- publishes
- applications
- purchases
- payments
- external mutations

This boundary should exist in code and state, not only in documentation.

## 5. Resume from a checkpoint

After reconciliation, continue from the last safe checkpoint instead of restarting the whole workflow.

Typical recovery branch:

1. detect interrupted run
2. mark effect `unknown_outcome`
3. read external state
4. if effect exists, save receipt and continue
5. if effect is confirmed absent, retry using the same idempotency key
6. if still uncertain, stop for human or policy review

## 6. Production acceptance test

Before trusting an agent with side effects, simulate:

1. the provider accepts the write
2. the network response is dropped
3. the local process restarts
4. the agent must recover without repeating the write

If the only recovery path is "try again," the workflow is not production-ready yet.

Related:

- [AI Agent Idempotency & Side-Effect Safety](./ai-agent-idempotency-safety.md)
- [AI Agent Production Readiness Checklist](./ai-agent-production-readiness-checklist.md)
- [AI Automation PoC Boundaries](./ai-automation-poc-boundaries.md)
