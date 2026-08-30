# Receipt ledger status boundary

`receipt_ledger_check.py` treats `status` as required evidence for every receipt record.

A record with a missing or whitespace-only `status` is not considered a clean receipt. It is reported as `missing_status` so an idempotency key by itself cannot make an unknown outcome look reconciled.

Known terminal states remain `completed`, `succeeded`, `failed`, `cancelled`, and `blocked`. `pending`, `running`, and `unknown` remain accepted non-terminal states. Other non-empty values are reported as `unknown_status`.

This validator does not infer a status from other fields and does not perform retries or external reconciliation. Its job is only to make missing outcome evidence visible before another system decides what to do next.

Regression coverage includes both an omitted `status` field and a whitespace-only value.
