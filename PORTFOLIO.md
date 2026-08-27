# AgentLink Portfolio

This page is the public portfolio index for AgentLink's verified technical demos, case studies, and paid engineering offers.

The production AgentLink core remains private. Public examples are deliberately standalone and avoid exposing private authorization, infrastructure, credentials, customer data, or internal runbooks.

## Technical demos

### Receipt Replay Simulator

Path: `demos/receipt-replay-simulator/`

Demonstrates conservative recovery after interrupted external actions:

- completed receipt -> skip duplicate execution
- not-started receipt -> retry
- uncertain receipt -> reconcile

### Idempotency Key Simulator

Path: `demos/idempotency-key-simulator/`

Demonstrates:

- stable job identity
- idempotency-key lookup
- first execution versus duplicate replay
- returning the original receipt on repeated attempts

### Worker Lease Recovery Simulator

Path: `demos/worker-lease-recovery/`

Demonstrates:

- worker ownership leases
- lease expiry
- stale-owner detection
- safe re-claim by another worker
- explicit job-state transitions

## Case study

### RAG Fleet Harness MVP

See `CASE_STUDY_RAG_FLEET.md`.

Verified public claims include:

- 10 isolated RAG-agent configurations
- routing by agent ID
- fleet health reporting
- deterministic local retrieval proof
- unknown-agent handling
- invalid-configuration validation
- 5 automated tests passed

## Paid services

### AI Automation Opportunity Scan — ¥2,980

Asynchronous review of one workflow or automation idea with candidate automations, difficulty, risks, and next actions.

Buy: https://buy.stripe.com/14AdR8dBAd38g77f0TgEg06

### AI Agent / RAG Architecture Quick Audit — ¥9,800

Architecture review, risk checklist, quality/operability gaps, prioritized next steps, and an implementation plan.

Buy: https://buy.stripe.com/00w7sK7dc4wCf33f0TgEg05

### Agent Reliability & Recovery Review — ¥14,800

Review focused on duplicate execution, idempotency, retries, failure recovery, worker leases, stale-owner recovery, receipts, and auditability.

Buy: https://buy.stripe.com/8x2fZg4104wC9IJ4mfgEg08

### AI Automation Small PoC Starter — ¥29,800

One narrow, non-production workflow PoC with requirements, boundary definition, a small executable prototype, basic validation, and handoff notes.

Buy: https://buy.stripe.com/eVq9AS8hg8MS6wxbOHgEg07

### Larger PoCs

Reference scopes currently include:

- Working Python / API / RAG PoC — from ¥59,800
- Multi-step AI Agent / RAG PoC — from ¥98,000
- Enterprise design-partner PoCs — scoped separately

See `SERVICES.md` and `POC.md`.

## Contact / intake

Use the repository's Paid Service Request issue form for non-confidential inquiries.

Do not post credentials, API keys, customer data, private URLs, proprietary datasets, or other confidential information in a public issue.
