# AI Agent Incident Recovery Runbook

When an AI automation fails halfway through a workflow, the safest next action is often not “retry everything.” A useful incident runbook separates diagnosis, reconciliation, recovery, and replay.

This guide is intentionally provider-neutral and focuses on operational boundaries rather than model quality.

## 1. Freeze new writes for the affected workflow

Before debugging, stop new write-producing executions for the same logical job or resource.

Keep read-only inspection available when possible. The goal is to prevent a second worker or automatic retry loop from creating additional side effects while the original outcome is still unclear.

## 2. Capture the execution identity

Record the identifiers needed to reconstruct the run:

- logical job ID
- idempotency key
- worker or lease owner
- checkpoint ID
- start time and last known progress time
- external provider object IDs already returned
- current authorization scope

Do not rely only on a chat transcript or an in-memory worker log.

## 3. Classify each side effect

For every external write, place it in one of three states:

1. **confirmed complete**: provider-side evidence proves the effect happened
2. **confirmed not started**: evidence shows no effect occurred
3. **uncertain**: timeout, disconnect, partial response, or missing receipt leaves the outcome unknown

Only the second category is automatically safe to execute again.

## 4. Reconcile uncertain effects

Query the external system using stable identifiers whenever possible.

Examples:

- email message or sent-folder lookup
- payment object status
- Git commit or blob read-back
- issue/comment lookup
- database record version
- webhook delivery log

If reconciliation is impossible, keep the action uncertain instead of silently converting it to failed.

## 5. Restore from the latest trustworthy checkpoint

A checkpoint is useful only if it represents durable state that was written before the worker disappeared.

Compare:

- checkpoint state
- external receipts
- provider-side read-back
- current resource ownership

The recovery point should reflect the most advanced state that can be proven, not merely the most advanced state a worker claimed to reach.

## 6. Re-establish ownership before continuing

Before a replacement worker resumes:

- expire or revoke stale ownership where appropriate
- acquire a new lease or resource lock
- preserve the original logical idempotency keys
- confirm the new worker has only the authority required for the remaining steps

Changing worker identity should not create a new logical action identity.

## 7. Resume only unfinished work

Build a remaining-work set from reconciliation results.

Completed external effects are skipped. Confirmed not-started effects may run. Uncertain effects stay blocked until reconciled or explicitly reviewed.

This turns recovery into a deterministic continuation problem instead of a blind replay problem.

## 8. Verify every recovered write

After each recovered write, perform read-back verification when the provider supports it and persist a durable receipt containing the provider-side identifier.

A successful API response is useful evidence, but a provider-side object ID plus read-back is stronger evidence.

## 9. Close the incident with a compact record

Keep a small incident summary containing:

- root trigger
- affected logical job
- external effects found complete
- effects reconciled as not started
- unresolved effects
- recovery checkpoint
- replacement worker or lease
- final outcome
- prevention action

This record becomes input for future retry policy, tests, and monitoring.

## Practical AgentLink references

Related public material:

- [AI agent idempotency and receipt safety](./ai-agent-idempotency-safety.md)
- [AI automation PoC boundaries](./ai-automation-poc-boundaries.md)
- [Receipt Replay Simulator](../demos/receipt-replay-simulator/)
- [Receipt Ledger Check](../tools/receipt_ledger_check.py)

For fixed-scope architecture and reliability reviews, see [AgentLink Services](../SERVICES.md).

Public documentation intentionally avoids claiming customer outcomes that have not been verified.
