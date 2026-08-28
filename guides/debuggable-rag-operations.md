# Debuggable RAG Operations

RAG quality is not only about how often an answer is correct. In production, a second question matters just as much:

> When the answer is wrong, can you tell why?

A RAG system that cannot explain its own retrieval path is difficult to improve safely. Teams often end up tuning prompts, changing models, or adjusting `top_k` without knowing whether the real failure came from retrieval, routing, stale data, or the wrong agent boundary.

This guide describes a small operating contract that makes RAG failures easier to diagnose before adding more infrastructure.

## 1. Keep source IDs in every retrieved hit

Every returned chunk should preserve a stable source identifier.

That gives you a fast first split when an answer is wrong:

- the wrong document was retrieved
- the right document was retrieved but ranked poorly
- retrieval was correct and the generation step failed

Without source IDs, these failure classes blur together.

## 2. Assign a run ID to every query

A run ID lets operators trace one specific execution across routing, retrieval, generation, logging, and any downstream actions.

This is especially useful when:

- multiple agents run concurrently
- retries are possible
- the same user query is executed more than once
- logs from several services are interleaved

A run ID turns “something went wrong around 14:03” into “inspect this exact execution.”

## 3. Enforce agent and corpus isolation

If a system serves several agents, projects, or tenants, retrieval should be scoped before ranking begins.

At minimum, test that:

- agent IDs are unique
- documents are attached to the intended agent only
- a query cannot silently fall through to another agent
- an unknown agent returns an explicit error

Isolation bugs can look like model hallucinations even when the model is doing exactly what the retriever gave it.

## 4. Validate configuration before serving traffic

Small validation checks prevent confusing runtime failures later.

Useful checks include:

- duplicate agent IDs
- empty corpora
- invalid `top_k`
- missing required metadata
- unavailable adapters or indexes

Validation should fail loudly and early instead of allowing a partially broken configuration into live traffic.

## 5. Expose health separately from answer quality

A healthy RAG service should be able to report whether its operating pieces are present even before evaluating semantic quality.

Examples:

- agent registered
- corpus loaded
- retriever available
- index reachable
- configuration valid
- last successful query time

This separates infrastructure failures from retrieval-quality failures.

## 6. Add regression tests around failure boundaries

The most useful early tests are often not “does this answer sound good?” tests.

Start with deterministic operating guarantees:

1. expected agents are registered
2. retrieval stays inside the selected agent
3. an unknown agent returns a clean error
4. duplicate IDs are rejected
5. empty data is flagged

These tests create a stable shell around the parts that tend to break when a prototype becomes a service.

## A small verified example

AgentLink's public RAG Fleet Harness MVP uses a deliberately simple local retriever to test this operating contract before choosing production model and vector-store adapters.

The current proof registers 10 isolated agent configurations and includes source IDs, run IDs, routing, validation, health reporting, explicit unknown-agent handling, and five passing automated tests.

See the verified case study:

- [RAG Fleet Harness MVP](../CASE_STUDY_RAG_FLEET.md)

## Production path

Once the operating contract is stable, the simple retriever can be replaced with production components such as:

- embedding providers
- vector databases
- rerankers
- evaluation datasets
- persistent stores
- auth boundaries
- monitoring and alerting
- recovery workflows

The key is to preserve the observability contract while the intelligence layer changes.

## Practical takeaway

A strong RAG system should not only answer well. It should leave enough evidence behind that a bad answer can be investigated without guesswork.

Before optimizing accuracy, make sure you can answer:

- which agent handled the query?
- which run produced the answer?
- which sources were retrieved?
- was the configuration valid?
- did the request cross the correct corpus boundary?

That makes future quality work faster, safer, and much easier to repeat.
