# Worker Lease Recovery Simulator

A standalone demo of stale-worker recovery for long-running jobs.

This toy model shows a job being claimed by one worker, the lease expiring, and a second worker safely taking ownership after the stale lease is detected.

It is illustrative only. It is not production AgentLink code and does not expose private authorization or infrastructure details.

## What it demonstrates

- worker ownership leases
- lease expiration
- stale-owner detection
- safe re-claim by another worker
- explicit job state transitions

## Run

```bash
python simulator.py
```
