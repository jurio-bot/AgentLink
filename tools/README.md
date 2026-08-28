# AgentLink Public Tools

Small, dependency-free utilities published as practical, testable building blocks. They are intentionally standalone and do not expose AgentLink's private production core.

## CSV Doctor

[`csv-doctor/`](./csv-doctor/) diagnoses common CSV/TSV delivery problems before a file reaches a client or downstream system.

It checks issues such as:

- encoding and delimiter detection
- blank rows
- duplicate rows
- inconsistent column counts
- basic structural quality signals

Run it with ordinary Python; no third-party package is required. The directory includes unit tests and its own README/quick start.

## Retry Guard

`retry_guard.py` classifies whether an interrupted automation should execute again.

It accepts a JSON receipt/incident record and emits one decision:

- `SKIP_COMPLETED` — a success receipt/status already proves completion.
- `RETRY` — no external side effect occurred and the retry budget remains.
- `RECONCILE` — an external side effect is confirmed or its outcome is uncertain; inspect the external system before attempting another write.
- `HUMAN_REVIEW` — a human gate or retry limit requires review.

### Run Retry Guard

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

### Retry Guard input fields

| Field | Type | Meaning |
|---|---|---|
| `status` | string | Execution status such as `succeeded`, `failed`, `blocked`, or `human_gate`. |
| `receipt_present` | bool | Whether a durable completion receipt exists. |
| `side_effect` | string | `none`, `confirmed`, or `unknown`. Defaults to `unknown` to avoid unsafe blind retry. |
| `attempts` | int | Retry attempts already used. Defaults to `0`. |
| `max_attempts` | int | Retry ceiling. Defaults to `3`. |

### Test Retry Guard

```bash
cd tools
python -m unittest -v test_retry_guard.py
```

## Receipt Ledger Check

`receipt_ledger_check.py` validates a JSONL ledger of external-effect receipts without performing any external action.

It detects:

- missing idempotency keys
- duplicate idempotency keys
- malformed JSON records
- unknown status values
- completed receipts that lack a provider-side object ID
- duplicate provider IDs among completed receipts

### Run Receipt Ledger Check

```bash
python tools/receipt_ledger_check.py receipts.jsonl
```

For machine-readable output:

```bash
python tools/receipt_ledger_check.py --json receipts.jsonl
```

### Test Receipt Ledger Check

```bash
cd tools
python -m unittest -v test_receipt_ledger_check.py
```

These utilities are intentionally narrow. They do not call external APIs, bypass approval gates, infer success from missing evidence, or perform retries themselves. The caller remains responsible for external-system reconciliation and policy decisions.
