# AgentLink Practical Guides

Short, implementation-oriented notes for building AI automation and agent workflows with clearer operating boundaries.

## Start here

### AI Automation PoC Boundaries

Before automating a large workflow, define one observable outcome, run an API preflight, decide recovery behavior, and separate proof from production complexity.

- [Read: AI Automation PoC Boundaries](./ai-automation-poc-boundaries.md)

### AI Agent Idempotency & Receipt Safety

A practical guide to preventing duplicate external actions during retries, resumes, and partial failures. Covers idempotency keys, effect receipts, read-back verification, reconciliation, and authority boundaries.

- [Read: AIエージェントの二重実行を防ぐ](./ai-agent-idempotency-safety.md)

## Verified engineering proof

AgentLink also publishes a sanitized RAG Fleet Harness case study demonstrating 10 isolated agent configurations, routing, source-aware results, run IDs, health reporting, validation, unknown-agent handling, and five passing automated tests.

- [RAG Fleet Harness MVP case study](../CASE_STUDY_RAG_FLEET.md)

## Services and starter kits

For a compact DIY planning bundle or fixed-scope reviews and PoCs, see:

- [AgentLink Services](../SERVICES.md)

Current public descriptions intentionally avoid claiming customer outcomes that have not been verified.
