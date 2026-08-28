# AI Automation PoC Boundaries: Decide What Not to Automate First

AI automation projects often fail before model quality becomes the real problem. The first useful question is not only “what can we automate?” but also “what should stay outside the first PoC?”

This guide describes a conservative way to define a small automation proof-of-concept before adding production complexity.

## 1. Start with one observable outcome

Choose one workflow outcome that can be verified without interpreting intent after the fact.

Examples:

- transform one known input format into one known output format
- retrieve from one bounded source set and return source-aware results
- trigger one internal action only after a validation step passes
- produce one draft artifact without publishing or sending it automatically

Avoid combining discovery, approval, money movement, external publishing, and fulfillment in the first PoC.

## 2. Run an API preflight before building

Confirm the practical integration boundary before writing the main workflow:

- authentication method
- read versus write permissions
- rate limits and quotas
- required identifiers
- sandbox or test-mode availability
- webhook or polling behavior
- retry semantics
- error response shape

A technically possible API is not automatically an operationally safe API.

## 3. Define failure and recovery behavior

Before adding more steps, decide what happens when execution stops halfway through.

Useful questions:

- Can the same step be retried safely?
- How is duplicate execution detected?
- What receipt proves that an external effect already happened?
- Where is the latest checkpoint stored?
- What happens when a worker disappears while owning a task?
- Which states require human review instead of automatic continuation?

These boundaries matter independently of model quality.

## 4. Separate proof from production

A PoC should prove the operating contract, not imitate a complete production platform.

Keep the first version narrow enough that validation is cheap and repeatable. Production work can then add authentication boundaries, persistent stores, monitoring, deployment packaging, richer evaluation, and external integrations without changing the core contract unnecessarily.

## 5. Use explicit success criteria

A small PoC is easier to evaluate when success is defined before implementation.

Examples:

- all expected inputs produce schema-valid outputs
- invalid inputs fail predictably
- duplicate execution does not duplicate the protected side effect
- source identifiers are preserved in retrieval results
- the system can resume from a saved checkpoint
- a fixed regression test set passes

## AgentLink examples

AgentLink publishes a verified RAG Fleet Harness case study covering 10 isolated agent configurations, routing, source-aware retrieval, run IDs, health reporting, validation, unknown-agent handling, and five passing automated tests:

- [RAG Fleet Harness case study](../CASE_STUDY_RAG_FLEET.md)

For a compact planning kit that includes an automation suitability score, PoC template, API preflight checklist, reliability/recovery checklist, and editable ROI calculator, see:

- [AgentLink Services](../SERVICES.md)

The public materials intentionally avoid claiming customer outcomes that have not been verified.
