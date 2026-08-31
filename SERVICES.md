# AgentLink Services

Paid work here is hands-on engineering. We do not sell prompt-only reviews, generic checklists, planning templates, or one-file cleanup that a ChatGPT Plus user can reasonably reproduce on their own.

## Automation Debug & Recovery Sprint — ¥9,800

**Checkout:** https://buy.stripe.com/8x214meFE4wC5st7yrgEg0g

For one existing automation / AI workflow with a concrete failure.

Included:
- reproduce the failure from real code, config, and logs
- isolate the cause
- patch the bounded issue
- re-run a representative test
- add minimal retry / idempotency / duplicate protection / receipts when the failure needs them
- deliver the actual diff plus verification notes

This is not a review-only product.

## Agent / RAG Reliability Hardening Sprint — ¥14,800

**Checkout:** https://buy.stripe.com/8x2fZg4104wC9IJ4mfgEg08

For one existing Agent, RAG, or automation flow that needs to keep behaving when things fail.

Included as relevant:
- duplicate-execution protection
- retry boundaries
- idempotency keys
- unknown-outcome reconciliation
- receipts / logs
- resume points
- representative failure-path tests
- implementation diff and restart notes

This is implementation work, not an architecture memo.

## Automation Deployment Sprint — ¥29,800

**Checkout:** https://buy.stripe.com/eVq9AS8hg8MS6wxbOHgEg07

For one real business workflow that should be installed and run in the actual environment.

Typical scope:
- connect roughly two services, or one local/server-side process
- implement the trigger and workflow
- configure the target environment
- add basic logging and failure handling
- test with representative data
- leave run / restart / handoff instructions

Make, n8n, Python, APIs, webhooks, local services, or another suitable route can be used depending on the job.

## Larger builds

Larger Python/API/RAG/Agent systems are quoted after the environment, integrations, failure modes, and acceptance tests are known. A higher price is for integration and verified execution, not for longer generated documents.

## Public engineering proof

- [AgentLink](./README.md)
- [RAG Fleet Harness MVP](./CASE_STUDY_RAG_FLEET.md)
- [Receipt Replay Simulator](./demos/receipt-replay-simulator/)
- [Debuggable RAG Operations](./guides/debuggable-rag-operations.md)
- [RAG Trace Check](./tools/rag_trace_check.py)

Do not put passwords, API keys, private URLs, personal data, or proprietary datasets in a public GitHub Issue. Sensitive setup details are handled only through an appropriate private delivery channel.
