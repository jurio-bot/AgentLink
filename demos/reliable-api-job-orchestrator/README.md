# Reliable API Job Orchestrator Demo

A small standalone Python demo of reliability primitives useful in API-backed AI and automation platforms.

## Demonstrates

- deterministic job identity from an idempotency key
- duplicate submit suppression
- worker ownership leases
- active-lease conflict prevention
- stale-worker recovery after lease expiry
- completion guarded by a valid lease
- stable completion receipts

## Run

```bash
python -m unittest -v
```

Verified locally before publication: **5 tests passed**.

This demo is intentionally dependency-light and does not expose the private AgentLink production core, authorization internals, infrastructure, credentials, or customer data. It is an engineering proof of selected reliability patterns, not a claim of a production customer deployment or cloud architecture.
