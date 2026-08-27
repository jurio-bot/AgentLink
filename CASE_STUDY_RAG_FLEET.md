# Case Study: RAG Fleet Harness MVP

## Problem

A single RAG prototype is easy to start. Operations get harder when a team needs many isolated agents with separate corpora, routing, validation, run identifiers, health reporting, and predictable failure behavior.

This proof-of-concept asks a narrow question:

> Can a small, dependency-light harness establish the operating contract for a fleet of RAG agents before choosing production model and vector-store adapters?

## Prototype

The internal MVP registers **10 isolated agent configurations** behind one Python harness.

The core prototype supports:

- fleet configuration loading
- unique agent IDs
- per-agent documents and `top_k`
- query routing by agent ID
- deterministic local token-overlap retrieval for the proof layer
- source IDs in returned hits
- run IDs
- fleet validation
- health reporting
- clean error for an unknown agent

The local retriever is deliberately simple. Its purpose is to validate fleet isolation, routing, validation, observability shape, and handoff boundaries without hiding those concerns behind a larger vector database or model stack.

## Validation

The MVP has an automated test set covering:

1. a 10-agent fleet is registered and reported correctly
2. retrieval stays isolated to the selected agent
3. an unknown agent returns a clean error
4. duplicate agent IDs are rejected
5. empty document configuration is flagged by validation

**Result: 5 tests passed.**

Additional command-line checks exercise validation, health output, and a sample agent query.

## Production path

The proof is intentionally not presented as a finished production RAG system. A production implementation can replace the local retriever with model / embedding / vector-store adapters while keeping useful operating concepts stable:

- fleet registration
- agent routing
- run IDs
- validation
- health output
- source-aware responses
- regression tests

Depending on project requirements, next steps can include persistent stores, embedding providers, reranking, evaluation datasets, auth boundaries, monitoring, recovery behavior, and deployment packaging.

## Why this matters

The design keeps the first implementation small enough to test quickly while exposing the parts that often become painful later: isolation, routing, observability, validation, and repeatability.

## Related services

See [SERVICES.md](./SERVICES.md) for architecture reviews and PoC implementation scopes.

For a non-confidential project inquiry, open an Issue in this repository. Do not include credentials, private datasets, client secrets, or personal data in a public issue.
