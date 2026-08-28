# AgentLink Practical Guides

Short, implementation-oriented notes for building AI automation and agent workflows with clearer operating boundaries.

## Start here

### AI Automation PoC Boundaries

Before automating a large workflow, define one observable outcome, run an API preflight, decide recovery behavior, and separate proof from production complexity.

- [Read: AI Automation PoC Boundaries](./ai-automation-poc-boundaries.md)

### AI Agent Idempotency & Receipt Safety

A practical guide to preventing duplicate external actions during retries, resumes, and partial failures. Covers idempotency keys, effect receipts, read-back verification, reconciliation, and authority boundaries.

- [Read: AIエージェントの二重実行を防ぐ](./ai-agent-idempotency-safety.md)

### AI Agent Unknown-Outcome Recovery

What to do when a local run failed but the external side effect may already have happened. Covers explicit unknown states, read-back reconciliation, provider-side receipts, and safe resume behavior.

- [Read: AI Agent Unknown-Outcome Recovery](./ai-agent-unknown-outcome-recovery.md)

### AI Agent Production Readiness Checklist

A compact checklist for deciding whether an agent workflow is ready to move beyond a successful demo into repeatable operation.

- [Read: AI Agent Production Readiness Checklist](./ai-agent-production-readiness-checklist.md)

### Debuggable RAG Operations

A practical operating contract for diagnosing bad RAG answers without guesswork. Covers source IDs, run IDs, agent/corpus isolation, validation, health reporting, and regression tests around failure boundaries.

- [Read: Debuggable RAG Operations](./debuggable-rag-operations.md)

### AI Agent Incident Recovery Runbook

A provider-neutral incident flow for freezing affected writes, classifying side effects, reconciling uncertain outcomes, restoring from trustworthy checkpoints, re-establishing ownership, and resuming only unfinished work.

- [Read: AI Agent Incident Recovery Runbook](./ai-agent-incident-recovery-runbook.md)

## Public tools

- [Retry Guard](../tools/retry_guard.py) — conservative retry/reconcile classification
- [Receipt Ledger Check](../tools/receipt_ledger_check.py) — JSONL receipt consistency validation
- [CSV Doctor](../tools/csv-doctor/) — structural CSV/TSV checks before handoff

## Verified engineering proof

AgentLink also publishes a sanitized RAG Fleet Harness case study demonstrating 10 isolated agent configurations, routing, source-aware results, run IDs, health reporting, validation, unknown-agent handling, and five passing automated tests.

- [RAG Fleet Harness MVP case study](../CASE_STUDY_RAG_FLEET.md)

## Services and starter kits

For a compact DIY planning bundle or fixed-scope reviews and PoCs, see:

- [AgentLink Services](../SERVICES.md)

Current public descriptions intentionally avoid claiming customer outcomes that have not been verified.
