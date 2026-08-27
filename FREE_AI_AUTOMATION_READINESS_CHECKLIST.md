# Free AI Automation Readiness Checklist

A lightweight pre-check before spending time or money on an automation project.

Score each item **0 = no / unclear**, **1 = partly**, **2 = yes / clear**.

## Workflow clarity

1. The workflow has a clear start trigger.
2. The workflow has a clear finish condition.
3. Inputs are known and repeatable.
4. Expected outputs can be described concretely.
5. Exceptions and human-review points are known.

## Data and access

6. Required data sources are identified.
7. Required accounts / APIs / files can be accessed legitimately.
8. Sensitive data can be separated or minimized.
9. The workflow does not depend on frequent manual CAPTCHA / OTP steps.
10. API or export limits are understood well enough to test.

## Reliability

11. Duplicate execution would be detectable or harmless.
12. Failed steps can be retried without blindly repeating completed side effects.
13. There is a way to verify that the final action actually happened.
14. A human can safely take over when automation is uncertain.
15. The workflow can be tested on a narrow scope before production use.

## Business fit

16. The task happens often enough to justify automation.
17. Manual effort or delay can be estimated.
18. A useful success metric exists, such as time saved, response time, or error reduction.
19. The first version can be kept small.
20. Failure would not create unacceptable legal, financial, safety, or customer harm.

## Quick interpretation

- **32–40:** strong candidate for a narrow automation PoC.
- **22–31:** promising, but clarify the weak areas first.
- **12–21:** likely needs process cleanup before automation.
- **0–11:** automate later. The workflow itself is still too uncertain.

This checklist is intentionally conservative. A high score does not guarantee that automation is appropriate, secure, compliant, or profitable.

## Want the full planning kit?

The **AI Automation Quickstart Kit — ¥980** adds:

- a larger 24-check scorecard,
- an AI Automation PoC planning canvas,
- API integration preflight,
- reliability and recovery checklist,
- automation ROI estimator (CSV),
- usage notes and templates.

**Get the full kit:** https://buy.stripe.com/3cIdR8cxw2ou8EFbOHgEg09

For implementation or architecture review, see [SERVICES.md](./SERVICES.md).
