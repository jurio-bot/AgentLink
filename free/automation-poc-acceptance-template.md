# AI Automation PoC Acceptance Template

Use this before building an automation PoC so “done” is measurable instead of subjective.

## 1. Workflow boundary

- Trigger / starting condition:
- Inputs available at start:
- Expected output:
- Explicitly out of scope:
- Human-only gates (approval, payment, KYC, legal, sensitive access):

## 2. Acceptance criteria

A PoC is accepted only when all applicable checks below are demonstrated with evidence.

- [ ] Happy-path run completes from defined trigger to expected output.
- [ ] Required fields are validated before execution.
- [ ] Duplicate/retry behavior is defined and tested.
- [ ] A failed step produces a visible error or receipt instead of silent success.
- [ ] Human-only gates stop safely rather than being bypassed.
- [ ] Secrets and credentials are not written into logs or deliverables.
- [ ] At least one representative failure case has been tested.
- [ ] Handoff notes explain how to run, verify, and recover the PoC.

## 3. Evidence table

| Criterion | Evidence | Result |
| --- | --- | --- |
| Happy path | command, screenshot, test output, or receipt | PASS / FAIL |
| Input validation | test/output | PASS / FAIL |
| Duplicate safety | test/output | PASS / FAIL |
| Failure visibility | test/output | PASS / FAIL |
| Human gate safety | test/output | PASS / FAIL |
| Secret hygiene | review/test | PASS / FAIL |
| Failure case | test/output | PASS / FAIL |
| Handoff | document/link | PASS / FAIL |

## 4. Decision

- Accepted / needs revision:
- Known limitations:
- Next production-hardening step:

---

This template is intentionally small. For the broader planning workflow, including readiness scoring, API preflight, reliability/recovery checks, ROI estimation, and a PoC planning canvas, see [AI Automation Quickstart Kit](../DIGITAL_PRODUCTS.md).
