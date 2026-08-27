# Receipt Replay Simulator

A tiny, standalone demonstration of one AgentLink design idea:

> before retrying an interrupted external action, check durable receipt state so already-completed work is not repeated blindly.

This is **not production AgentLink code**. It is a deliberately simplified educational simulator with no private implementation details, endpoints, credentials, or infrastructure assumptions.

## Why this matters

Long-running agents can lose connectivity or execution ownership at awkward moments. If an agent retries everything after recovery, it can duplicate messages, writes, purchases, or other side effects.

This demo models three receipt states:

- `completed` — do not repeat the action
- `not_started` — retry is allowed
- `uncertain` — stop and reconcile instead of blindly replaying

## Run

```bash
python3 demo.py
```

Expected output shows how the same recovery routine makes different decisions depending on the durable receipt state.

## What this demonstrates

- stable action identity
- explicit receipt state
- idempotency-aware recovery decisions
- a conservative path for uncertain completion

## What this does not claim

The real-world problem is significantly harder. Production systems must consider remote-service idempotency, partial failure, concurrent workers, authorization state, reconciliation, causal ordering, expiry, and other failure modes.

This toy demo exists only to make the core reliability idea inspectable without publishing AgentLink's private production implementation.

## License

The code in this demo directory is released under the MIT License in `LICENSE`.
