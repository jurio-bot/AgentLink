# Google Form → Sheets → Slack Automation Reference

A small reference design for turning form submissions into reliable Slack work items without treating a single webhook call as the whole system.

## Flow

1. A user submits a Google Form.
2. Google Sheets remains the human-readable source table.
3. An Apps Script trigger or small worker normalizes the new row into a stable event payload.
4. A deterministic event key is derived from the response/row identity.
5. The worker checks whether that event key has already produced a Slack side effect.
6. Slack receives a structured message or channel/workflow request.
7. The worker records the Slack result, timestamp, event key, and failure state for reconciliation.

## Why keep an idempotency key?

Form and automation triggers can retry. Without a stable key, a temporary failure can turn into duplicate Slack posts or duplicate downstream work. The event key makes retries safe enough to reconcile instead of blindly repeating effects.

## Minimal payload contract

```json
{
  "event_key": "form:<form-id>:response:<response-id>",
  "submitted_at": "ISO-8601",
  "requester": "normalized value",
  "work_type": "normalized value",
  "summary": "normalized value",
  "source_row": 42
}
```

## Operational checks

- Required form fields are validated before Slack is called.
- Secrets and Slack tokens are never stored in the Sheet.
- A failed Slack call leaves a retryable record instead of being marked complete.
- A successful Slack call stores a receipt such as message/channel id.
- Reprocessing the same response does not intentionally create a second side effect.
- Human operators can see unresolved/failed rows without reading server logs.

## Implementation choices

For a small team, Apps Script can be enough. When the workflow grows, moving delivery/retry/reconciliation into a small Python or Node worker gives clearer observability and testing while Sheets stays usable by non-developers.

This is a reference architecture, not a claim of a customer deployment. AgentLink uses the same reliability ideas around idempotency, receipts, checkpoints, and recovery in its own automation work.

Related: [SERVICES.md](../../SERVICES.md)
