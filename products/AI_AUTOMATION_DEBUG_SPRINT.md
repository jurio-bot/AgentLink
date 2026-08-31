# Automation Debug & Recovery Sprint

**¥9,800 one-time**  
[Checkout](https://buy.stripe.com/8x214meFE4wC5st7yrgEg0g)

One existing automation / AI workflow, one concrete failure. The job is to work on the real thing, not to return a generic review.

## Included

- inspect the supplied code, config, and relevant logs
- reproduce the primary failure where the environment permits it
- isolate the cause
- make a bounded repair
- re-run a representative test
- add minimal retry, idempotency, duplicate protection, or receipts when the failure actually needs them
- return the implementation diff and verification result

## Typical failures

- API / webhook timeouts and retry loops
- duplicate external side effects
- broken state after restart
- malformed structured output reaching downstream code
- Make / n8n / Python workflow edges
- LLM step succeeds but the surrounding automation fails

## Boundary

This is not an unlimited rebuild. If the real cause requires a larger redesign, the sprint stops before expanding the scope. Authentication bypass, KYC/CAPTCHA bypass, third-party fees, legal/compliance decisions, and 24-hour operations are not included.

The paid value is the reproduction, repair, and verification in the actual workflow. A prompt-only answer or architecture memo is not the deliverable.
