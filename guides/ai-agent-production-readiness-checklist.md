# AI Agent Production Readiness Checklist

A practical checklist for moving an AI agent or automation from "it worked once" to something safer to operate repeatedly.

## 1. Idempotency

- Every externally meaningful job has a stable idempotency key.
- A completed effect is never repeated only because a local process restarted.
- Retries are classified before execution: retry, reconcile, skip, or human review.

## 2. External effect receipts

- Email, GitHub, payment, application, notification, and other writes keep provider-side evidence.
- Receipts include durable identifiers such as message ID, commit SHA, URL, or provider ID.
- Success is verified by read-back when the external system supports it.

## 3. Checkpoint and recovery

- Multi-step work records the last safe checkpoint.
- Restarting does not automatically restart the whole workflow.
- Unknown side-effect state is treated as a reconciliation problem, not a blind retry.

## 4. Authority boundaries

- The system separates "technically possible" from "authorized to execute".
- Payments, contracts, identity/KYC, and sensitive public actions have explicit boundaries.
- Human gates are represented as state rather than hidden assumptions.

## 5. Observability

- Each run has a run/job ID.
- Logs can be tied back to the specific request and external effects.
- Failure reasons are structured enough to support recovery decisions.

## 6. Retrieval / RAG systems

- Source IDs are preserved.
- Retrieval results can be inspected independently from generated answers.
- Unknown-agent, empty-result, and bad-source cases have defined behavior.
- Health and validation checks exist outside the happy path.

## 7. Production acceptance test

Before calling the system production-ready, test at least these scenarios:

1. Run the same request twice.
2. Interrupt after an external write but before local completion.
3. Restart from a checkpoint.
4. Remove or invalidate a dependency.
5. Trigger an action that requires authority the agent does not have.
6. Confirm the system can explain what happened using receipts and IDs.

The goal is not zero failure. The goal is bounded failure, verifiable effects, and safe recovery.

Related:

- [AI Agent Idempotency & Side-Effect Safety](./ai-agent-idempotency-safety.md)
- [AI Automation PoC Boundaries](./ai-automation-poc-boundaries.md)
- [RAG Fleet Case Study](../CASE_STUDY_RAG_FLEET.md)
- [AgentLink Services](../SERVICES.md)
