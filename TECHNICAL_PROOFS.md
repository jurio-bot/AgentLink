# Technical Proof Inventory

This page lists categories of implementation evidence that exist in the private AgentLink development environment. It deliberately avoids publishing internal code, private infrastructure details, credentials, or sensitive operational data.

## Evidence categories

### Persistent execution

Private development includes mechanisms and tests around durable work state, long-running execution, checkpoints, and resume behavior.

### Action receipts

Development includes append-oriented execution receipt concepts intended to make completed work auditable and reduce unsafe replay.

### Failure replay / recovery

Recovery work includes distinguishing interrupted work from already-completed actions and using receipts when reconstructing execution state.

### Capability leases

Worker capability and availability can be represented as time-bounded state so routing does not rely indefinitely on stale worker assumptions.

### Stale-owner recovery

Long-running execution needs a way to recover ownership when a worker or generation disappears without cleanly releasing a job.

### Cloud worker activity

AgentLink development includes cloud-worker paths and persistent heartbeat concepts for extending execution beyond a single local machine.

### Parallel coordination

The project is exploring lane ownership, locking, conflict reduction, and handoff behavior for multiple concurrent workers.

## What would constitute stronger public proof

Planned public evidence should prefer reproducible measurements over screenshots alone:

- fault-injection tests
- recovery success rate
- duplicate-action count
- migration success rate
- p50 / p95 recovery time
- authorization rejection tests
- throughput vs single-worker baseline

## Publication policy

Technical proof should be published only when it can be shared without exposing:

- production endpoints
- private host information
- tokens or secrets
- sensitive authorization internals
- private customer / user data
- exploitable operational detail

The goal is to publish **credible evidence**, not attack-surface documentation.