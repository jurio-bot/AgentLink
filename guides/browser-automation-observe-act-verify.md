# Browser Automation: Observe → Act → Verify

A browser action returning “success” is not the same thing as the intended outcome being true.

Modern web apps are dynamic. A button can be found and clicked while the page is still changing, a composer can accept focus without accepting text, a submit control can fire while the network request later fails, or the UI can move to an intermediate state that looks finished but is not.

A safer operating loop is:

1. **Observe** the current page and identify the intended target from fresh state.
2. **Act once** with the smallest useful interaction.
3. **Verify** the resulting URL, visible state, DOM, or provider-side result before continuing.

This pattern is useful for browser-driven AI agents, RPA, test automation, and supervised computer-use workflows.

## 1. Observe fresh state

Before a mutating interaction, collect enough current state to answer:

- Am I on the expected origin and page?
- Is the intended control visible and enabled?
- Is there a login, CAPTCHA, verification, or other human-auth challenge?
- Is the target still the same element or workflow step I expected?
- Does the page already show that the intended effect happened earlier?

Do not reuse a stale element reference just because it worked several steps ago. Dynamic applications can replace nodes while keeping the screen visually similar.

## 2. Act once

Prefer one bounded interaction at a time:

- open a composer
- focus a field
- type a draft
- select one option
- submit one form

Avoid long blind chains such as “click → type → click → navigate → submit” without intermediate checks. When a chain fails, you otherwise lose the boundary between the last known-good state and the uncertain state.

For external side effects such as publishing, sending, applying, purchasing, or deleting, keep the final action behind the appropriate authority or approval boundary.

## 3. Verify post-state

Choose verification evidence that matches the effect.

### Navigation

Check the resulting URL and a page-specific visible marker.

### Form or composer input

Read the field or visible draft state back. A focus event alone is not evidence that the intended text was entered.

### Publish / send / submit

Prefer a combination of:

- provider success message
- changed URL or object identifier
- public/read-back visibility when appropriate
- server/provider receipt or API result when available

### Unknown outcome

If the action timed out or the connection dropped after submission, do **not** blindly repeat it. Reconcile first by checking whether the external object already exists.

This is especially important for messages, posts, applications, payments, and other effects where a retry can create duplicates.

## 4. Keep the receipt small

A useful browser-action receipt can be compact:

```json
{
  "action": "submit",
  "target": "post composer",
  "pre_state": "draft_present",
  "result": "confirmed",
  "verification": ["success_marker", "public_readback"]
}
```

Do not store passwords, session cookies, OTPs, private form contents, authentication tokens, or other secrets just to make the receipt more detailed.

## 5. A practical state machine

A small state model is easier to recover than a long macro:

```text
OBSERVED
  ↓
ACTION_READY
  ↓
ACTION_ATTEMPTED
  ├─→ CONFIRMED
  ├─→ FAILED
  └─→ UNKNOWN → RECONCILE → CONFIRMED / RETRY_SAFE / HUMAN_REVIEW
```

The important state is `UNKNOWN`. Treating every exception as `FAILED` encourages unsafe retries.

## Why this helps

The loop adds a little observation overhead, but it makes failures much cheaper to diagnose. Instead of asking “why did the automation break somewhere in this script?”, you can usually identify the exact boundary where observed reality stopped matching the plan.

The same idea also composes well with idempotency keys, effect receipts, checkpoints, and recovery workflows used outside the browser.

## Related guides

- [AI Agent Idempotency & Receipt Safety](./ai-agent-idempotency-safety.md)
- [AI Agent Unknown-Outcome Recovery](./ai-agent-unknown-outcome-recovery.md)
- [AI Agent Incident Recovery Runbook](./ai-agent-incident-recovery-runbook.md)

This guide describes a general operating pattern. It does not document private browser sessions, credentials, production endpoints, or authorization internals.
