# Idempotency Key Simulator

A tiny standalone demo showing how an execution layer can avoid repeating the same external side effect when the same job is retried.

This is illustrative code only. It is not production AgentLink code and contains no private infrastructure.

## What it demonstrates

- stable job identity
- idempotency-key lookup
- first execution versus duplicate replay
- deterministic receipt storage

## Run

```bash
python simulator.py
```

Expected behavior: the first attempt executes, later attempts using the same idempotency key return the original receipt instead of executing again.
