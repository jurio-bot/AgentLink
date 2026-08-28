# AgentLink Public Reliability Tools

Small, dependency-free utilities that demonstrate conservative automation-recovery patterns without exposing AgentLink's private production core.

## Retry Guard

`retry_guard.py` classifies whether an interrupted automation should execute again.

It accepts a JSON receipt/incident record and emits one decision:

- `SKIP_COMPLETED` — a success receipt/status already proves completion.
- `RETRY` — no external side effect occurred and the retry budget remains.
- `RECONCILE` — an external side effect is confirmed or its outcome is uncertain; inspect the external system before attempting another write.
- `HUMAN_REVIEW` — a human gate or retry limit requires review.

### Run

```bash
echo '{"status":"failed","side_effect":"unknown"}' | python tools/retry_guard.py
```

Expected output:

```text
RECONCILE
```

JSON output is also available:

```bash
echo '{"status":"failed","side_effect":"none","attempts":1}' | python tools/retry_guard.py --json
```

### Input fields

| Field | Type | Meaning |
|---|---|---|
| `status` | string | Execution status such as `succeeded`, `failed`, `blocked`, or `human_gate`. |
| `receipt_present` | bool | Whether a durable completion receipt exists. |
| `side_effect` | string | `none`, `confirmed`, or `unknown`. Defaults to `unknown` to avoid unsafe blind retry. |
| `attempts` | int | Retry attempts already used. Defaults to `0`. |
| `max_attempts` | int | Retry ceiling. Defaults to `3`. |

### Test

```bash
cd tools
python -m unittest -v test_retry_guard.py
```

The utility is intentionally narrow. It does not call external APIs, bypass approval gates, infer success from missing evidence, or perform retries itself. The caller remains responsible for external-system reconciliation and policy decisions.
